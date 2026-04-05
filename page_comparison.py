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

st.markdown("""
<h2 style="background:linear-gradient(90deg,#5b52f5,#a855f7);-webkit-background-clip:text;
-webkit-text-fill-color:transparent;font-family:'Rajdhani',sans-serif;
font-size:2rem;font-weight:700;margin:0">⚔️ Player Comparison</h2>
<p style="color:#4a5568;font-size:.875rem;margin-top:4px">
Head-to-head across all 3 sports · Radar chart · Live from MySQL</p>
""", unsafe_allow_html=True)
st.info("💡 Pick a sport, select two players — radar chart and stats update instantly.")
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

sport = st.selectbox("1️⃣ Select Sport", list(SPORT_CFG.keys()))
cfg   = SPORT_CFG[sport]
raw   = run_query(cfg["q_players"])

if not raw or len(raw) < 2:
    st.warning(f"Need ≥ 2 players with recorded scores. Enter scores in the {sport.split(' ',1)[1]} module.")
    st.stop()

pmap   = {f"{p['Player_Name']} ({p['Team_Name']})": p["Player_ID"] for p in raw}
labels = list(pmap.keys())

st.markdown("**2️⃣ Choose two players:**")
c1, cv, c2 = st.columns([5,1,5])
with c1:  la = st.selectbox("🟣 Player A", labels, index=0)
with cv:  st.markdown("<div style='text-align:center;font-size:1.4rem;color:#2a3a52;padding-top:28px'>VS</div>",unsafe_allow_html=True)
with c2:  lb = st.selectbox("🟢 Player B", labels, index=min(1,len(labels)-1))

if la == lb:
    st.error("❌ Select two different players."); st.stop()

pid_a, pid_b = pmap[la], pmap[lb]
sa = cfg["q_stats"](pid_a)[0]; sb = cfg["q_stats"](pid_b)[0]
axes   = cfg["axes"]
va     = [float(sa.get(k,0) or 0) for k in axes]
vb     = [float(sb.get(k,0) or 0) for k in axes]
maxv   = [max(a,b,1) for a,b in zip(va,vb)]
na     = [round(v/m*100,1) for v,m in zip(va,maxv)]
nb     = [round(v/m*100,1) for v,m in zip(vb,maxv)]

st.divider()
chart_col, stats_col = st.columns([1.4,1])

with chart_col:
    st.subheader("Radar Chart")
    theta = axes + [axes[0]]
    fig   = go.Figure()
    fig.add_trace(go.Scatterpolar(r=na+[na[0]],theta=theta,fill="toself",
        name=la.split(" (")[0],line=dict(color=cfg["ca"],width=2),fillcolor=hex_rgba(cfg["ca"],0.15)))
    fig.add_trace(go.Scatterpolar(r=nb+[nb[0]],theta=theta,fill="toself",
        name=lb.split(" (")[0],line=dict(color=cfg["cb"],width=2),fillcolor=hex_rgba(cfg["cb"],0.15)))
    fig.update_layout(
        polar=dict(bgcolor="rgba(0,0,0,0)",
                   radialaxis=dict(visible=True,range=[0,110],gridcolor="#1e2d45",
                                   linecolor="#1e2d45",tickfont=dict(color="#3a4a6a",size=9),
                                   tickvals=[25,50,75,100]),
                   angularaxis=dict(gridcolor="#1e2d45",linecolor="#1e2d45",
                                    tickfont=dict(color="#e8ecf4",size=12))),
        paper_bgcolor="rgba(0,0,0,0)",font_color="#e8ecf4",showlegend=True,
        legend=dict(orientation="h",yanchor="bottom",y=-0.18,xanchor="center",x=0.5),
        margin=dict(t=20,b=40,l=40,r=40))
    st.plotly_chart(fig,use_container_width=True)
    st.caption("Values normalised 0–100 relative to the higher player per stat.")

with stats_col:
    st.subheader("Head-to-Head")
    rows=[]
    for stat,a,b in zip(axes,va,vb):
        w = (f"🟣 {la.split(' (')[0]}" if a>b else
             (f"🟢 {lb.split(' (')[0]}" if b>a else "🤝 Tied"))
        rows.append({"Stat":stat.replace("_"," "),la.split(" (")[0]:int(a),lb.split(" (")[0]:int(b),"Edge":w})
    cdf=pd.DataFrame(rows)
    def hle(v):
        if "🟣" in str(v): return "color:#a855f7;font-weight:bold"
        if "🟢" in str(v): return "color:#22c55e;font-weight:bold"
        return "color:#3a4a6a"
    st.dataframe(cdf.style.map(hle,subset=["Edge"]),use_container_width=True,hide_index=True)
    aw=sum(1 for r in rows if "🟣" in r["Edge"])
    bw=sum(1 for r in rows if "🟢" in r["Edge"])
    st.divider()
    if aw>bw:   wn,clr = la.split(" (")[0], cfg["ca"]
    elif bw>aw: wn,clr = lb.split(" (")[0], cfg["cb"]
    else:       wn,clr = None, "#3a4a6a"
    if wn:
        st.markdown(f"""<div style="padding:14px 18px;border-radius:10px;border-left:4px solid {clr};
        background:rgba(91,82,245,.07);font-size:14px;font-weight:600">
        🏆 Overall Edge: {wn}<br>
        <span style="font-size:12px;font-weight:400;color:#4a5568">
        Leading in {max(aw,bw)} of {len(axes)} stats</span></div>""",unsafe_allow_html=True)
    else:
        st.markdown("""<div style="padding:14px 18px;border-radius:10px;
        border-left:4px solid #3a4a6a;background:rgba(58,74,106,.07)">🤝 Evenly matched!</div>""",
        unsafe_allow_html=True)

st.caption("ARENA SNU v7 · Player Comparison · System Architect: Mudit")