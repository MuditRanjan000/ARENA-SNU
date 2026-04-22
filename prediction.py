import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from db_connection import run_query

try:
    st.set_page_config(page_title="Predictions — ARENA SNU", page_icon="📈", layout="wide")
except Exception:
    pass

# ── UNIFIED CSS ───────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
/* Base */ html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background: #080c14 !important; font-family: 'DM Sans', sans-serif; color: #b0bac8; } [data-testid="stSidebar"] { background: rgba(8,12,20,0.95) !important; border-right: 1px solid rgba(255,255,255,0.06); } [data-testid="stHeader"] { background: transparent !important; } section[data-testid="stMain"] > div { background: transparent !important; } p, label, div { color: #b0bac8; font-family: 'DM Sans', sans-serif; }
/* Dividers */ hr { border: none; border-top: 1px solid rgba(255,255,255,0.07) !important; margin: 2rem 0 !important; }
/* Buttons */ div.stButton > button { background: transparent !important; color: #fff !important; font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; font-size: 0.875rem !important; border-radius: 40px !important; border: 1px solid rgba(255,255,255,0.3) !important; padding: 0.55rem 1.6rem !important; letter-spacing: 0.03em !important; transition: all 0.25s ease !important; backdrop-filter: blur(8px) !important; } div.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 32px rgba(108,99,255,0.25) !important; border-color: rgba(108,99,255,0.5) !important; } div.stButton > button[kind="primary"], div.stFormSubmitButton > button { background: linear-gradient(135deg, rgba(108,99,255,0.6), rgba(168,85,247,0.5)) !important; color: #fff !important; font-weight: 700 !important; border-radius: 50px !important; border: 1px solid rgba(108,99,255,0.4) !important; padding: 12px 32px !important; font-family: 'Rajdhani', sans-serif !important; font-size: 1rem !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; transition: all 0.3s ease !important; width: 100% !important; } div.stButton > button[kind="primary"]:hover, div.stFormSubmitButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 12px 40px rgba(108,99,255,0.5) !important; }
/* Inputs */ div[data-baseweb="select"] > div, div[data-baseweb="input"] > div input, div[data-testid="stNumberInput"] input, [data-testid="stTimeInput"] input, [data-testid="stDateInput"] input { background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 10px !important; color: #e8ecf4 !important; font-family: 'DM Sans', sans-serif !important; } div[data-baseweb="select"] svg { color: #7a8499 !important; } div[data-baseweb="popover"] { background: #0f1623 !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 12px !important; } div[data-baseweb="menu"] { background: #0f1623 !important; } div[data-baseweb="menu"] li { color: #b0bac8 !important; } div[data-baseweb="menu"] li:hover { background: rgba(255,255,255,0.07) !important; } label[data-testid="stWidgetLabel"] p, div[data-testid="stSelectbox"] label p { color: rgba(255,255,255,0.4) !important; font-size: 0.7rem !important; letter-spacing: 4px !important; text-transform: uppercase !important; font-family: 'DM Sans', sans-serif !important; font-weight: 500 !important; margin-bottom: 6px !important; }
/* Number inputs */ div[data-testid="stNumberInput"] button { background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(255,255,255,0.1) !important; color: #b0bac8 !important; border-radius: 6px !important; }
/* Form & Containers */ div[data-testid="stForm"] { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 20px !important; padding: 1.5rem !important; } div[data-testid="stDataFrame"] { background: rgba(255,255,255,0.03) !important; border-radius: 16px !important; overflow: hidden !important; border: 1px solid rgba(255,255,255,0.08) !important; } iframe[data-testid="stDataFrameResizable"] { background: transparent !important; } div[data-testid="stAlert"] { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 12px !important; color: #b0bac8 !important; font-family: 'DM Sans', sans-serif !important; } details summary { color: #b0bac8 !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.875rem !important; } details { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 14px !important; padding: 0.25rem 1rem !important; } div[data-testid="stSpinner"] p { color: #7a8499 !important; } div[data-testid="stToast"] { background: rgba(15,22,35,0.95) !important; border: 1px solid rgba(34,197,94,0.3) !important; border-radius: 14px !important; color: #e8ecf4 !important; backdrop-filter: blur(18px) !important; } .js-plotly-plot .plotly { background: transparent !important; }
/* Tabs */ [data-testid="stTabs"] [data-baseweb="tab-list"] { background: rgba(255,255,255,0.03); border-radius: 50px; padding: 4px; border: 1px solid rgba(255,255,255,0.08); gap: 4px; } [data-testid="stTabs"] [data-baseweb="tab"] { background: transparent; border-radius: 50px; color: rgba(255,255,255,0.45); font-family: 'DM Sans', sans-serif; font-weight: 500; font-size: 0.875rem; padding: 8px 20px; border: none; transition: all 0.25s; } [data-testid="stTabs"] [aria-selected="true"] { background: rgba(255,255,255,0.1) !important; color: #fff !important; border: 1px solid rgba(255,255,255,0.2) !important; } [data-testid="stTabs"] [data-baseweb="tab-highlight"], [data-testid="stTabs"] [data-baseweb="tab-border"] { background: transparent !important; }
/* Metrics */ div[data-testid="stMetric"] { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 16px !important; padding: 20px 22px !important; backdrop-filter: blur(18px) !important; } div[data-testid="stMetric"] label { color: rgba(255,255,255,0.35) !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.65rem !important; letter-spacing: 4px !important; text-transform: uppercase !important; } div[data-testid="stMetricValue"] { font-family: 'Rajdhani', sans-serif !important; font-size: 2rem !important; font-weight: 700 !important; color: #e8ecf4 !important; } div[data-testid="stMetricDelta"] { display: none !important; } footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

def hex_rgba(hex_color, alpha=0.15):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

# ── HERO HEADER ───────────────────────────────────────────────
st.markdown("""
<div style="padding: 2.5rem 0 1rem; position: relative;">
    <div style="display: inline-block; background: rgba(108,99,255,0.1); border: 1px solid rgba(108,99,255,0.22);
        border-radius: 20px; padding: 4px 14px; margin-bottom: 18px;">
        <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
            color:rgba(255,255,255,0.45); text-transform:uppercase; font-weight:500;">
            ARENA SNU · MACHINE LEARNING
        </span>
    </div>
    <h1 style="font-family:'Rajdhani',sans-serif; font-size:3rem; font-weight:800; margin:0;
        line-height:1.0; color:#fff; letter-spacing:-0.01em;">
        ML Performance <span style="color:#a855f7;">Predictor</span>
    </h1>
    <div style="width:52px; height:3px; background:linear-gradient(90deg,#6c63ff,transparent);
        border-radius:2px; margin:14px 0 12px 0;"></div>
    <p style="font-family:'DM Sans',sans-serif; color:#7a8499; font-size:0.95rem;
        margin:0; line-height:1.7;">
        Select a sport and player to predict their next match score using linear regression on past data.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding:12px 18px; border-radius:12px; background:rgba(108,99,255,0.07);
   border:1px solid rgba(108,99,255,0.2); font-family:'DM Sans',sans-serif;
   font-size:0.85rem; color:#7a8499; margin-bottom:1.5rem; line-height:1.7;">
  💡 <strong style="color:#b0bac8">How it works:</strong>
  Fetches up to the last 10 scores from MySQL → fits a numpy linear regression line
  → plots trendline + 95% confidence band → lets you save the prediction back to the database.
</div>
""", unsafe_allow_html=True)

st.divider()

SPORT_CONFIG = {
    "🏏 Cricket":    {"table": "Scorecard_Cricket",    "metric": "Runs_Scored", "label": "Runs",   "color": "#a855f7"},
    "⚽ Football":   {"table": "Scorecard_Football",   "metric": "Goals",       "label": "Goals",  "color": "#22c55e"},
    "🏀 Basketball": {"table": "Scorecard_Basketball", "metric": "Points",      "label": "Points", "color": "#f97316"},
}

# ── SPORT + PLAYER SELECT ─────────────────────────────────────
st.markdown("""
<div style="margin-bottom:0.5rem;">
  <p style="font-family:'DM Sans',sans-serif; font-size:0.7rem; letter-spacing:5px;
     color:rgba(255,255,255,0.35); text-transform:uppercase; margin:0 0 8px">Configuration</p>
  <div style="width:36px; height:3px; background:linear-gradient(90deg,#6c63ff,transparent);
     border-radius:2px;"></div>
</div>
""", unsafe_allow_html=True)

col_sport, col_player = st.columns([1, 2], gap="large")
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
    st.markdown(f"""
    <div style="padding:16px 20px; border-radius:12px; background:rgba(249,115,22,0.06);
       border:1px solid rgba(249,115,22,0.2); font-family:'DM Sans',sans-serif;
       font-size:0.875rem; color:#fdba74; margin-top:1rem;">
      ⚠️ No {sport_name} scorecard data found. Enter scores in the {sport_name} module first.
    </div>
    """, unsafe_allow_html=True)
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
    st.markdown("""
    <div style="padding:16px 20px; border-radius:12px; background:rgba(249,115,22,0.06);
       border:1px solid rgba(249,115,22,0.2); font-family:'DM Sans',sans-serif;
       font-size:0.875rem; color:#fdba74; margin-top:1rem;">
      ⚠️ This player needs at least 2 match entries for regression. Enter more scores first.
    </div>
    """, unsafe_allow_html=True)
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

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
st.divider()

# ── STAT CALLOUTS ─────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:0.75rem;">
  <p style="font-family:'DM Sans',sans-serif; font-size:0.7rem; letter-spacing:5px;
     color:rgba(255,255,255,0.35); text-transform:uppercase; margin:0 0 8px">Prediction Output</p>
  <div style="width:36px; height:3px; background:linear-gradient(90deg,#6c63ff,transparent);
     border-radius:2px;"></div>
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4, gap="medium")
trend = "↑ Improving" if slope > 0.05 else ("↓ Declining" if slope < -0.05 else "→ Stable")

with m1:
    st.markdown(f"""
    <div style="padding:20px 22px; border-radius:16px; background:rgba(255,255,255,0.04);
       border:1px solid rgba(108,99,255,0.25); backdrop-filter:blur(18px);">
      <p style="font-family:'DM Sans',sans-serif; font-size:0.65rem; letter-spacing:4px;
         text-transform:uppercase; color:rgba(255,255,255,0.35); margin:0 0 8px;">
        Predicted Next {cfg['label']}</p>
      <p style="font-family:'Rajdhani',sans-serif; font-size:2.2rem; font-weight:800;
         color:#e8ecf4; margin:0; line-height:1;">{prediction}</p>
    </div>
    """, unsafe_allow_html=True)
with m2:
    st.markdown(f"""
    <div style="padding:20px 22px; border-radius:16px; background:rgba(255,255,255,0.04);
       border:1px solid rgba(255,255,255,0.08); backdrop-filter:blur(18px);">
      <p style="font-family:'DM Sans',sans-serif; font-size:0.65rem; letter-spacing:4px;
         text-transform:uppercase; color:rgba(255,255,255,0.35); margin:0 0 8px;">95% Range</p>
      <p style="font-family:'Rajdhani',sans-serif; font-size:1.6rem; font-weight:700;
         color:#e8ecf4; margin:0; line-height:1;">{conf_low} – {conf_high}</p>
    </div>
    """, unsafe_allow_html=True)
with m3:
    trend_color = "#86efac" if slope > 0.05 else ("#fca5a5" if slope < -0.05 else "#fde68a")
    st.markdown(f"""
    <div style="padding:20px 22px; border-radius:16px; background:rgba(255,255,255,0.04);
       border:1px solid rgba(255,255,255,0.08); backdrop-filter:blur(18px);">
      <p style="font-family:'DM Sans',sans-serif; font-size:0.65rem; letter-spacing:4px;
         text-transform:uppercase; color:rgba(255,255,255,0.35); margin:0 0 8px;">Form Trend</p>
      <p style="font-family:'Rajdhani',sans-serif; font-size:1.6rem; font-weight:700;
         color:{trend_color}; margin:0; line-height:1;">{trend}</p>
      <p style="font-family:'DM Sans',sans-serif; font-size:0.75rem; color:#7a8499; margin:4px 0 0;">
        {abs(round(slope,2))}/match</p>
    </div>
    """, unsafe_allow_html=True)
with m4:
    st.markdown(f"""
    <div style="padding:20px 22px; border-radius:16px; background:rgba(255,255,255,0.04);
       border:1px solid rgba(255,255,255,0.08); backdrop-filter:blur(18px);">
      <p style="font-family:'DM Sans',sans-serif; font-size:0.65rem; letter-spacing:4px;
         text-transform:uppercase; color:rgba(255,255,255,0.35); margin:0 0 8px;">
        Avg of Last {n}</p>
      <p style="font-family:'Rajdhani',sans-serif; font-size:2.2rem; font-weight:800;
         color:#e8ecf4; margin:0; line-height:1;">{round(y.mean(), 2)}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

# ── CHART ──────────────────────────────────────────────────────
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
    font_family="DM Sans",
    title=dict(
        text=f"{selected_label.split(' (')[0]} — {sport_name} Prediction",
        font=dict(size=15, family="Rajdhani", color="#e8ecf4")
    ),
    xaxis=dict(title="Match #", gridcolor="rgba(255,255,255,0.05)",
               linecolor="rgba(255,255,255,0.05)", tickvals=list(range(1, int(next_x)+1)),
               tickfont=dict(color="#7a8499")),
    yaxis=dict(title=cfg["label"], gridcolor="rgba(255,255,255,0.05)",
               linecolor="rgba(255,255,255,0.05)", tickfont=dict(color="#7a8499")),
    legend=dict(orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5, bgcolor="rgba(0,0,0,0)",
                font=dict(color="#b0bac8", size=12)),
    margin=dict(t=40, b=80, l=0, r=0),
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("""
<p style="font-family:'DM Sans',sans-serif; font-size:0.75rem; color:rgba(255,255,255,0.25);
   text-align:center; margin-top:-8px;">
  Shaded band = 95% confidence interval · ⭐ = predicted score for next match
</p>
""", unsafe_allow_html=True)

st.divider()

# ── SAVE PREDICTION ────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:0.75rem;">
  <p style="font-family:'DM Sans',sans-serif; font-size:0.7rem; letter-spacing:5px;
     color:rgba(255,255,255,0.35); text-transform:uppercase; margin:0 0 8px">Save</p>
  <div style="width:36px; height:3px; background:linear-gradient(90deg,#6c63ff,transparent);
     border-radius:2px;"></div>
</div>
""", unsafe_allow_html=True)

col_save, col_info = st.columns([1, 2], gap="large")
with col_save:
    if st.button("💾 Save Prediction to Database", use_container_width=True):
        run_query(
            "INSERT INTO Predictions (Player_ID, Sport_Name, Predicted_Score) VALUES (%s, %s, %s)",
            (pid, sport_name, prediction), fetch=False
        )
        st.markdown(f"""
        <div style="padding:12px 16px; border-radius:12px; background:rgba(34,197,94,0.08);
           border:1px solid rgba(34,197,94,0.25); font-family:'DM Sans',sans-serif;
           font-size:0.875rem; color:#86efac; margin-top:0.5rem;">
          ✅ Saved: <strong>{prediction}</strong> {cfg['label']}
          for {selected_label.split(' (')[0]}
        </div>
        """, unsafe_allow_html=True)

with col_info:
    st.markdown("""
    <div style="padding:14px 18px; border-radius:12px; background:rgba(255,255,255,0.03);
       border:1px solid rgba(255,255,255,0.07); font-family:'DM Sans',sans-serif;
       font-size:0.8rem; color:#7a8499; line-height:1.7; margin-top:2px;">
      Prediction is saved to the
      <code style="background:rgba(255,255,255,0.06); padding:1px 6px;
        border-radius:4px; color:#b0bac8;">Predictions</code>
      table in MySQL and can be reviewed below.
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
st.divider()

# ── PAST PREDICTIONS ──────────────────────────────────────────
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
        st.markdown("""
        <div style="padding:14px 18px; font-family:'DM Sans',sans-serif;
           font-size:0.875rem; color:#7a8499;">No predictions saved yet.</div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style="padding: 2rem 0 0.5rem; font-family:'DM Sans',sans-serif;
   font-size:0.75rem; color:rgba(255,255,255,0.2); text-align:center; letter-spacing:2px;">
  ARENA SNU · ML Module · System Architect: Mudit
</div>
""", unsafe_allow_html=True)