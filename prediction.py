# prediction.py — ARENA SNU ML Prediction Module (Novel Feature)
# Python fetches MySQL data → linear regression → stores prediction back to DB
import streamlit as st
import pandas as pd
import numpy as np
from db_connection import run_query

st.set_page_config(page_title="ARENA SNU — Predictions", page_icon="📈", layout="wide")

st.markdown("""
<h2 style='color:#6c63ff;font-weight:800'>📈 Player Performance Prediction</h2>
<p style='color:#888'>Linear regression on MySQL match data — predicts next match performance</p>
""", unsafe_allow_html=True)
st.divider()

sport_choice = st.selectbox("Select Sport", ["Cricket", "Football", "Basketball"])

if sport_choice == "Cricket":
    players = run_query("""
        SELECT DISTINCT p.Player_ID, p.Player_Name, t.Team_Name
        FROM Scorecard_Cricket sc
        JOIN Players p ON sc.Player_ID=p.Player_ID
        JOIN Teams t ON p.Team_ID=t.Team_ID
        ORDER BY p.Player_Name
    """)
    metric_col = "Runs_Scored"
    metric_name = "Runs"
    table = "Scorecard_Cricket"

elif sport_choice == "Football":
    players = run_query("""
        SELECT DISTINCT p.Player_ID, p.Player_Name, t.Team_Name
        FROM Scorecard_Football sf
        JOIN Players p ON sf.Player_ID=p.Player_ID
        JOIN Teams t ON p.Team_ID=t.Team_ID
        ORDER BY p.Player_Name
    """)
    metric_col = "Goals"
    metric_name = "Goals"
    table = "Scorecard_Football"

else:
    players = run_query("""
        SELECT DISTINCT p.Player_ID, p.Player_Name, t.Team_Name
        FROM Scorecard_Basketball sb
        JOIN Players p ON sb.Player_ID=p.Player_ID
        JOIN Teams t ON p.Team_ID=t.Team_ID
        ORDER BY p.Player_Name
    """)
    metric_col = "Points"
    metric_name = "Points"
    table = "Scorecard_Basketball"

if not players:
    st.info(f"No {sport_choice} scores entered yet.")
    st.stop()

player_map = {f"{p['Player_Name']} ({p['Team_Name']})": p["Player_ID"] for p in players}
selected_player = st.selectbox("Select Player", list(player_map.keys()))
player_id = player_map[selected_player]

# Fetch last 10 matches from MySQL
history = run_query(f"""
    SELECT {metric_col} as score FROM {table}
    WHERE Player_ID = %s ORDER BY Stat_ID DESC LIMIT 10
""", (player_id,))

if len(history) < 2:
    st.warning("Need at least 2 matches of data to make a prediction.")
    st.stop()

scores = [h["score"] for h in reversed(history)]
X = np.array(range(1, len(scores)+1)).reshape(-1,1)
y = np.array(scores, dtype=float)

# Simple linear regression without sklearn import issues
n = len(X)
x_mean, y_mean = X.mean(), y.mean()
slope = ((X.flatten() - x_mean) * (y - y_mean)).sum() / ((X.flatten() - x_mean)**2).sum()
intercept = y_mean - slope * x_mean
predicted = slope * (n + 1) + intercept
predicted = max(0, round(predicted, 1))

col1, col2 = st.columns(2)
with col1:
    st.subheader("Recent Performance (from MySQL)")
    df = pd.DataFrame({"Match": range(1, len(scores)+1), metric_name: scores})
    st.dataframe(df, use_container_width=True)
    st.line_chart(df.set_index("Match"))

with col2:
    st.subheader("Prediction")
    st.metric(f"Predicted {metric_name} in Next Match", predicted)
    st.metric("Average (last 10)", round(float(np.mean(scores)), 1))
    st.metric("Trend", "📈 Rising" if slope > 0 else "📉 Falling")

    if st.button("💾 Save Prediction to Database"):
        rows = run_query(
            "INSERT INTO Predictions (Player_ID, Sport_Name, Predicted_Score) VALUES (%s, %s, %s)",
            (player_id, sport_choice, predicted), fetch=False)
        if rows:
            st.success(f"✅ Prediction saved to MySQL Predictions table!")
        else:
            st.error("Failed to save.")

st.divider()
st.subheader("All Stored Predictions")
st.caption("Every prediction ever made — stored in MySQL Predictions table")
preds = run_query("""
    SELECT p.Player_Name, t.Team_Name, pr.Sport_Name,
           pr.Predicted_Score, pr.Predicted_At
    FROM Predictions pr
    JOIN Players p ON pr.Player_ID=p.Player_ID
    JOIN Teams t ON p.Team_ID=t.Team_ID
    ORDER BY pr.Predicted_At DESC LIMIT 20
""")
if preds:
    st.dataframe(preds, use_container_width=True)
else:
    st.info("No predictions saved yet.")

st.caption("ARENA SNU | Novel Feature: Python ML + MySQL Integration | System Architect: Mudit")
