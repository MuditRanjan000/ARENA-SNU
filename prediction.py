import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from db_connection import run_query

try:
    st.set_page_config(page_title="Predictions — ARENA SNU", page_icon="📈", layout="wide")
except Exception:
    pass

st.markdown("""
<style>
    div.stButton > button {
        background: linear-gradient(90deg, #6c63ff, #a855f7);
        color: white; font-weight: 700; border-radius: 8px;
        border: none; transition: all .3s;
    }
    div.stButton > button:hover { transform: scale(1.02); box-shadow: 0 4px 20px rgba(108,99,255,.45); }
    [data-testid="stMetric"] { background: #1c2030; border: 1px solid #252c3d; border-radius: 12px; padding: 16px 20px; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

def hex_rgba(hex_color, alpha=0.15):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

st.markdown("""
<div style="padding:20px 0 6px">
  <h2 style="background:linear-gradient(90deg,#6c63ff,#a855f7);-webkit-background-clip:text;
     -webkit-text-fill-color:transparent;font-size:2rem;font-weight:800;margin:0">📈 ML Performance Predictor</h2>
  <p style="color:#6b7a99;font-size:.875rem;margin-top:4px">
    Select a sport and player to predict their next match score using linear regression on past data.</p>
</div>
""", unsafe_allow_html=True)
st.info("💡 **How it works:** Fetches up to the last 10 scores from MySQL → fits a numpy linear regression line → plots trendline + 95% confidence band → lets you save the prediction back to the database.")
st.divider()

SPORT_CONFIG = {
    "🏏 Cricket":    {"table": "Scorecard_Cricket",    "metric": "Runs_Scored", "label": "Runs",   "color": "#a855f7"},
    "⚽ Football":   {"table": "Scorecard_Football",   "metric": "Goals",       "label": "Goals",  "color": "#22c55e"},
    "🏀 Basketball": {"table": "Scorecard_Basketball", "metric": "Points",      "label": "Points", "color": "#f97316"},
}

col_sport, col_player = st.columns([1, 2])
with col_sport:
    sport_choice = st.selectbox("1️⃣ Select Sport", list(SPORT_CONFIG.keys()))

cfg        = SPORT_CONFIG[sport_choice]
sport_name = sport_choice.split(" ", 1)[1]

players_raw = run_query(f"""
    SELECT p.Player_ID, p.Player_Name, t.Team_Name, COUNT(*) AS entries
    FROM {cfg['table']} sc
    JOIN Players p ON sc.Player_ID = p.Player_ID
    JOIN Teams t ON p.Team_ID = t.Team_ID
    GROUP BY sc.Player_ID HAVING entries >= 1
    ORDER BY p.Player_Name
""")

if not players_raw:
    st.warning(f"⚠️ No {sport_name} scorecard data found. Enter scores in the {sport_name} module first.")
    st.stop()

with col_player:
    player_map    = {f"{p['Player_Name']} ({p['Team_Name']})": p for p in players_raw}
    selected_label = st.selectbox("2️⃣ Select Player", list(player_map.keys()))

player = player_map[selected_label]
pid    = player["Player_ID"]

scores_raw = run_query(f"""
    SELECT {cfg['metric']} AS score FROM {cfg['table']}
    WHERE Player_ID = {pid} ORDER BY Stat_ID DESC LIMIT 10
""")
scores = [float(r["score"]) for r in reversed(scores_raw)]
n      = len(scores)

if n < 2:
    st.warning("⚠️ This player needs at least 2 match entries for regression. Enter more scores first.")
    if n == 1:
        st.metric(f"Only entry so far — {cfg['label']}", scores[0])
    st.stop()

x = np.arange(1, n + 1, dtype=float)
y = np.array(scores, dtype=float)

x_mean    = x.mean();  y_mean = y.mean()
denom     = np.sum((x - x_mean) ** 2)
slope     = np.sum((x - x_mean) * (y - y_mean)) / denom if denom else 0.0
intercept = y_mean - slope * x_mean
next_x    = float(n + 1)
prediction = max(0.0, round(slope * next_x + intercept, 2))

y_hat     = slope * x + intercept
residuals = y - y_hat
se        = np.sqrt(np.sum(residuals ** 2) / max(n - 2, 1))
margin    = 2.0 * se * np.sqrt(1 + 1/n + (next_x - x_mean)**2 / max(denom, 1e-9))
conf_low  = max(0.0, round(prediction - margin, 2))
conf_high = round(prediction + margin, 2)

st.divider()
m1, m2, m3, m4 = st.columns(4)
m1.metric(f"Predicted Next {cfg['label']}", prediction)
m2.metric("95% Range", f"{conf_low} – {conf_high}")
trend = "↑ Improving" if slope > 0.05 else ("↓ Declining" if slope < -0.05 else "→ Stable")
m3.metric("Form Trend", trend, f"{abs(round(slope,2))}/match")
m4.metric(f"Avg of Last {n}", round(y.mean(), 2))

c   = cfg["color"]
fig = go.Figure()

x_band  = list(x) + [next_x]
y_upper = [slope * xi + intercept + 2*se for xi in x_band]
y_lower = [max(0, slope * xi + intercept - 2*se) for xi in x_band]

fig.add_trace(go.Scatter(
    x=x_band + x_band[::-1], y=y_upper + y_lower[::-1],
    fill="toself", fillcolor=hex_rgba(c, 0.12),
    line=dict(color="rgba(0,0,0,0)"), hoverinfo="skip", showlegend=False
))
fig.add_trace(go.Scatter(
    x=list(x) + [next_x], y=[slope * xi + intercept for xi in list(x) + [next_x]],
    mode="lines", name="Trend", line=dict(color=hex_rgba(c, 0.8), width=2, dash="dash"),
))
fig.add_trace(go.Scatter(
    x=list(x), y=list(y), mode="markers+lines", name="Actual",
    marker=dict(size=10, color=c, line=dict(color="#fff", width=1.5)),
    line=dict(color=c, width=2),
))
fig.add_trace(go.Scatter(
    x=[next_x], y=[prediction], mode="markers",
    name=f"⭐ Prediction (Match {int(next_x)})",
    marker=dict(size=16, color="#facc15", symbol="star", line=dict(color="#fff", width=1.5)),
))
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#e8ecf4",
    xaxis=dict(title="Match #", gridcolor="#252c3d", tickvals=list(range(1, int(next_x)+1))),
    yaxis=dict(title=cfg["label"], gridcolor="#252c3d"),
    legend=dict(orientation="h", y=1.12), margin=dict(t=20, b=10, l=0, r=0),
    title=dict(text=f"{selected_label.split(' (')[0]} — {sport_name} Prediction", font=dict(size=15)),
)
st.plotly_chart(fig, use_container_width=True)
st.caption("Shaded band = 95% confidence interval. ⭐ = predicted score for next match.")

st.divider()
col_save, col_info = st.columns([1, 2])
with col_save:
    if st.button("💾 Save Prediction to Database", use_container_width=True):
        run_query(
            "INSERT INTO Predictions (Player_ID, Sport_Name, Predicted_Score) VALUES (%s, %s, %s)",
            (pid, sport_name, prediction), fetch=False
        )
        st.success(f"✅ Saved: {prediction} {cfg['label']} for {selected_label.split(' (')[0]}")
with col_info:
    st.markdown("""<div style="padding:10px 14px;border-radius:8px;background:#1c2030;font-size:13px;
    color:#6b7a99">Prediction is saved to the <code>Predictions</code> table in MySQL.</div>""",
    unsafe_allow_html=True)

st.divider()
with st.expander("📋 All Saved Predictions", expanded=False):
    past = run_query("""
        SELECT p.Player_Name, t.Team_Name, pr.Sport_Name, pr.Predicted_Score, pr.Predicted_At
        FROM Predictions pr
        JOIN Players p ON pr.Player_ID = p.Player_ID
        JOIN Teams t ON p.Team_ID = t.Team_ID
        ORDER BY pr.Predicted_At DESC LIMIT 30
    """)
    if past:
        st.dataframe(pd.DataFrame(past), use_container_width=True, hide_index=True)
    else:
        st.info("No predictions saved yet.")

st.caption("ARENA SNU · ML Module · System Architect: Mudit")