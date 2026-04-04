# prediction.py — ARENA SNU ML Prediction Module
# System Architect: Mudit
# numpy linear regression on MySQL match history → saves back to DB

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
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
    [data-testid="stMetric"] {
        background: #1c2030; border: 1px solid #252c3d;
        border-radius: 12px; padding: 16px 20px;
    }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding:24px 0 8px">
  <h2 style="background:linear-gradient(90deg,#6c63ff,#a855f7);
     -webkit-background-clip:text;-webkit-text-fill-color:transparent;
     font-size:2rem;font-weight:800;margin:0">📈 ML Performance Predictor</h2>
  <p style="color:#6b7a99;font-size:.875rem;margin-top:4px">
     Linear Regression on MySQL match history · Predictions saved back to DB</p>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div style="padding:10px 16px;border-radius:8px;border-left:3px solid #6c63ff;
background:rgba(108,99,255,.07);font-size:13px;margin-bottom:16px">
    Fetches last 10 scores from MySQL per player · Pure <strong>numpy</strong> linear regression ·
    Scatter + trendline + 95% confidence band · Predicted score saved to <code>Predictions</code> table.
</div>
""", unsafe_allow_html=True)
st.divider()

# ── Sport + Player Selection ──────────────────────────────────
SPORT_CONFIG = {
    "Cricket": {
        "table":  "Scorecard_Cricket",
        "metric": "Runs_Scored",
        "label":  "Runs",
        "color":  "#a855f7",
        "icon":   "🏏",
    },
    "Football": {
        "table":  "Scorecard_Football",
        "metric": "Goals",
        "label":  "Goals",
        "color":  "#22c55e",
        "icon":   "⚽",
    },
    "Basketball": {
        "table":  "Scorecard_Basketball",
        "metric": "Points",
        "label":  "Points",
        "color":  "#f97316",
        "icon":   "🏀",
    },
}

col_sport, col_player = st.columns([1, 2])

with col_sport:
    sport_choice = st.selectbox("Sport", list(SPORT_CONFIG.keys()))

cfg = SPORT_CONFIG[sport_choice]

# Fetch players who have at least 3 entries (minimum for meaningful regression)
players_raw = run_query(f"""
    SELECT p.Player_ID, p.Player_Name, t.Team_Name,
           COUNT(*) AS entries
    FROM {cfg['table']} sc
    JOIN Players p ON sc.Player_ID = p.Player_ID
    JOIN Teams t ON p.Team_ID = t.Team_ID
    GROUP BY sc.Player_ID
    HAVING entries >= 1
    ORDER BY p.Player_Name
""")

if not players_raw:
    st.warning(f"⚠️ No {sport_choice} scorecard data found. Enter some scores first.")
    st.stop()

with col_player:
    player_map = {
        f"{p['Player_Name']} ({p['Team_Name']})": p for p in players_raw
    }
    selected_label = st.selectbox("Select Player", list(player_map.keys()))

player = player_map[selected_label]
pid    = player["Player_ID"]

# ── Fetch last 10 scores ──────────────────────────────────────
scores_raw = run_query(f"""
    SELECT {cfg['metric']} AS score
    FROM {cfg['table']}
    WHERE Player_ID = {pid}
    ORDER BY Stat_ID DESC
    LIMIT 10
""")

if not scores_raw:
    st.warning("No scores found for this player.")
    st.stop()

scores = [float(r["score"]) for r in reversed(scores_raw)]  # chronological order
n      = len(scores)
x      = np.arange(1, n + 1, dtype=float)
y      = np.array(scores, dtype=float)

# ── Linear Regression (pure numpy) ───────────────────────────
x_mean = x.mean()
y_mean = y.mean()
slope  = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
intercept = y_mean - slope * x_mean

next_x     = float(n + 1)
prediction = slope * next_x + intercept
prediction = max(0.0, round(prediction, 2))   # scores can't be negative

# ── Confidence band (95%) ─────────────────────────────────────
y_hat = slope * x + intercept
residuals = y - y_hat
se   = np.sqrt(np.sum(residuals ** 2) / max(n - 2, 1))
t95  = 2.0   # approx t-value for small n
margin = t95 * se * np.sqrt(1 + 1/n + (next_x - x_mean)**2 / np.sum((x - x_mean)**2))

conf_low  = max(0.0, round(prediction - margin, 2))
conf_high = round(prediction + margin, 2)

# ── Metrics Row ───────────────────────────────────────────────
st.divider()
m1, m2, m3, m4 = st.columns(4)
m1.metric(f"{cfg['icon']} Predicted Next {cfg['label']}", prediction)
m2.metric("95% Range", f"{conf_low} – {conf_high}")
m3.metric("Trend", f"{'↑' if slope >= 0 else '↓'} {abs(round(slope, 2))} per match")
m4.metric("Avg (last {})".format(n), round(y.mean(), 2))

# ── Chart ─────────────────────────────────────────────────────
fig = go.Figure()

# Confidence band
x_band = list(x) + [next_x]
y_upper = list(y_hat + t95 * se) + [conf_high]
y_lower = list(y_hat - t95 * se) + [conf_low]
y_lower = [max(0, v) for v in y_lower]

fig.add_trace(go.Scatter(
    x=x_band + x_band[::-1],
    y=y_upper + y_lower[::-1],
    fill="toself",
    fillcolor=cfg["color"] + "22",
    line=dict(color="rgba(0,0,0,0)"),
    hoverinfo="skip",
    showlegend=False,
    name="95% CI"
))

# Trend line
x_line = list(x) + [next_x]
y_line = [slope * xi + intercept for xi in x_line]
fig.add_trace(go.Scatter(
    x=x_line, y=y_line,
    mode="lines",
    name="Trend",
    line=dict(color=cfg["color"], width=2, dash="dash"),
))

# Actual scores
fig.add_trace(go.Scatter(
    x=list(x), y=list(y),
    mode="markers+lines",
    name="Actual",
    marker=dict(size=9, color=cfg["color"], line=dict(color="#fff", width=1.5)),
    line=dict(color=cfg["color"], width=1.5),
))

# Prediction point
fig.add_trace(go.Scatter(
    x=[next_x], y=[prediction],
    mode="markers",
    name=f"Prediction (Match {int(next_x)})",
    marker=dict(size=14, color="#facc15", symbol="star",
                line=dict(color="#fff", width=1.5)),
))

fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#e8ecf4",
    xaxis=dict(title="Match #", gridcolor="#252c3d", tickvals=list(range(1, int(next_x) + 1))),
    yaxis=dict(title=cfg["label"], gridcolor="#252c3d"),
    legend=dict(orientation="h", y=1.12),
    margin=dict(t=20, b=20, l=0, r=0),
    title=dict(
        text=f"{selected_label.split(' (')[0]} — {sport_choice} {cfg['label']} Prediction",
        font=dict(size=15, color="#e8ecf4")
    )
)
st.plotly_chart(fig, use_container_width=True)

# ── Save to DB ────────────────────────────────────────────────
st.divider()
if st.button("💾 Save Prediction to Database", use_container_width=True):
    run_query(
        "INSERT INTO Predictions (Player_ID, Sport_Name, Predicted_Score) VALUES (%s, %s, %s)",
        (pid, sport_choice, prediction), fetch=False
    )
    st.toast(f"Prediction saved: {prediction} {cfg['label']} for {selected_label.split(' (')[0]}", icon="✅")

# ── Past Predictions ──────────────────────────────────────────
with st.expander("📋 Saved Predictions from MySQL"):
    past = run_query("""
        SELECT p.Player_Name, pr.Sport_Name,
               pr.Predicted_Score, pr.Predicted_At
        FROM Predictions pr
        JOIN Players p ON pr.Player_ID = p.Player_ID
        ORDER BY pr.Predicted_At DESC
        LIMIT 20
    """)
    if past:
        st.dataframe(pd.DataFrame(past), use_container_width=True, hide_index=True)
    else:
        st.info("No predictions saved yet. Run the predictor and click Save.")

st.caption("ARENA SNU · ML Module · System Architect: Mudit | numpy linear regression → MySQL Predictions table")