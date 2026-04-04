# page_comparison.py — ARENA SNU Player Comparison Tool
# Novel Feature — System Architect: Mudit
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from db_connection import run_query

try:
    st.set_page_config(page_title="Player Comparison — ARENA SNU", page_icon="⚔️", layout="wide")
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
     -webkit-text-fill-color:transparent;font-size:2rem;font-weight:800;margin:0">⚔️ Player Comparison</h2>
  <p style="color:#6b7a99;font-size:.875rem;margin-top:4px">
    Head-to-head stat comparison across any two players · Radar chart · Live from MySQL</p>
</div>
""", unsafe_allow_html=True)
st.info("💡 **How to use:** Pick a sport, then select two different players. The radar chart and table update instantly from MySQL.")
st.divider()

SPORT_QUERIES = {
    "🏏 Cricket": {
        "players": """
            SELECT DISTINCT p.Player_ID, p.Player_Name, t.Team_Name
            FROM Scorecard_Cricket sc JOIN Players p ON sc.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID ORDER BY p.Player_Name
        """,
        "stats": lambda pid: run_query(f"""
            SELECT IFNULL(SUM(Runs_Scored),0) AS Runs, IFNULL(SUM(Wickets_Taken),0) AS Wickets,
                   IFNULL(SUM(Catches),0) AS Catches, IFNULL(ROUND(SUM(Overs_Bowled),1),0) AS Overs,
                   IFNULL(COUNT(DISTINCT Match_ID),0) AS Matches
            FROM Scorecard_Cricket WHERE Player_ID={pid}
        """),
        "axes": ["Runs", "Wickets", "Catches", "Overs", "Matches"],
        "color_a": "#a855f7", "color_b": "#22c55e",
    },
    "⚽ Football": {
        "players": """
            SELECT DISTINCT p.Player_ID, p.Player_Name, t.Team_Name
            FROM Scorecard_Football sf JOIN Players p ON sf.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID ORDER BY p.Player_Name
        """,
        "stats": lambda pid: run_query(f"""
            SELECT IFNULL(SUM(Goals),0) AS Goals, IFNULL(SUM(Assists),0) AS Assists,
                   IFNULL(SUM(Yellow_Cards),0) AS Yellow_Cards, IFNULL(SUM(Red_Cards),0) AS Red_Cards,
                   IFNULL(COUNT(DISTINCT Match_ID),0) AS Matches
            FROM Scorecard_Football WHERE Player_ID={pid}
        """),
        "axes": ["Goals", "Assists", "Yellow_Cards", "Red_Cards", "Matches"],
        "color_a": "#22c55e", "color_b": "#f97316",
    },
    "🏀 Basketball": {
        "players": """
            SELECT DISTINCT p.Player_ID, p.Player_Name, t.Team_Name
            FROM Scorecard_Basketball sb JOIN Players p ON sb.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID ORDER BY p.Player_Name
        """,
        "stats": lambda pid: run_query(f"""
            SELECT IFNULL(SUM(Points),0) AS Points, IFNULL(SUM(Rebounds),0) AS Rebounds,
                   IFNULL(SUM(Assists),0) AS Assists, IFNULL(SUM(Steals),0) AS Steals,
                   IFNULL(COUNT(DISTINCT Match_ID),0) AS Matches
            FROM Scorecard_Basketball WHERE Player_ID={pid}
        """),
        "axes": ["Points", "Rebounds", "Assists", "Steals", "Matches"],
        "color_a": "#f97316", "color_b": "#3b82f6",
    },
}

sport_choice = st.selectbox("1️⃣ Select Sport", list(SPORT_QUERIES.keys()))
cfg = SPORT_QUERIES[sport_choice]

players_raw = run_query(cfg["players"])
if not players_raw or len(players_raw) < 2:
    st.warning(f"⚠️ Need at least 2 players with recorded scores to compare. Enter scores in the {sport_choice.split(' ',1)[1]} module.")
    st.stop()

player_map    = {f"{p['Player_Name']} ({p['Team_Name']})": p["Player_ID"] for p in players_raw}
player_labels = list(player_map.keys())

st.markdown("**2️⃣ Choose two players to compare:**")
col_p1, col_vs, col_p2 = st.columns([5, 1, 5])
with col_p1:
    player_a_label = st.selectbox("🟣 Player A", player_labels, index=0)
with col_vs:
    st.markdown("<div style='text-align:center;font-size:1.4rem;font-weight:800;color:#6b7a99;padding-top:28px'>VS</div>", unsafe_allow_html=True)
with col_p2:
    player_b_label = st.selectbox("🟢 Player B", player_labels, index=min(1, len(player_labels)-1))

if player_a_label == player_b_label:
    st.error("❌ Please select two different players.")
    st.stop()

pid_a = player_map[player_a_label]
pid_b = player_map[player_b_label]

stats_a_raw = cfg["stats"](pid_a)
stats_b_raw = cfg["stats"](pid_b)
if not stats_a_raw or not stats_b_raw:
    st.error("❌ Could not fetch stats.")
    st.stop()

stats_a = stats_a_raw[0]
stats_b = stats_b_raw[0]
axes    = cfg["axes"]
vals_a  = [float(stats_a.get(k, 0) or 0) for k in axes]
vals_b  = [float(stats_b.get(k, 0) or 0) for k in axes]

max_vals = [max(a, b, 1) for a, b in zip(vals_a, vals_b)]
norm_a   = [round(v / m * 100, 1) for v, m in zip(vals_a, max_vals)]
norm_b   = [round(v / m * 100, 1) for v, m in zip(vals_b, max_vals)]

st.divider()
chart_col, stats_col = st.columns([1.4, 1])

with chart_col:
    st.subheader("Radar Chart")
    fig = go.Figure()
    theta = axes + [axes[0]]

    fig.add_trace(go.Scatterpolar(
        r=norm_a + [norm_a[0]], theta=theta, fill="toself",
        name=player_a_label.split(" (")[0],
        line=dict(color=cfg["color_a"], width=2),
        fillcolor=hex_rgba(cfg["color_a"], 0.15),
    ))
    fig.add_trace(go.Scatterpolar(
        r=norm_b + [norm_b[0]], theta=theta, fill="toself",
        name=player_b_label.split(" (")[0],
        line=dict(color=cfg["color_b"], width=2),
        fillcolor=hex_rgba(cfg["color_b"], 0.15),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 110], gridcolor="#252c3d",
                            linecolor="#252c3d", tickfont=dict(color="#6b7a99", size=9),
                            tickvals=[25, 50, 75, 100]),
            angularaxis=dict(gridcolor="#252c3d", linecolor="#252c3d",
                             tickfont=dict(color="#e8ecf4", size=12)),
        ),
        paper_bgcolor="rgba(0,0,0,0)", font_color="#e8ecf4", showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.18, xanchor="center", x=0.5),
        margin=dict(t=20, b=40, l=40, r=40),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Values normalized 0–100 relative to the higher player per stat.")

with stats_col:
    st.subheader("Head-to-Head Stats")
    rows = []
    for stat, va, vb in zip(axes, vals_a, vals_b):
        winner = f"🟣 {player_a_label.split(' (')[0]}" if va > vb else (
                 f"🟢 {player_b_label.split(' (')[0]}" if vb > va else "🤝 Tied")
        rows.append({"Stat": stat.replace("_", " "),
                     player_a_label.split(" (")[0]: int(va),
                     player_b_label.split(" (")[0]: int(vb),
                     "Edge": winner})

    cmp_df = pd.DataFrame(rows)
    def highlight_edge(val):
        if "🟣" in str(val): return "color:#a855f7;font-weight:bold"
        if "🟢" in str(val): return "color:#22c55e;font-weight:bold"
        return "color:#6b7a99"
    st.dataframe(cmp_df.style.map(highlight_edge, subset=["Edge"]),
                 use_container_width=True, hide_index=True)

    a_wins = sum(1 for r in rows if "🟣" in r["Edge"])
    b_wins = sum(1 for r in rows if "🟢" in r["Edge"])
    st.divider()
    if a_wins > b_wins:
        winner_name, color = player_a_label.split(" (")[0], cfg["color_a"]
    elif b_wins > a_wins:
        winner_name, color = player_b_label.split(" (")[0], cfg["color_b"]
    else:
        winner_name, color = None, "#6b7a99"

    if winner_name:
        st.markdown(f"""<div style="padding:14px 18px;border-radius:10px;border-left:4px solid {color};
        background:rgba(108,99,255,.07);font-size:14px;font-weight:600">
            🏆 Overall Edge: {winner_name}<br>
            <span style="font-size:12px;font-weight:400;color:#6b7a99">
            Leading in {max(a_wins,b_wins)} of {len(axes)} stats</span></div>""",
        unsafe_allow_html=True)
    else:
        st.markdown("""<div style="padding:14px 18px;border-radius:10px;border-left:4px solid #6b7a99;
        background:rgba(107,122,153,.07)">🤝 Perfectly even match!</div>""", unsafe_allow_html=True)

st.divider()
with st.expander("📋 Match-by-Match History"):
    table_map = {
        "🏏 Cricket":    ("Scorecard_Cricket",    "Runs_Scored", "Stat_ID"),
        "⚽ Football":   ("Scorecard_Football",   "Goals",       "Stat_ID"),
        "🏀 Basketball": ("Scorecard_Basketball", "Points",      "Stat_ID"),
    }
    tbl, metric, id_col = table_map[sport_choice]
    hist_a = run_query(f"SELECT {id_col} AS N, {metric} AS Score FROM {tbl} WHERE Player_ID={pid_a} ORDER BY {id_col}")
    hist_b = run_query(f"SELECT {id_col} AS N, {metric} AS Score FROM {tbl} WHERE Player_ID={pid_b} ORDER BY {id_col}")

    if hist_a or hist_b:
        fig2 = go.Figure()
        if hist_a:
            fig2.add_trace(go.Scatter(x=list(range(1,len(hist_a)+1)), y=[r["Score"] for r in hist_a],
                mode="lines+markers", name=player_a_label.split(" (")[0],
                line=dict(color=cfg["color_a"], width=2), marker=dict(size=7, color=cfg["color_a"])))
        if hist_b:
            fig2.add_trace(go.Scatter(x=list(range(1,len(hist_b)+1)), y=[r["Score"] for r in hist_b],
                mode="lines+markers", name=player_b_label.split(" (")[0],
                line=dict(color=cfg["color_b"], width=2), marker=dict(size=7, color=cfg["color_b"])))
        fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#e8ecf4", xaxis=dict(title="Entry #", gridcolor="#252c3d"),
            yaxis=dict(title=metric.replace("_"," "), gridcolor="#252c3d"),
            legend=dict(orientation="h", y=1.1), margin=dict(t=10,b=0,l=0,r=0))
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No individual match history available.")

st.caption("ARENA SNU · Novel Feature: Player Comparison Tool · System Architect: Mudit")