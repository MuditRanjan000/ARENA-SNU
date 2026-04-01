# page_comparison.py — ARENA SNU Player Comparison Tool
# Novel Feature — System Architect: Mudit
# Head-to-head player stat comparison with radar chart
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
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
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 20px rgba(108,99,255,.45);
    }
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
     font-size:2rem;font-weight:800;margin:0">⚔️ Player Comparison</h2>
  <p style="color:#6b7a99;font-size:.875rem;margin-top:4px">
     Head-to-head stat comparison · Radar chart · Live from MySQL</p>
</div>
""", unsafe_allow_html=True)
st.divider()

# ── Sport Selection ───────────────────────────────────────────
sport_choice = st.selectbox(
    "Select Sport",
    ["Cricket", "Football", "Basketball"],
    help="Choose the sport to compare players in"
)

# ── Fetch players with at least 1 entry ──────────────────────
SPORT_QUERIES = {
    "Cricket": {
        "players": """
            SELECT DISTINCT p.Player_ID, p.Player_Name, t.Team_Name
            FROM Scorecard_Cricket sc
            JOIN Players p ON sc.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID
            ORDER BY p.Player_Name
        """,
        "stats": lambda pid: run_query(f"""
            SELECT
                IFNULL(SUM(Runs_Scored), 0)              AS Runs,
                IFNULL(SUM(Wickets_Taken), 0)            AS Wickets,
                IFNULL(SUM(Catches), 0)                  AS Catches,
                IFNULL(ROUND(SUM(Overs_Bowled), 1), 0)   AS Overs,
                IFNULL(COUNT(DISTINCT Match_ID), 0)       AS Matches
            FROM Scorecard_Cricket WHERE Player_ID = {pid}
        """),
        "axes": ["Runs", "Wickets", "Catches", "Overs", "Matches"],
        "color_a": "#a855f7",
        "color_b": "#22c55e",
    },
    "Football": {
        "players": """
            SELECT DISTINCT p.Player_ID, p.Player_Name, t.Team_Name
            FROM Scorecard_Football sf
            JOIN Players p ON sf.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID
            ORDER BY p.Player_Name
        """,
        "stats": lambda pid: run_query(f"""
            SELECT
                IFNULL(SUM(Goals), 0)        AS Goals,
                IFNULL(SUM(Assists), 0)      AS Assists,
                IFNULL(SUM(Yellow_Cards), 0) AS Yellow_Cards,
                IFNULL(SUM(Red_Cards), 0)    AS Red_Cards,
                IFNULL(COUNT(DISTINCT Match_ID), 0) AS Matches
            FROM Scorecard_Football WHERE Player_ID = {pid}
        """),
        "axes": ["Goals", "Assists", "Yellow_Cards", "Red_Cards", "Matches"],
        "color_a": "#22c55e",
        "color_b": "#f97316",
    },
    "Basketball": {
        "players": """
            SELECT DISTINCT p.Player_ID, p.Player_Name, t.Team_Name
            FROM Scorecard_Basketball sb
            JOIN Players p ON sb.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID
            ORDER BY p.Player_Name
        """,
        "stats": lambda pid: run_query(f"""
            SELECT
                IFNULL(SUM(Points), 0)   AS Points,
                IFNULL(SUM(Rebounds), 0) AS Rebounds,
                IFNULL(SUM(Assists), 0)  AS Assists,
                IFNULL(SUM(Steals), 0)   AS Steals,
                IFNULL(COUNT(DISTINCT Match_ID), 0) AS Matches
            FROM Scorecard_Basketball WHERE Player_ID = {pid}
        """),
        "axes": ["Points", "Rebounds", "Assists", "Steals", "Matches"],
        "color_a": "#f97316",
        "color_b": "#3b82f6",
    },
}

cfg = SPORT_QUERIES[sport_choice]

players_raw = run_query(cfg["players"])
if not players_raw or len(players_raw) < 2:
    st.warning(f"⚠️ Need at least 2 {sport_choice} players with recorded scores to compare.")
    st.stop()

player_map = {f"{p['Player_Name']} ({p['Team_Name']})": p["Player_ID"] for p in players_raw}
player_labels = list(player_map.keys())

# ── Player Selection ──────────────────────────────────────────
col_p1, col_vs, col_p2 = st.columns([5, 1, 5])

with col_p1:
    player_a_label = st.selectbox("🟣 Player A", player_labels, index=0, key="pa")
with col_vs:
    st.markdown(
        "<div style='text-align:center;font-size:1.4rem;font-weight:800;"
        "color:#6b7a99;padding-top:28px'>VS</div>",
        unsafe_allow_html=True
    )
with col_p2:
    default_b = 1 if len(player_labels) > 1 else 0
    player_b_label = st.selectbox("🟢 Player B", player_labels, index=default_b, key="pb")

if player_a_label == player_b_label:
    st.error("❌ Please select two different players.")
    st.stop()

pid_a = player_map[player_a_label]
pid_b = player_map[player_b_label]

# ── Fetch Stats ───────────────────────────────────────────────
stats_a_raw = cfg["stats"](pid_a)
stats_b_raw = cfg["stats"](pid_b)

if not stats_a_raw or not stats_b_raw:
    st.error("❌ Could not fetch stats for one or both players.")
    st.stop()

stats_a = stats_a_raw[0]
stats_b = stats_b_raw[0]
axes    = cfg["axes"]

vals_a = [float(stats_a.get(k, 0) or 0) for k in axes]
vals_b = [float(stats_b.get(k, 0) or 0) for k in axes]

# ── Normalize to 0–100 for radar (safe division) ─────────────
max_vals = [max(a, b, 1) for a, b in zip(vals_a, vals_b)]
norm_a   = [round(v / m * 100, 1) for v, m in zip(vals_a, max_vals)]
norm_b   = [round(v / m * 100, 1) for v, m in zip(vals_b, max_vals)]

# ── Radar Chart ───────────────────────────────────────────────
st.divider()
chart_col, stats_col = st.columns([1.4, 1])

with chart_col:
    st.subheader("Radar Comparison")

    fig = go.Figure()
    theta = axes + [axes[0]]   # close the polygon

    fig.add_trace(go.Scatterpolar(
        r=norm_a + [norm_a[0]], theta=theta,
        fill="toself",
        name=player_a_label.split(" (")[0],
        line=dict(color=cfg["color_a"], width=2),
        fillcolor=cfg["color_a"].replace(")", ",0.15)").replace("rgb", "rgba")
                 if cfg["color_a"].startswith("rgb")
                 else cfg["color_a"] + "26",   # add 15% alpha via hex
        opacity=0.9
    ))
    fig.add_trace(go.Scatterpolar(
        r=norm_b + [norm_b[0]], theta=theta,
        fill="toself",
        name=player_b_label.split(" (")[0],
        line=dict(color=cfg["color_b"], width=2),
        fillcolor=cfg["color_b"] + "26",
        opacity=0.9
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True, range=[0, 110],
                gridcolor="#252c3d", linecolor="#252c3d",
                tickfont=dict(color="#6b7a99", size=9),
                tickvals=[25, 50, 75, 100],
            ),
            angularaxis=dict(
                gridcolor="#252c3d", linecolor="#252c3d",
                tickfont=dict(color="#e8ecf4", size=12),
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#e8ecf4",
        showlegend=True,
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.15,
            xanchor="center", x=0.5,
            font=dict(size=12)
        ),
        margin=dict(t=20, b=40, l=40, r=40),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Values normalized to 0–100 relative to the higher of the two players per stat.")

with stats_col:
    st.subheader("Head-to-Head Stats")

    # Winner badge per stat
    rows = []
    for stat, va, vb in zip(axes, vals_a, vals_b):
        if va > vb:   winner = f"🟣 {player_a_label.split(' (')[0]}"
        elif vb > va: winner = f"🟢 {player_b_label.split(' (')[0]}"
        else:          winner = "🤝 Tied"
        rows.append({
            "Stat":   stat.replace("_", " "),
            player_a_label.split(" (")[0]: int(va),
            player_b_label.split(" (")[0]: int(vb),
            "Edge":  winner
        })

    cmp_df = pd.DataFrame(rows)

    def highlight_edge(val):
        if "🟣" in str(val): return "color:#a855f7;font-weight:bold"
        if "🟢" in str(val): return "color:#22c55e;font-weight:bold"
        return "color:#6b7a99"

    st.dataframe(
        cmp_df.style.map(highlight_edge, subset=["Edge"]),
        use_container_width=True, hide_index=True
    )

    # Overall edge count
    a_wins = sum(1 for r in rows if player_a_label.split(" (")[0] in r["Edge"] and "🟣" in r["Edge"])
    b_wins = sum(1 for r in rows if player_b_label.split(" (")[0] in r["Edge"] and "🟢" in r["Edge"])

    st.divider()
    if a_wins > b_wins:
        overall_winner = player_a_label.split(" (")[0]
        color = cfg["color_a"]
    elif b_wins > a_wins:
        overall_winner = player_b_label.split(" (")[0]
        color = cfg["color_b"]
    else:
        overall_winner = None

    if overall_winner:
        st.markdown(f"""
        <div style="padding:14px 18px;border-radius:10px;
        border-left:4px solid {color};
        background:rgba(108,99,255,.07);font-size:14px;font-weight:600">
            🏆 Overall Edge: {overall_winner}<br>
            <span style="font-size:12px;font-weight:400;color:#6b7a99">
            Leading in {max(a_wins,b_wins)} out of {len(axes)} stats
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="padding:14px 18px;border-radius:10px;
        border-left:4px solid #6b7a99;background:rgba(107,122,153,.07);font-size:14px">
            🤝 Perfectly even match!
        </div>""", unsafe_allow_html=True)

# ── Match History Comparison ──────────────────────────────────
st.divider()
with st.expander("📋 Full Match-by-Match History"):
    table_map = {
        "Cricket":    ("Scorecard_Cricket",    "Runs_Scored",  "Stat_ID"),
        "Football":   ("Scorecard_Football",   "Goals",        "Stat_ID"),
        "Basketball": ("Scorecard_Basketball", "Points",       "Stat_ID"),
    }
    tbl, metric, id_col = table_map[sport_choice]

    hist_a = run_query(f"SELECT {id_col} AS Match_Num, {metric} AS Score FROM {tbl} "
                       f"WHERE Player_ID={pid_a} ORDER BY {id_col}")
    hist_b = run_query(f"SELECT {id_col} AS Match_Num, {metric} AS Score FROM {tbl} "
                       f"WHERE Player_ID={pid_b} ORDER BY {id_col}")

    if hist_a or hist_b:
        max_matches = max(len(hist_a or []), len(hist_b or []))
        a_scores = [r["Score"] for r in (hist_a or [])]
        b_scores = [r["Score"] for r in (hist_b or [])]
        match_nums = list(range(1, max_matches + 1))

        import plotly.express as px
        fig2 = go.Figure()
        if a_scores:
            fig2.add_trace(go.Scatter(
                x=list(range(1, len(a_scores) + 1)), y=a_scores,
                mode="lines+markers", name=player_a_label.split(" (")[0],
                line=dict(color=cfg["color_a"], width=2),
                marker=dict(size=7, color=cfg["color_a"])
            ))
        if b_scores:
            fig2.add_trace(go.Scatter(
                x=list(range(1, len(b_scores) + 1)), y=b_scores,
                mode="lines+markers", name=player_b_label.split(" (")[0],
                line=dict(color=cfg["color_b"], width=2),
                marker=dict(size=7, color=cfg["color_b"])
            ))
        fig2.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#e8ecf4",
            xaxis=dict(title="Entry #", gridcolor="#252c3d"),
            yaxis=dict(title=metric.replace("_", " "), gridcolor="#252c3d"),
            legend=dict(orientation="h", y=1.1),
            margin=dict(t=10, b=0, l=0, r=0),
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No individual match history available.")

st.caption("ARENA SNU · Novel Feature: Player Comparison Tool · System Architect: Mudit")
