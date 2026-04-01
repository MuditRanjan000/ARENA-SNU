# prediction.py — ARENA SNU ML Prediction Module (v2)
# Novel Feature: Python fetches MySQL data → linear regression → stores back to DB
# System Architect: Mudit
import streamlit as st
import pandas as pd
import numpy as np
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
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 20px rgba(108,99,255,.45);
    }
    [data-testid="stMetric"] {
        background: #1c2030; border: 1px solid #252c3d;
        border-radius: 12px; padding: 16px 20px;
        border-top: 3px solid #6c63ff;
    }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding:24px 0 8px">
  <h2 style="background:linear-gradient(90deg,#6c63ff,#a855f7);
     -webkit-background-clip:text;-webkit-text-fill-color:transparent;
     font-size:2rem;font-weight:800;margin:0">📈 Player Performance Prediction</h2>
  <p style="color:#6b7a99;font-size:.875rem;margin-top:4px">
     Linear regression on MySQL match history · Stores predictions back to the database</p>
</div>
""", unsafe_allow_html=True)
st.divider()

# ── Sport & Player Selection ──────────────────────────────────
col_sel1, col_sel2 = st.columns([1, 2])

SPORT_CONFIG = {
    "Cricket":    {"table": "Scorecard_Cricket",    "metric": "Runs_Scored",  "label": "Runs"},
    "Football":   {"table": "Scorecard_Football",   "metric": "Goals",        "label": "Goals"},
    "Basketball": {"table": "Scorecard_Basketball", "metric": "Points",       "label": "Points"},
}

with col_sel1:
    sport_choice = st.selectbox("Sport", list(SPORT_CONFIG.keys()))

cfg = SPORT_CONFIG[sport_choice]

join_table = {
    "Cricket":    "Scorecard_Cricket sc  JOIN Players p ON sc.Player_ID=p.Player_ID JOIN Teams t ON p.Team_ID=t.Team_ID",
    "Football":   "Scorecard_Football sf JOIN Players p ON sf.Player_ID=p.Player_ID JOIN Teams t ON p.Team_ID=t.Team_ID",
    "Basketball": "Scorecard_Basketball sb JOIN Players p ON sb.Player_ID=p.Player_ID JOIN Teams t ON p.Team_ID=t.Team_ID",
}

players = run_query(f"""
    SELECT DISTINCT p.Player_ID, p.Player_Name, t.Team_Name
    FROM {join_table[sport_choice]}
    ORDER BY p.Player_Name
""")

if not players:
    st.info(f"No {sport_choice} scores recorded yet. Enter some scores first.")
    st.stop()

player_map = {f"{p['Player_Name']} ({p['Team_Name']})": p["Player_ID"] for p in players}

with col_sel2:
    selected_player = st.selectbox("Player", list(player_map.keys()))

player_id = player_map[selected_player]

# ── Fetch match history ───────────────────────────────────────
history = run_query(
    f"SELECT {cfg['metric']} AS score FROM {cfg['table']} "
    f"WHERE Player_ID = %s ORDER BY Stat_ID DESC LIMIT 10",
    (player_id,)
)

if not history or len(history) < 2:
    st.warning("⚠️ Need at least 2 match records to generate a prediction. Enter more scores first.")
    st.stop()

scores = [h["score"] for h in reversed(history)]
n      = len(scores)
X      = np.arange(1, n + 1, dtype=float)
y      = np.array(scores, dtype=float)

# ── Linear regression (pure numpy) ───────────────────────────
x_mean, y_mean = X.mean(), y.mean()
slope     = ((X - x_mean) * (y - y_mean)).sum() / ((X - x_mean) ** 2).sum()
intercept = y_mean - slope * x_mean

predicted   = max(0.0, round(slope * (n + 1) + intercept, 1))
trend_line  = slope * X + intercept

# Confidence range: ±1 std dev of residuals
residuals   = y - (slope * X + intercept)
std_resid   = float(np.std(residuals))
conf_lo     = max(0.0, round(predicted - std_resid, 1))
conf_hi     = round(predicted + std_resid, 1)

# ── Layout ────────────────────────────────────────────────────
st.divider()
col_chart, col_metrics = st.columns([2, 1])

with col_chart:
    st.subheader(f"{selected_player} — Last {n} Matches")

    fig = go.Figure()

    # Actual scores scatter + line
    fig.add_trace(go.Scatter(
        x=list(X), y=scores,
        mode="lines+markers",
        name="Actual",
        line=dict(color="#6c63ff", width=2.5),
        marker=dict(size=8, color="#6c63ff",
                    line=dict(color="#fff", width=1.5)),
    ))

    # Trend line
    fig.add_trace(go.Scatter(
        x=list(X), y=list(trend_line),
        mode="lines",
        name="Trend",
        line=dict(color="#a855f7", width=1.5, dash="dot"),
    ))

    # Prediction point with confidence bar
    fig.add_trace(go.Scatter(
        x=[n + 1], y=[predicted],
        mode="markers",
        name=f"Prediction (Match {n+1})",
        marker=dict(size=14, color="#f5a623",
                    symbol="star",
                    line=dict(color="#fff", width=1.5)),
        error_y=dict(
            type="data", symmetric=False,
            array=[conf_hi - predicted],
            arrayminus=[predicted - conf_lo],
            color="#f5a623", thickness=1.5, width=6
        )
    ))

    # Shade the future match region
    fig.add_vrect(
        x0=n + 0.5, x1=n + 1.5,
        fillcolor="rgba(245,166,35,.06)",
        layer="below", line_width=0
    )
    fig.add_annotation(
        x=n + 1, y=max(scores) * 1.05,
        text="Next match →",
        showarrow=False, font=dict(color="#f5a623", size=11)
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color="#e8ecf4",
        xaxis=dict(title="Match #", gridcolor="#252c3d", dtick=1),
        yaxis=dict(title=cfg["label"], gridcolor="#252c3d"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1),
        margin=dict(t=20, b=0, l=0, r=0),
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

with col_metrics:
    st.subheader("Prediction Summary")

    trend_emoji = "📈 Rising" if slope > 0.1 else ("📉 Falling" if slope < -0.1 else "➡️ Stable")

    st.metric(f"Predicted {cfg['label']} (next match)", predicted)
    st.metric("Confidence Range", f"{conf_lo} – {conf_hi}",
              help="±1 standard deviation of recent residuals")
    st.metric(f"Average (last {n})", round(float(y_mean), 1))
    st.metric("Trend", trend_emoji)
    st.metric("Peak (last 10)", int(y.max()))
    st.metric("Low (last 10)",  int(y.min()))

    st.divider()
    if st.button("💾 Save Prediction to MySQL", use_container_width=True):
        with st.spinner("Saving to Predictions table…"):
            rows = run_query(
                "INSERT INTO Predictions (Player_ID, Sport_Name, Predicted_Score) VALUES (%s, %s, %s)",
                (player_id, sport_choice, predicted), fetch=False
            )
        if rows:
            st.success("✅ Saved to MySQL Predictions table!")
            st.toast("Prediction stored!", icon="💾")
        else:
            st.error("❌ Failed to save.")

# ── Prediction History ────────────────────────────────────────
st.divider()
st.subheader("📚 All Stored Predictions")
st.caption("Every prediction ever saved — pulled live from MySQL Predictions table")

preds = run_query("""
    SELECT p.Player_Name, t.Team_Name, pr.Sport_Name,
           pr.Predicted_Score, pr.Predicted_At
    FROM Predictions pr
    JOIN Players p ON pr.Player_ID=p.Player_ID
    JOIN Teams t ON p.Team_ID=t.Team_ID
    ORDER BY pr.Predicted_At DESC
    LIMIT 30
""")

if preds:
    pred_df = pd.DataFrame(preds)
    st.dataframe(pred_df, use_container_width=True, hide_index=True)

    # Mini chart: predictions over time per sport
    with st.expander("📈 Prediction Trend Chart"):
        fig2 = px.line(
            pred_df, x="Predicted_At", y="Predicted_Score",
            color="Sport_Name", markers=True,
            color_discrete_sequence=["#a855f7", "#22c55e", "#f97316"],
            labels={"Predicted_At": "Saved At", "Predicted_Score": "Predicted Score"}
        )
        fig2.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#e8ecf4",
            xaxis=dict(gridcolor="#252c3d"),
            yaxis=dict(gridcolor="#252c3d"),
            margin=dict(t=10, b=0, l=0, r=0),
        )
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No predictions saved yet. Generate and save one above!")

st.caption("ARENA SNU · Novel Feature: Python ML + MySQL Integration · System Architect: Mudit")