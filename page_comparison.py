# page_comparison.py — ARENA SNU Player Comparison v7
# System Architect: Mudit
import streamlit as st, pandas as pd
import plotly.graph_objects as go
from db_connection import run_query

try: st.set_page_config(page_title="Compare — ARENA SNU", page_icon="⚔️", layout="wide")
except: pass

def hex_rgba(h, a=0.15):
    h=h.lstrip("#"); r,g,b=int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    return f"rgba({r},{g},{b},{a})"

# ── UNIFIED CSS ───────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
/* Base */ html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background: #080c14 !important; font-family: 'DM Sans', sans-serif; color: #b0bac8; } [data-testid="stSidebar"] { background: rgba(8,12,20,0.95) !important; border-right: 1px solid rgba(255,255,255,0.06); } [data-testid="stHeader"] { background: transparent !important; } section[data-testid="stMain"] > div { background: transparent !important; } p, label, div { color: #b0bac8; font-family: 'DM Sans', sans-serif; }
/* Dividers */ hr { border: none; border-top: 1px solid rgba(255,255,255,0.07) !important; margin: 2rem 0 !important; }
/* Buttons */ div.stButton > button { background: transparent !important; color: #fff !important; font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; font-size: 0.875rem !important; border-radius: 40px !important; border: 1px solid rgba(255,255,255,0.3) !important; padding: 0.55rem 1.6rem !important; letter-spacing: 0.03em !important; transition: all 0.25s ease !important; backdrop-filter: blur(8px) !important; } div.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 32px rgba(168,85,247,0.25) !important; border-color: rgba(168,85,247,0.5) !important; } div.stButton > button[kind="primary"], div.stFormSubmitButton > button { background: linear-gradient(135deg, rgba(168,85,247,0.6), rgba(34,197,94,0.5)) !important; color: #fff !important; font-weight: 700 !important; border-radius: 50px !important; border: 1px solid rgba(168,85,247,0.4) !important; padding: 12px 32px !important; font-family: 'Rajdhani', sans-serif !important; font-size: 1rem !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; transition: all 0.3s ease !important; width: 100% !important; } div.stButton > button[kind="primary"]:hover, div.stFormSubmitButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 12px 40px rgba(168,85,247,0.5) !important; }
/* Inputs */ div[data-baseweb="select"] > div, div[data-baseweb="input"] > div input, div[data-testid="stNumberInput"] input, [data-testid="stTimeInput"] input, [data-testid="stDateInput"] input { background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 10px !important; color: #e8ecf4 !important; font-family: 'DM Sans', sans-serif !important; } div[data-baseweb="select"] svg { color: #7a8499 !important; } div[data-baseweb="popover"] { background: #0f1623 !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 12px !important; } div[data-baseweb="menu"] { background: #0f1623 !important; } div[data-baseweb="menu"] li { color: #b0bac8 !important; } div[data-baseweb="menu"] li:hover { background: rgba(255,255,255,0.07) !important; } label[data-testid="stWidgetLabel"] p, div[data-testid="stSelectbox"] label p { color: rgba(255,255,255,0.4) !important; font-size: 0.7rem !important; letter-spacing: 4px !important; text-transform: uppercase !important; font-family: 'DM Sans', sans-serif !important; font-weight: 500 !important; margin-bottom: 6px !important; }
/* Number inputs */ div[data-testid="stNumberInput"] button { background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(255,255,255,0.1) !important; color: #b0bac8 !important; border-radius: 6px !important; }
/* Form & Containers */ div[data-testid="stForm"] { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 20px !important; padding: 1.5rem !important; } div[data-testid="stDataFrame"] { background: rgba(255,255,255,0.03) !important; border-radius: 16px !important; overflow: hidden !important; border: 1px solid rgba(255,255,255,0.08) !important; } iframe[data-testid="stDataFrameResizable"] { background: transparent !important; } div[data-testid="stAlert"] { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 12px !important; color: #b0bac8 !important; font-family: 'DM Sans', sans-serif !important; } details summary { color: #b0bac8 !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.875rem !important; } details { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 14px !important; padding: 0.25rem 1rem !important; } div[data-testid="stSpinner"] p { color: #7a8499 !important; } div[data-testid="stToast"] { background: rgba(15,22,35,0.95) !important; border: 1px solid rgba(34,197,94,0.3) !important; border-radius: 14px !important; color: #e8ecf4 !important; backdrop-filter: blur(18px) !important; } .js-plotly-plot .plotly { background: transparent !important; }
/* Tabs */ [data-testid="stTabs"] [data-baseweb="tab-list"] { background: rgba(255,255,255,0.03); border-radius: 50px; padding: 4px; border: 1px solid rgba(255,255,255,0.08); gap: 4px; } [data-testid="stTabs"] [data-baseweb="tab"] { background: transparent; border-radius: 50px; color: rgba(255,255,255,0.45); font-family: 'DM Sans', sans-serif; font-weight: 500; font-size: 0.875rem; padding: 8px 20px; border: none; transition: all 0.25s; } [data-testid="stTabs"] [aria-selected="true"] { background: rgba(255,255,255,0.1) !important; color: #fff !important; border: 1px solid rgba(255,255,255,0.2) !important; } [data-testid="stTabs"] [data-baseweb="tab-highlight"], [data-testid="stTabs"] [data-baseweb="tab-border"] { background: transparent !important; }
/* Metrics */ div[data-testid="stMetric"] { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 16px !important; padding: 20px 22px !important; backdrop-filter: blur(18px) !important; } div[data-testid="stMetric"] label { color: rgba(255,255,255,0.35) !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.65rem !important; letter-spacing: 4px !important; text-transform: uppercase !important; } div[data-testid="stMetricValue"] { font-family: 'Rajdhani', sans-serif !important; font-size: 2rem !important; font-weight: 700 !important; color: #e8ecf4 !important; } div[data-testid="stMetricDelta"] { display: none !important; } footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── HERO HEADER ───────────────────────────────────────────────
st.markdown("""
<div style="padding: 2.5rem 0 1rem; position: relative;">
    <div style="display: inline-block; background: rgba(168,85,247,0.1); border: 1px solid rgba(168,85,247,0.22);
        border-radius: 20px; padding: 4px 14px; margin-bottom: 18px;">
        <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
            color:rgba(255,255,255,0.45); text-transform:uppercase; font-weight:500;">
            ARENA SNU · ANALYTICS
        </span>
    </div>
    <h1 style="font-family:'Rajdhani',sans-serif; font-size:3rem; font-weight:800; margin:0;
        line-height:1.0; color:#fff; letter-spacing:-0.01em;">
        Player <span style="background:linear-gradient(90deg,#a855f7,#22c55e);
        background-clip: text; -webkit-background-clip: text; color: transparent; -webkit-text-fill-color: transparent;">Comparison</span>
    </h1>
    <div style="width:52px; height:3px; background:linear-gradient(90deg,#a855f7,transparent);
        border-radius:2px; margin:14px 0 12px 0;"></div>
    <p style="font-family:'DM Sans',sans-serif; color:#7a8499; font-size:0.95rem;
        margin:0; line-height:1.7;">
        Head-to-head across all 3 sports · Radar chart · Live from MySQL
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding:12px 18px; border-radius:12px; background:rgba(91,82,245,0.07);
   border:1px solid rgba(91,82,245,0.2); font-family:'DM Sans',sans-serif;
   font-size:0.85rem; color:#7a8499; margin-bottom:1rem;">
  💡 Pick a sport, select two players — radar chart and stats update instantly.
</div>
""", unsafe_allow_html=True)

st.divider()

SPORT_CFG = {
    "🏏 Cricket": {
        "q_players": """
            SELECT DISTINCT p.Player_ID,p.Player_Name,t.Team_Name
            FROM Scorecard_Cricket sc JOIN Players p ON sc.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID ORDER BY p.Player_Name
        """,
        "q_stats": lambda pid: run_query(f"""
            SELECT IFNULL(SUM(Runs_Scored),0) AS Runs,
                   IFNULL(SUM(Wickets_Taken),0) AS Wickets,
                   IFNULL(SUM(Catches),0) AS Catches,
                   IFNULL(ROUND(SUM(Overs_Bowled),1),0) AS Overs,
                   IFNULL(COUNT(DISTINCT Match_ID),0) AS Matches
            FROM Scorecard_Cricket WHERE Player_ID={pid}
        """),
        "axes": ["Runs","Wickets","Catches","Overs","Matches"],
        "ca": "#a855f7", "cb": "#22c55e",
    },
    "⚽ Football": {
        "q_players": """
            SELECT DISTINCT p.Player_ID,p.Player_Name,t.Team_Name
            FROM Scorecard_Football sf JOIN Players p ON sf.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID ORDER BY p.Player_Name
        """,
        "q_stats": lambda pid: run_query(f"""
            SELECT IFNULL(SUM(Goals),0) AS Goals, IFNULL(SUM(Assists),0) AS Assists,
                   IFNULL(SUM(Yellow_Cards),0) AS Yellow_Cards,
                   IFNULL(SUM(Red_Cards),0) AS Red_Cards,
                   IFNULL(COUNT(DISTINCT Match_ID),0) AS Matches
            FROM Scorecard_Football WHERE Player_ID={pid}
        """),
        "axes": ["Goals","Assists","Yellow_Cards","Red_Cards","Matches"],
        "ca": "#22c55e", "cb": "#f97316",
    },
    "🏀 Basketball": {
        "q_players": """
            SELECT DISTINCT p.Player_ID,p.Player_Name,t.Team_Name
            FROM Scorecard_Basketball sb JOIN Players p ON sb.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID ORDER BY p.Player_Name
        """,
        "q_stats": lambda pid: run_query(f"""
            SELECT IFNULL(SUM(Points),0) AS Points, IFNULL(SUM(Rebounds),0) AS Rebounds,
                   IFNULL(SUM(Assists),0) AS Assists, IFNULL(SUM(Steals),0) AS Steals,
                   IFNULL(COUNT(DISTINCT Match_ID),0) AS Matches
            FROM Scorecard_Basketball WHERE Player_ID={pid}
        """),
        "axes": ["Points","Rebounds","Assists","Steals","Matches"],
        "ca": "#f97316", "cb": "#3b82f6",
    },
}

# ── SPORT SELECT ──────────────────────────────────────────────
sel_col, _ = st.columns([1, 2], gap="large")
with sel_col:
    sport = st.selectbox("1️⃣ Select Sport", list(SPORT_CFG.keys()))

cfg   = SPORT_CFG[sport]
raw   = run_query(cfg["q_players"])

if not raw or len(raw) < 2:
    st.markdown(f"""
    <div style="padding:16px 20px; border-radius:12px; background:rgba(249,115,22,0.06);
       border:1px solid rgba(249,115,22,0.2); font-family:'DM Sans',sans-serif;
       font-size:0.875rem; color:#fdba74; margin-top:1rem;">
      ⚠️ Need ≥ 2 players with recorded scores. Enter scores in the {sport.split(' ',1)[1]} module.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

pmap   = {f"{p['Player_Name']} ({p['Team_Name']})": p["Player_ID"] for p in raw}
labels = list(pmap.keys())

# ── PLAYER SELECTOR ──────────────────────────────────────────
st.markdown("""
<div style="margin: 1.5rem 0 0.5rem;">
  <p style="font-family:'DM Sans',sans-serif; font-size:0.7rem; letter-spacing:5px;
     color:rgba(255,255,255,0.35); text-transform:uppercase; margin:0 0 8px">Select Players</p>
  <div style="width:36px; height:3px; background:linear-gradient(90deg,#5b52f5,transparent);
     border-radius:2px;"></div>
</div>
""", unsafe_allow_html=True)

c1, cv, c2 = st.columns([5, 1, 5], gap="medium")
with c1:
    st.markdown(f"""
    <div style="display:inline-block; padding:4px 12px; border-radius:20px;
       border:1px solid rgba(168,85,247,0.4); background:rgba(168,85,247,0.08);
       font-family:'DM Sans',sans-serif; font-size:0.7rem; color:#c084fc;
       letter-spacing:3px; text-transform:uppercase; margin-bottom:6px;">Player A</div>
    """, unsafe_allow_html=True)
    la = st.selectbox("Player A", labels, index=0, label_visibility="collapsed")

with cv:
    st.markdown("""
    <div style="text-align:center; padding-top:18px;">
      <div style="font-family:'Rajdhani',sans-serif; font-size:1.3rem; font-weight:800;
         color:rgba(255,255,255,0.25); letter-spacing:2px;">VS</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div style="display:inline-block; padding:4px 12px; border-radius:20px;
       border:1px solid rgba(34,197,94,0.4); background:rgba(34,197,94,0.08);
       font-family:'DM Sans',sans-serif; font-size:0.7rem; color:#86efac;
       letter-spacing:3px; text-transform:uppercase; margin-bottom:6px;">Player B</div>
    """, unsafe_allow_html=True)
    lb = st.selectbox("Player B", labels, index=min(1,len(labels)-1), label_visibility="collapsed")

if la == lb:
    st.markdown("""
    <div style="padding:14px 18px; border-radius:12px; background:rgba(239,68,68,0.08);
       border:1px solid rgba(239,68,68,0.25); font-family:'DM Sans',sans-serif;
       font-size:0.875rem; color:#fca5a5; margin-top:0.75rem;">
      ❌ Select two different players.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

pid_a, pid_b = pmap[la], pmap[lb]
sa = cfg["q_stats"](pid_a)[0]; sb = cfg["q_stats"](pid_b)[0]
axes   = cfg["axes"]
va     = [float(sa.get(k,0) or 0) for k in axes]
vb     = [float(sb.get(k,0) or 0) for k in axes]
maxv   = [max(a,b,1) for a,b in zip(va,vb)]
na     = [round(v/m*100,1) for v,m in zip(va,maxv)]
nb     = [round(v/m*100,1) for v,m in zip(vb,maxv)]

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
st.divider()

# ── CHART + STATS ─────────────────────────────────────────────
chart_col, stats_col = st.columns([1.4, 1], gap="large")

with chart_col:
    st.markdown("""
    <div style="margin-bottom:0.75rem;">
      <p style="font-family:'DM Sans',sans-serif; font-size:0.7rem; letter-spacing:5px;
         color:rgba(255,255,255,0.35); text-transform:uppercase; margin:0 0 6px">Visual</p>
      <h3 style="font-family:'Rajdhani',sans-serif; font-size:1.4rem; font-weight:700;
         color:#e8ecf4; margin:0; line-height:1.1;">Radar Chart</h3>
      <div style="width:36px; height:3px; background:linear-gradient(90deg,#5b52f5,transparent);
         border-radius:2px; margin-top:8px;"></div>
    </div>
    """, unsafe_allow_html=True)

    theta = axes + [axes[0]]
    fig   = go.Figure()
    fig.add_trace(go.Scatterpolar(r=na+[na[0]],theta=theta,fill="toself",
        name=la.split(" (")[0],line=dict(color=cfg["ca"],width=2),fillcolor=hex_rgba(cfg["ca"],0.15)))
    fig.add_trace(go.Scatterpolar(r=nb+[nb[0]],theta=theta,fill="toself",
        name=lb.split(" (")[0],line=dict(color=cfg["cb"],width=2),fillcolor=hex_rgba(cfg["cb"],0.15)))
    fig.update_layout(
        polar=dict(bgcolor="rgba(0,0,0,0)",
                   radialaxis=dict(visible=True,range=[0,110],gridcolor="rgba(255,255,255,0.08)",
                                   linecolor="rgba(255,255,255,0.08)",tickfont=dict(color="#7a8499",size=9),
                                   tickvals=[25,50,75,100]),
                   angularaxis=dict(gridcolor="rgba(255,255,255,0.08)",linecolor="rgba(255,255,255,0.08)",
                                    tickfont=dict(color="#e8ecf4",size=12,family="DM Sans"))),
        paper_bgcolor="rgba(0,0,0,0)",font_color="#e8ecf4",showlegend=True,
        legend=dict(orientation="h",yanchor="bottom",y=-0.18,xanchor="center",x=0.5,
                    font=dict(family="DM Sans",size=12),bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=20,b=40,l=40,r=40))
    st.plotly_chart(fig,use_container_width=True)
    st.markdown("""
    <p style="font-family:'DM Sans',sans-serif; font-size:0.75rem; color:rgba(255,255,255,0.3);
       text-align:center; margin-top:-8px;">Values normalised 0–100 relative to the higher player per stat.</p>
    """, unsafe_allow_html=True)

with stats_col:
    st.markdown("""
    <div style="margin-bottom:0.75rem;">
      <p style="font-family:'DM Sans',sans-serif; font-size:0.7rem; letter-spacing:5px;
         color:rgba(255,255,255,0.35); text-transform:uppercase; margin:0 0 6px">Stats</p>
      <h3 style="font-family:'Rajdhani',sans-serif; font-size:1.4rem; font-weight:700;
         color:#e8ecf4; margin:0; line-height:1.1;">Head-to-Head</h3>
      <div style="width:36px; height:3px; background:linear-gradient(90deg,#5b52f5,transparent);
         border-radius:2px; margin-top:8px; margin-bottom:1rem;"></div>
    </div>
    """, unsafe_allow_html=True)

    rows=[]
    for stat,a,b in zip(axes,va,vb):
        w = (f"🟣 {la.split(' (')[0]}" if a>b else
             (f"🟢 {lb.split(' (')[0]}" if b>a else "🤝 Tied"))
        rows.append({"Stat":stat.replace("_"," "),la.split(" (")[0]:int(a),lb.split(" (")[0]:int(b),"Edge":w})
    cdf=pd.DataFrame(rows)
    def hle(v):
        if "🟣" in str(v): return "color:#a855f7;font-weight:bold"
        if "🟢" in str(v): return "color:#22c55e;font-weight:bold"
        return "color:#7a8499"
    st.dataframe(cdf.style.map(hle,subset=["Edge"]),use_container_width=True,hide_index=True)

    aw=sum(1 for r in rows if "🟣" in r["Edge"])
    bw=sum(1 for r in rows if "🟢" in r["Edge"])
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    st.divider()
    if aw>bw:   wn,clr = la.split(" (")[0], cfg["ca"]
    elif bw>aw: wn,clr = lb.split(" (")[0], cfg["cb"]
    else:       wn,clr = None, "rgba(255,255,255,0.2)"
    if wn:
        st.markdown(f"""
        <div style="padding:16px 20px; border-radius:14px; border-left:3px solid {clr};
           background:rgba(255,255,255,0.04); backdrop-filter:blur(18px);">
          <p style="font-family:'Rajdhani',sans-serif; font-size:1.1rem; font-weight:700;
             color:#e8ecf4; margin:0 0 4px;">🏆 Overall Edge: {wn}</p>
          <p style="font-family:'DM Sans',sans-serif; font-size:0.8rem; color:#7a8499; margin:0;">
            Leading in {max(aw,bw)} of {len(axes)} stats</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="padding:16px 20px; border-radius:14px; border-left:3px solid rgba(255,255,255,0.15);
           background:rgba(255,255,255,0.03); font-family:'DM Sans',sans-serif;
           font-size:0.875rem; color:#7a8499;">
          🤝 Evenly matched across all stats.
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style="padding: 2rem 0 0.5rem; font-family:'DM Sans',sans-serif;
   font-size:0.75rem; color:rgba(255,255,255,0.2); text-align:center; letter-spacing:2px;">
  ARENA SNU v7 · Player Comparison · System Architect: Mudit
</div>
""", unsafe_allow_html=True)