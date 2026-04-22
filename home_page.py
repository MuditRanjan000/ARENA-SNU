# home_page.py — ARENA SNU Dashboard v7 (Updated)
# SURGE 2025 · System Architect: Mudit
import streamlit as st
import time
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from db_connection import run_query, call_procedure

try:
    st.set_page_config(page_title="ARENA SNU — Dashboard", page_icon="🏆", layout="wide")
except Exception:
    pass

# ── UNIFIED CSS ───────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
/* Base */ html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background: #080c14 !important; font-family: 'DM Sans', sans-serif; color: #b0bac8; } [data-testid="stSidebar"] { background: rgba(8,12,20,0.95) !important; border-right: 1px solid rgba(255,255,255,0.06); } [data-testid="stHeader"] { background: transparent !important; } section[data-testid="stMain"] > div { background: transparent !important; } p, label, div { color: #b0bac8; font-family: 'DM Sans', sans-serif; }
/* Dividers */ hr { border: none; border-top: 1px solid rgba(255,255,255,0.07) !important; margin: 2rem 0 !important; }
/* Buttons */ div.stButton > button { background: transparent !important; color: #fff !important; font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; font-size: 0.875rem !important; border-radius: 40px !important; border: 1px solid rgba(255,255,255,0.3) !important; padding: 0.55rem 1.6rem !important; letter-spacing: 0.03em !important; transition: all 0.25s ease !important; backdrop-filter: blur(8px) !important; } div.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 32px rgba(91,82,245,0.25) !important; border-color: rgba(91,82,245,0.5) !important; } div.stButton > button[kind="primary"], div.stFormSubmitButton > button { background: linear-gradient(135deg, rgba(91,82,245,0.6), rgba(168,85,247,0.5)) !important; color: #fff !important; font-weight: 700 !important; border-radius: 50px !important; border: 1px solid rgba(168,85,247,0.4) !important; padding: 12px 32px !important; font-family: 'Rajdhani', sans-serif !important; font-size: 1rem !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; transition: all 0.3s ease !important; width: 100% !important; } div.stButton > button[kind="primary"]:hover, div.stFormSubmitButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 12px 40px rgba(91,82,245,0.5) !important; }
/* Inputs */ div[data-baseweb="select"] > div, div[data-baseweb="input"] > div input, div[data-testid="stNumberInput"] input, [data-testid="stTimeInput"] input, [data-testid="stDateInput"] input { background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 10px !important; color: #e8ecf4 !important; font-family: 'DM Sans', sans-serif !important; } div[data-baseweb="select"] svg { color: #7a8499 !important; } div[data-baseweb="popover"] { background: #0f1623 !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 12px !important; } div[data-baseweb="menu"] { background: #0f1623 !important; } div[data-baseweb="menu"] li { color: #b0bac8 !important; } div[data-baseweb="menu"] li:hover { background: rgba(255,255,255,0.07) !important; } label[data-testid="stWidgetLabel"] p, div[data-testid="stSelectbox"] label p { color: rgba(255,255,255,0.4) !important; font-size: 0.7rem !important; letter-spacing: 4px !important; text-transform: uppercase !important; font-family: 'DM Sans', sans-serif !important; font-weight: 500 !important; margin-bottom: 6px !important; }
/* Number inputs */ div[data-testid="stNumberInput"] button { background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(255,255,255,0.1) !important; color: #b0bac8 !important; border-radius: 6px !important; }
/* Form & Containers */ div[data-testid="stForm"] { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 20px !important; padding: 1.5rem !important; } div[data-testid="stDataFrame"] { background: rgba(255,255,255,0.03) !important; border-radius: 16px !important; overflow: hidden !important; border: 1px solid rgba(255,255,255,0.08) !important; } iframe[data-testid="stDataFrameResizable"] { background: transparent !important; } div[data-testid="stAlert"] { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 12px !important; color: #b0bac8 !important; font-family: 'DM Sans', sans-serif !important; } details summary { color: #b0bac8 !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.875rem !important; } details { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 14px !important; padding: 0.25rem 1rem !important; } div[data-testid="stSpinner"] p { color: #7a8499 !important; } div[data-testid="stToast"] { background: rgba(15,22,35,0.95) !important; border: 1px solid rgba(34,197,94,0.3) !important; border-radius: 14px !important; color: #e8ecf4 !important; backdrop-filter: blur(18px) !important; } .js-plotly-plot .plotly { background: transparent !important; }
/* Tabs */ [data-testid="stTabs"] [data-baseweb="tab-list"] { background: rgba(255,255,255,0.03); border-radius: 50px; padding: 4px; border: 1px solid rgba(255,255,255,0.08); gap: 4px; } [data-testid="stTabs"] [data-baseweb="tab"] { background: transparent; border-radius: 50px; color: rgba(255,255,255,0.45); font-family: 'DM Sans', sans-serif; font-weight: 500; font-size: 0.875rem; padding: 8px 20px; border: none; transition: all 0.25s; } [data-testid="stTabs"] [aria-selected="true"] { background: rgba(255,255,255,0.1) !important; color: #fff !important; border: 1px solid rgba(255,255,255,0.2) !important; } [data-testid="stTabs"] [data-baseweb="tab-highlight"], [data-testid="stTabs"] [data-baseweb="tab-border"] { background: transparent !important; }
/* Metrics */ div[data-testid="stMetric"] { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 16px !important; padding: 20px 22px !important; backdrop-filter: blur(18px) !important; } div[data-testid="stMetric"] label { color: rgba(255,255,255,0.35) !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.65rem !important; letter-spacing: 4px !important; text-transform: uppercase !important; } div[data-testid="stMetricValue"] { font-family: 'Rajdhani', sans-serif !important; font-size: 2rem !important; font-weight: 700 !important; color: #e8ecf4 !important; } div[data-testid="stMetricDelta"] { display: none !important; } footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── HERO BANNER ───────────────────────────────────────────────
st.markdown("""
<div style="padding: 2.5rem 0 1.5rem; position: relative;">
  <p style="font-family:'DM Sans',sans-serif; font-size:0.7rem; letter-spacing:5px;
     color:rgba(255,255,255,0.35); text-transform:uppercase; margin:0 0 10px">
    SURGE 2025 · SNU SPORTS FESTIVAL
  </p>
  <h1 style="font-family:'Rajdhani',sans-serif; font-size:3.4rem; font-weight:800; margin:0;
     line-height:1.0; letter-spacing:-0.02em;">
    <span style="color:#f5a623;">🏆 ARENA SNU</span>
  </h1>
  <div style="width:56px; height:3px; background:linear-gradient(90deg,#f5a623,transparent);
     border-radius:2px; margin:14px 0 16px 0;"></div>
  <p style="font-family:'DM Sans',sans-serif; color:#7a8499; font-size:0.95rem;
     margin:0 0 20px 0; max-width:560px; line-height:1.7;">
     Athletic Resource & Event Navigation Application · 
     <strong style="color:#f5a623">SURGE 2025</strong><br>
     <span style="font-size:0.85rem;">Shiv Nadar University · 3 Sports · 18 Teams · 150+ Players</span>
  </p>
  <div style="display:flex; gap:10px; flex-wrap:wrap;">
      <span style="background:rgba(168,85,247,.1); border:1px solid rgba(168,85,247,.28);
          color:#c084fc; font-family:'DM Sans',sans-serif; font-size:0.75rem; font-weight:600;
          padding:5px 16px; border-radius:20px; letter-spacing:0.04em;">🏏 Cricket</span>
      <span style="background:rgba(34,197,94,.08); border:1px solid rgba(34,197,94,.25);
          color:#4ade80; font-family:'DM Sans',sans-serif; font-size:0.75rem; font-weight:600;
          padding:5px 16px; border-radius:20px; letter-spacing:0.04em;">⚽ Football</span>
      <span style="background:rgba(249,115,22,.08); border:1px solid rgba(249,115,22,.25);
          color:#fb923c; font-family:'DM Sans',sans-serif; font-size:0.75rem; font-weight:600;
          padding:5px 16px; border-radius:20px; letter-spacing:0.04em;">🏀 Basketball</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── RBAC LOGIC ────────────────────────────────────────────────
role            = st.session_state.get("role", "viewer")
CAN_MOD_TEAMS   = role in ("admin", "organiser")
CAN_MOD_PLAYERS = role in ("admin", "manager")
CAN_REMOVE_PLAYERS = role in ("admin", "manager", "organiser")
CAN_MOD_RESULTS = role in ("admin", "organiser")

tab_labels = ["📊 Dashboard", "🏆 Match Results", "🏟️ Teams", "👤 Players"]
tabs        = st.tabs(tab_labels)
tab_dash, tab_results, tab_teams, tab_players = tabs

# ═══════════ TAB 1 — DASHBOARD ═══════════════════════════════
with tab_dash:
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # ── KPI row ───────────────────────────────────────────────
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    def q1(sql): r=run_query(sql); return r[0]["cnt"] if r else 0
    c1.metric("🏅 Sports",    q1("SELECT COUNT(*) AS cnt FROM Sports"))
    c2.metric("🏟️ Teams",     q1("SELECT COUNT(*) AS cnt FROM Teams"))
    c3.metric("👤 Players",   q1("SELECT COUNT(*) AS cnt FROM Players"))
    c4.metric("📅 Matches",   q1("SELECT COUNT(*) AS cnt FROM Matches"))
    c5.metric("✅ Done",      q1("SELECT COUNT(*) AS cnt FROM Matches WHERE Status='Completed'"))
    c6.metric("⏳ Scheduled", q1("SELECT COUNT(*) AS cnt FROM Matches WHERE Status='Scheduled'"))

    st.markdown("<div style='height:36px'></div>", unsafe_allow_html=True)

    # ── Finals strip ──────────────────────────────────────────
    finals = run_query("SELECT * FROM Finals_Overview")
    if finals:
        st.markdown("""
        <div style="margin-bottom:20px;">
            <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
                color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                TOURNAMENT
            </span>
            <h3 style="font-family:'Rajdhani',sans-serif; font-size:1.6rem; font-weight:700;
                color:#fff; margin:6px 0 0 0; line-height:1.1;">
                🏆 SURGE 2025 — Finals
            </h3>
            <div style="width:48px; height:3px; background:linear-gradient(90deg,#f5a623,transparent);
                border-radius:2px; margin-top:10px;"></div>
        </div>
        """, unsafe_allow_html=True)

        sport_colors = {"Cricket":"#a855f7","Football":"#22c55e","Basketball":"#f97316"}
        fcols = st.columns(len(finals))
        for col, f in zip(fcols, finals):
            clr = sport_colors.get(f["Sport_Name"],"#5b52f5")
            champ = f["Champion"] if f["Champion"] != "TBD" else "🔜 TBD"
            col.markdown(f"""
            <div style="padding:20px 16px; border-radius:18px; text-align:center;
                background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
                border-top: 2px solid {clr}; backdrop-filter:blur(18px);">
                <div style="font-size:1.8rem; margin-bottom:10px;">{f['Icon']}</div>
                <div style="font-family:'DM Sans',sans-serif; font-size:0.68rem; letter-spacing:4px;
                    color:{clr}; text-transform:uppercase; font-weight:600; margin-bottom:10px;">
                    {f['Sport_Name']}
                </div>
                <div style="font-family:'DM Sans',sans-serif; font-size:0.85rem; color:#e8ecf4;
                    font-weight:500;">{f['Team_A']}</div>
                <div style="font-family:'Rajdhani',sans-serif; font-size:0.8rem; color:#7a8499;
                    margin:4px 0; letter-spacing:2px;">VS</div>
                <div style="font-family:'DM Sans',sans-serif; font-size:0.85rem; color:#e8ecf4;
                    font-weight:500;">{f['Team_B']}</div>
                <div style="font-family:'DM Sans',sans-serif; font-size:0.75rem; color:#7a8499;
                    margin-top:8px;">📅 {f['Match_Date']}</div>
                {'<div style="margin-top:12px; font-family:Rajdhani,sans-serif; font-size:1rem; font-weight:700; color:#f5a623;">🏆 ' + champ + '</div>'
                 if f['Champion'] != 'TBD'
                 else '<div style="margin-top:12px; font-family:DM Sans,sans-serif; font-size:0.75rem; color:#7a8499;">Pending</div>'}
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:36px'></div>", unsafe_allow_html=True)

    # ── Standings ─────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:20px;">
        <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
            color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
            RANKINGS
        </span>
        <h3 style="font-family:'Rajdhani',sans-serif; font-size:1.6rem; font-weight:700;
            color:#fff; margin:6px 0 0 0; line-height:1.1;">
            🏆 Tournament Standings
        </h3>
        <div style="width:48px; height:3px; background:linear-gradient(90deg,#5b52f5,transparent);
            border-radius:2px; margin-top:10px;"></div>
    </div>
    """, unsafe_allow_html=True)

    pts = run_query("SELECT Team_Name,University,Sport_Name,Matches_Played,Wins,Losses,Points FROM Points_Table")
    if pts:
        df_pts = pd.DataFrame(pts)
        sport_opts = ["All Sports"] + sorted(df_pts["Sport_Name"].unique().tolist())
        col_f, _ = st.columns([1,3])
        with col_f:
            sf = st.selectbox("Filter", sport_opts, label_visibility="collapsed", key="stand_f")
        filtered = df_pts if sf == "All Sports" else df_pts[df_pts["Sport_Name"]==sf]
        if not filtered.empty:
            leader = filtered.iloc[0]
            st.markdown(f"""
            <div style="padding:18px 22px; border-radius:14px;
                border:1px solid rgba(245,166,35,0.22); background:rgba(245,166,35,0.06);
                margin-bottom:20px; display:flex; align-items:center; gap:20px; flex-wrap:wrap;">
                <div>
                    <div style="font-family:'DM Sans',sans-serif; font-size:0.68rem; letter-spacing:4px;
                        color:rgba(245,166,35,0.75); text-transform:uppercase; font-weight:500; margin-bottom:6px;">
                        CURRENT LEADER · {leader['Sport_Name']}
                    </div>
                    <div style="font-family:'Rajdhani',sans-serif; font-size:1.5rem; font-weight:800;
                        color:#fff; line-height:1;">🏆 {leader['Team_Name']}</div>
                    <div style="font-family:'DM Sans',sans-serif; font-size:0.82rem;
                        color:#7a8499; margin-top:4px;">{leader['University']}</div>
                </div>
                <div style="display:flex; gap:24px; margin-left:auto; flex-wrap:wrap;">
                    <div style="text-align:center;">
                        <div style="font-family:'Rajdhani',sans-serif; font-size:1.8rem;
                            font-weight:700; color:#fbbf24; line-height:1;">{leader['Points']}</div>
                        <div style="font-size:0.65rem; letter-spacing:3px; color:#7a8499;
                            text-transform:uppercase; margin-top:2px;">PTS</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="font-family:'Rajdhani',sans-serif; font-size:1.8rem;
                            font-weight:700; color:#4ade80; line-height:1;">{leader['Wins']}</div>
                        <div style="font-size:0.65rem; letter-spacing:3px; color:#7a8499;
                            text-transform:uppercase; margin-top:2px;">W</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="font-family:'Rajdhani',sans-serif; font-size:1.8rem;
                            font-weight:700; color:#f87171; line-height:1;">{leader['Losses']}</div>
                        <div style="font-size:0.65rem; letter-spacing:3px; color:#7a8499;
                            text-transform:uppercase; margin-top:2px;">L</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            chart_col, tbl_col = st.columns([1.6,1])
            with chart_col:
                fig = px.bar(filtered.head(12), x="Team_Name", y="Points",
                             color="University",
                             hover_data=["Wins","Losses","Matches_Played","Sport_Name"],
                             color_discrete_sequence=px.colors.qualitative.Vivid,
                             labels={"Team_Name":"Team"})
                fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                                  font_color="#e8ecf4",showlegend=False,
                                  margin=dict(t=10,b=10,l=0,r=0),
                                  font=dict(family="DM Sans"),
                                  xaxis=dict(gridcolor="#1e2d45",tickangle=-30),
                                  yaxis=dict(gridcolor="#1e2d45"))
                fig.update_traces(marker_line_width=0)
                st.plotly_chart(fig, use_container_width=True)
            with tbl_col:
                st.dataframe(
                    filtered[["Team_Name","Sport_Name","Wins","Losses","Points"]].reset_index(drop=True),
                    use_container_width=True, hide_index=True)
    else:
        st.markdown("""
        <div style="padding:32px; text-align:center; border-radius:16px;
            background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);">
            <span style="color:#7a8499; font-size:0.9rem;">Standings appear once match results are recorded.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:36px'></div>", unsafe_allow_html=True)

    # ── Schedule ──────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:20px;">
        <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
            color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
            FIXTURES
        </span>
        <h3 style="font-family:'Rajdhani',sans-serif; font-size:1.6rem; font-weight:700;
            color:#fff; margin:6px 0 0 0; line-height:1.1;">
            📅 Match Schedule
        </h3>
        <div style="width:48px; height:3px; background:linear-gradient(90deg,#3b82f6,transparent);
            border-radius:2px; margin-top:10px;"></div>
    </div>
    """, unsafe_allow_html=True)

    col_sf, _ = st.columns([1,3])
    with col_sf:
        sf2 = st.selectbox("Sport filter", ["All","Cricket","Football","Basketball"],
                           label_visibility="collapsed", key="sched_sf")
    sq = ("SELECT Sport_Icon,Sport_Name,Team_A,Team_B,Match_Date,Match_Time,"
          "Venue_Name,Stage,Status,Winner FROM Upcoming_Schedule")
    if sf2 != "All":
        sq += f" WHERE Sport_Name='{sf2}'"
    sched = run_query(sq + " LIMIT 60")
    if sched:
        sdf = pd.DataFrame(sched)
        def style_status(v):
            if v=="Completed": return "color:#4ade80;font-weight:bold"
            if v=="Scheduled": return "color:#818cf8;font-weight:bold"
            if v=="Cancelled": return "color:#f87171;font-weight:bold"
            return ""
        st.dataframe(sdf.style.map(style_status,subset=["Status"]),
                     use_container_width=True,hide_index=True)
    else:
        st.markdown("""
        <div style="padding:32px; text-align:center; border-radius:16px;
            background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);">
            <span style="color:#7a8499; font-size:0.9rem;">No matches scheduled yet.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:36px'></div>", unsafe_allow_html=True)

    # ── Awards strip ──────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:20px;">
        <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
            color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
            HONORS
        </span>
        <h3 style="font-family:'Rajdhani',sans-serif; font-size:1.6rem; font-weight:700;
            color:#fff; margin:6px 0 0 0; line-height:1.1;">
            ⭐ Live Tournament Awards
        </h3>
        <div style="width:48px; height:3px; background:linear-gradient(90deg,#f5a623,transparent);
            border-radius:2px; margin-top:10px;"></div>
    </div>
    """, unsafe_allow_html=True)

    a1,a2,a3,a4 = st.columns(4)

    def award_header(col, icon, title, sub, clr):
        col.markdown(f"""
        <div style="padding:18px 14px 12px 14px; border-radius:16px; text-align:center;
            background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
            border-top:2px solid {clr}; backdrop-filter:blur(18px); margin-bottom:12px;">
            <div style="font-size:1.6rem; margin-bottom:8px;">{icon}</div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.68rem; letter-spacing:4px;
                color:{clr}; text-transform:uppercase; font-weight:600; margin-bottom:4px;">
                {title}
            </div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.75rem; color:#7a8499;">
                {sub}
            </div>
        </div>""", unsafe_allow_html=True)

    with a1:
        award_header(a1, "🏏", "Orange Cap", "Most Runs", "#a855f7")
        r=run_query("SELECT p.Player_Name,t.Team_Name,SUM(sc.Runs_Scored) AS T FROM Scorecard_Cricket sc JOIN Players p ON sc.Player_ID=p.Player_ID JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sc.Player_ID ORDER BY T DESC LIMIT 1")
        if r: st.metric(r[0]["Player_Name"],f"{r[0]['T']} runs",r[0]["Team_Name"])
        else: st.caption("No data yet")

    with a2:
        award_header(a2, "🏏", "Purple Cap", "Most Wickets", "#5b52f5")
        r=run_query("SELECT p.Player_Name,t.Team_Name,SUM(sc.Wickets_Taken) AS T FROM Scorecard_Cricket sc JOIN Players p ON sc.Player_ID=p.Player_ID JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sc.Player_ID HAVING T>0 ORDER BY T DESC LIMIT 1")
        if r: st.metric(r[0]["Player_Name"],f"{r[0]['T']} wkts",r[0]["Team_Name"])
        else: st.caption("No data yet")

    with a3:
        award_header(a3, "⚽", "Golden Boot", "Most Goals", "#22c55e")
        r=run_query("SELECT p.Player_Name,t.Team_Name,SUM(sf.Goals) AS T FROM Scorecard_Football sf JOIN Players p ON sf.Player_ID=p.Player_ID JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sf.Player_ID ORDER BY T DESC LIMIT 1")
        if r: st.metric(r[0]["Player_Name"],f"{r[0]['T']} goals",r[0]["Team_Name"])
        else: st.caption("No data yet")

    with a4:
        award_header(a4, "🏀", "MVP", "Avg Points", "#f97316")
        r=run_query("SELECT p.Player_Name,t.Team_Name,ROUND(AVG(sb.Points),1) AS T FROM Scorecard_Basketball sb JOIN Players p ON sb.Player_ID=p.Player_ID JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sb.Player_ID ORDER BY T DESC LIMIT 1")
        if r: st.metric(r[0]["Player_Name"],f"{r[0]['T']} avg",r[0]["Team_Name"])
        else: st.caption("No data yet")


# ═══════════ TAB 2 — MATCH RESULTS ═══════════════════════════
with tab_results:
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom:16px;">
        <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
            color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
            SEARCH & FILTER
        </span>
    </div>
    """, unsafe_allow_html=True)
    res_sport = st.selectbox("Filter Results by Sport", ["All", "Cricket", "Football", "Basketball"], key="res_sf")

    if CAN_MOD_RESULTS:
        st.markdown("""
        <div style="margin:20px 0 20px 0;">
            <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
                color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                RESULTS
            </span>
            <h3 style="font-family:'Rajdhani',sans-serif; font-size:1.6rem; font-weight:700;
                color:#fff; margin:6px 0 0 0; line-height:1.1;">
                🏆 Update Match Result
            </h3>
            <div style="width:48px; height:3px; background:linear-gradient(90deg,#5b52f5,transparent);
                border-radius:2px; margin-top:10px;"></div>
        </div>

        <div style="padding:16px 20px; border-radius:14px; background:rgba(91,82,245,0.07);
            border:1px solid rgba(91,82,245,0.2); margin-bottom:28px;">
            <p style="font-family:'DM Sans',sans-serif; font-size:0.875rem; color:#b0bac8; margin:0; line-height:1.7;">
                Calls <strong style="color:#e8ecf4;">UpdateMatchResult</strong> stored procedure — full ACID transaction.
                Trigger <code style="background:rgba(255,255,255,0.08); padding:1px 6px; border-radius:4px;
                font-size:0.8rem; color:#8b85ff;">trg_match_completed</code> auto-sets Status='Completed'.
            </p>
        </div>
        """, unsafe_allow_html=True)

        scheduled = run_query("""
            SELECT m.Match_ID,
              CONCAT(sp.Sport_Name,' | ',ta.Team_Name,' vs ',tb.Team_Name,
                     '  (',m.Match_Date,')  [',m.Stage,']') AS Match_Desc,
              ta.Team_Name AS Team_A, tb.Team_Name AS Team_B,
              ta.Team_ID AS TID_A, tb.Team_ID AS TID_B
            FROM Matches m
            JOIN Sports sp ON m.Sport_ID=sp.Sport_ID
            JOIN Teams ta ON m.Team_A_ID=ta.Team_ID
            JOIN Teams tb ON m.Team_B_ID=tb.Team_ID
            WHERE m.Status='Scheduled' ORDER BY m.Match_Date
        """)
        if scheduled:
            mdict = {r["Match_Desc"]: r for r in scheduled}

            st.markdown("""
            <div style="margin-bottom:6px;">
                <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
                    color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                    MATCH
                </span>
            </div>""", unsafe_allow_html=True)

            sel = mdict[st.selectbox("Select match", list(mdict.keys()), label_visibility="collapsed", key="hp_match_sel")]
            
            mc1, mc2 = st.columns(2)
            with mc1:
                ta_score = st.text_input(f"{sel['Team_A']} Overall Score", placeholder="Optional")
            with mc2:
                tb_score = st.text_input(f"{sel['Team_B']} Overall Score", placeholder="Optional")
                
            winner_label = st.radio("Who won?", [sel["Team_A"], sel["Team_B"]], horizontal=True, key="wr")
            wid = sel["TID_A"] if winner_label == sel["Team_A"] else sel["TID_B"]

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            if st.button("🏆 Confirm & Save Result", use_container_width=True):
                with st.spinner("Updating Match..."):
                    _, err = call_procedure("UpdateMatchResult", (sel["Match_ID"], wid, ta_score if ta_score else None, tb_score if tb_score else None))
                    time.sleep(0.4)
                if err:
                    st.error(f"❌ {err}")
                else:
                    st.success(f"✅ **{winner_label}** wins! Trigger fired → Status='Completed'.")
                    st.balloons(); time.sleep(1.5); st.rerun()
        else:
            st.markdown("""
            <div style="padding:32px; text-align:center; border-radius:16px;
                background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);">
                <span style="color:#7a8499; font-size:0.9rem;">All matches are completed or none are scheduled.</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom:16px;">
        <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
            color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
            HISTORY
        </span>
        <h3 style="font-family:'Rajdhani',sans-serif; font-size:1.4rem; font-weight:700;
            color:#fff; margin:6px 0 0 0; line-height:1.1;">
            ✅ Completed Match Scores
        </h3>
        <div style="width:40px; height:2px; background:linear-gradient(90deg,#4ade80,transparent);
            border-radius:2px; margin-top:8px;"></div>
    </div>
    """, unsafe_allow_html=True)

    # Uses the new Detailed_Match_Results View which calculates inline scores
    res_query = "SELECT Sport_Name, Team_A, Team_B, Score_Line, Winner, Match_Date, Stage FROM Detailed_Match_Results"
    if res_sport != "All":
        res_query += f" WHERE Sport_Name='{res_sport}'"
    
    done = run_query(res_query + " ORDER BY Match_Date DESC")
    if done:
        st.dataframe(pd.DataFrame(done), use_container_width=True, hide_index=True)
    else:
        st.markdown("""
        <div style="padding:32px; text-align:center; border-radius:16px;
            background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);">
            <span style="color:#7a8499; font-size:0.9rem;">No completed matches found for this selection.</span>
        </div>
        """, unsafe_allow_html=True)


# ═══════════ TAB 3 — TEAMS ═══════════════════════════════════
with tab_teams:
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom:24px;">
        <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
            color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
            MANAGEMENT
        </span>
        <h3 style="font-family:'Rajdhani',sans-serif; font-size:1.6rem; font-weight:700;
            color:#fff; margin:6px 0 0 0; line-height:1.1;">
            🏟️ Team Management
        </h3>
        <div style="width:48px; height:3px; background:linear-gradient(90deg,#22c55e,transparent);
            border-radius:2px; margin-top:10px;"></div>
    </div>
    """, unsafe_allow_html=True)

    sports_list = run_query("SELECT Sport_ID,Sport_Name,Icon FROM Sports ORDER BY Sport_Name")
    sport_map   = {f"{s['Icon']} {s['Sport_Name']}": s["Sport_ID"] for s in sports_list} if sports_list else {}

    cf, cl = st.columns([1,1.4], gap="large")
    
    with cf:
        if CAN_MOD_TEAMS:
            st.markdown("""
            <div style="margin-bottom:12px;">
                <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:4px;
                    color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                    ➕ Register a New Team
                </span>
            </div>
            """, unsafe_allow_html=True)
            with st.form("add_team", clear_on_submit=True):
                tname = st.text_input("Team Name *", placeholder="e.g. DTU Warriors")
                uni   = st.text_input("University *", placeholder="e.g. Delhi Tech. University")
                sport = st.selectbox("Sport *", list(sport_map.keys()) if sport_map else ["—"])
                coach = st.text_input("Coach Name *", placeholder="e.g. Rahul Dravid")
                if st.form_submit_button("✅ Add Team", use_container_width=True):
                    if not all([tname.strip(), uni.strip(), coach.strip()]):
                        st.error("❌ All fields required.")
                    elif not sport_map:
                        st.error("❌ No sports in database.")
                    else:
                        rows = run_query(
                            "INSERT INTO Teams (Team_Name,University,Sport_ID,Coach_Name) VALUES (%s,%s,%s,%s)",
                            (tname.strip(), uni.strip(), sport_map[sport], coach.strip()), fetch=False
                        )
                        time.sleep(0.3)
                        if rows:
                            st.balloons(); st.toast(f"'{tname}' added!", icon="✅"); time.sleep(1); st.rerun()
                        else:
                            st.error("❌ Failed — team may already exist for this sport.")
        else:
            st.markdown("""
            <div style="padding:20px; border-radius:12px; background:rgba(255,255,255,0.04);
                border:1px solid rgba(255,255,255,0.08); display:flex; align-items:center; gap:10px;">
                <span style="font-size:1.2rem;">🔒</span>
                <span style="color:#7a8499; font-size:0.9rem;">Team registration is restricted to <strong>Organisers</strong> and <strong>Admins</strong>.</span>
            </div>
            """, unsafe_allow_html=True)

    with cl:
        st.markdown("""
        <div style="margin-bottom:12px;">
            <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:4px;
                color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                📋 All Teams
            </span>
        </div>
        """, unsafe_allow_html=True)
        tdata = run_query("""
            SELECT t.Team_Name, t.University, sp.Sport_Name AS Sport,
                   t.Coach_Name, t.Group_Name AS `Group`,
                   COUNT(p.Player_ID) AS Players
            FROM Teams t
            JOIN Sports sp ON t.Sport_ID=sp.Sport_ID
            LEFT JOIN Players p ON p.Team_ID=t.Team_ID
            GROUP BY t.Team_ID ORDER BY sp.Sport_Name, t.Team_Name
        """)
        if tdata:
            st.dataframe(pd.DataFrame(tdata), use_container_width=True, hide_index=True)


# ═══════════ TAB 4 — PLAYERS ═════════════════════════════════
with tab_players:
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom:24px;">
        <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
            color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
            ROSTER
        </span>
        <h3 style="font-family:'Rajdhani',sans-serif; font-size:1.6rem; font-weight:700;
            color:#fff; margin:6px 0 0 0; line-height:1.1;">
            👤 Player Management
        </h3>
        <div style="width:48px; height:3px; background:linear-gradient(90deg,#a855f7,transparent);
            border-radius:2px; margin-top:10px;"></div>
    </div>
    """, unsafe_allow_html=True)

    all_teams = run_query("""
        SELECT t.Team_ID,t.Team_Name,t.University,sp.Sport_Name,sp.Icon
        FROM Teams t JOIN Sports sp ON t.Sport_ID=sp.Sport_ID
        ORDER BY sp.Sport_Name, t.Team_Name
    """)
    team_map = {
        f"{t['Icon']} {t['Team_Name']} ({t['University']})": t["Team_ID"]
        for t in all_teams
    } if all_teams else {}

    pf, pl = st.columns([1,1.4], gap="large")
    
    with pf:
        if CAN_MOD_PLAYERS:
            st.markdown("""
            <div style="margin-bottom:12px;">
                <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:4px;
                    color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                    ➕ Register a Player
                </span>
            </div>
            """, unsafe_allow_html=True)
            with st.form("add_player", clear_on_submit=True):
                pname  = st.text_input("Player Name *", placeholder="e.g. Arjun Mehta")
                tsel   = st.selectbox("Team *", list(team_map.keys()) if team_map else ["—"])
                prole  = st.text_input("Role *", placeholder="e.g. Batsman, Striker, Guard")
                jersey = st.number_input("Jersey No *", min_value=1, max_value=99, value=10)
                if st.form_submit_button("✅ Register Player", use_container_width=True):
                    if not pname.strip() or not prole.strip():
                        st.error("❌ Name and role required.")
                    elif not team_map:
                        st.error("❌ No teams yet.")
                    else:
                        _, err = call_procedure(
                            "RegisterPlayer", (pname.strip(), team_map[tsel], prole.strip(), int(jersey))
                        )
                        time.sleep(0.3)
                        if err:
                            if "jersey" in err.lower():
                                st.error(f"❌ Jersey #{jersey} already taken. Pick another.")
                            else:
                                st.error(f"❌ {err}")
                        else:
                            st.toast(f"{pname} registered!", icon="✅"); time.sleep(1); st.rerun()
        else:
            st.markdown("""
            <div style="padding:20px; border-radius:12px; background:rgba(255,255,255,0.04);
                border:1px solid rgba(255,255,255,0.08); display:flex; align-items:center; gap:10px;">
                <span style="font-size:1.2rem;">🔒</span>
                <span style="color:#7a8499; font-size:0.9rem;">Player registration is restricted to <strong>Managers</strong> and <strong>Admins</strong>.</span>
            </div>
            """, unsafe_allow_html=True)
            
        if CAN_REMOVE_PLAYERS:
            st.markdown("""
            <div style="margin-top:32px; margin-bottom:12px;">
                <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:4px;
                    color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                    🗑️ Remove a Player
                </span>
            </div>
            """, unsafe_allow_html=True)
            all_players_del = run_query("SELECT p.Player_ID, p.Player_Name, t.Team_Name FROM Players p JOIN Teams t ON p.Team_ID = t.Team_ID ORDER BY p.Player_Name")
            if all_players_del:
                del_map = {f"{p['Player_Name']} ({p['Team_Name']})": p["Player_ID"] for p in all_players_del}
                with st.form("remove_player", clear_on_submit=True):
                    del_sel = st.selectbox("Select Player to Remove", list(del_map.keys()))
                    if st.form_submit_button("🗑️ Delete Player", use_container_width=True):
                        try:
                            # Try deleting the player. Will fail if foreign key constraints are violated.
                            run_query("DELETE FROM Players WHERE Player_ID=%s", (del_map[del_sel],), fetch=False)
                            st.toast(f"Player removed!", icon="✅")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error("❌ Cannot delete this player. They likely have recorded match scores or predictions.")
            else:
                st.caption("No players available to remove.")

    with pl:
        st.markdown("""
        <div style="margin-bottom:12px;">
            <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:4px;
                color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                📋 All Players
            </span>
        </div>
        """, unsafe_allow_html=True)
        sf3 = st.selectbox("Sport filter",
                           ["All"]+[s["Sport_Name"] for s in (sports_list or [])],
                           key="plist_sf", label_visibility="collapsed")
        pq = """SELECT p.Player_Name,t.Team_Name,sp.Sport_Name AS Sport,
                       p.Role,p.Jersey_No AS Jersey,p.Form_Status
                FROM Players p JOIN Teams t ON p.Team_ID=t.Team_ID
                JOIN Sports sp ON t.Sport_ID=sp.Sport_ID"""
        if sf3 != "All":
            pq += f" WHERE sp.Sport_Name='{sf3}'"
        pq += " ORDER BY sp.Sport_Name,t.Team_Name,p.Player_Name"
        pdata = run_query(pq)
        if pdata:
            pdf = pd.DataFrame(pdata)
            def color_form(v):
                if v=="In Form":     return "color:#4ade80;font-weight:bold"
                if v=="Out of Form": return "color:#f87171;font-weight:bold"
                return "color:#4a5568"
            st.dataframe(pdf.style.map(color_form,subset=["Form_Status"]),
                         use_container_width=True,hide_index=True)
        else:
            st.markdown("""
            <div style="padding:32px; text-align:center; border-radius:16px;
                background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);">
                <span style="color:#7a8499; font-size:0.9rem;">No players yet.</span>
            </div>
            """, unsafe_allow_html=True)