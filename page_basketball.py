# page_basketball.py — ARENA SNU Basketball Module v7
# SURGE 2025 · Assigned: Amitog · Reviewed: Mudit
import streamlit as st, time, pandas as pd
import plotly.express as px
from db_connection import run_query

try: st.set_page_config(page_title="Basketball — ARENA SNU", page_icon="🏀", layout="wide")
except: pass

# ── UNIFIED CSS ───────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
/* Base */ html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background: #080c14 !important; font-family: 'DM Sans', sans-serif; color: #b0bac8; } [data-testid="stSidebar"] { background: rgba(8,12,20,0.95) !important; border-right: 1px solid rgba(255,255,255,0.06); } [data-testid="stHeader"] { background: transparent !important; } section[data-testid="stMain"] > div { background: transparent !important; } p, label, div { color: #b0bac8; font-family: 'DM Sans', sans-serif; }
/* Dividers */ hr { border: none; border-top: 1px solid rgba(255,255,255,0.07) !important; margin: 2rem 0 !important; }
/* Buttons */ div.stButton > button { background: transparent !important; color: #fff !important; font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; font-size: 0.875rem !important; border-radius: 40px !important; border: 1px solid rgba(255,255,255,0.3) !important; padding: 0.55rem 1.6rem !important; letter-spacing: 0.03em !important; transition: all 0.25s ease !important; backdrop-filter: blur(8px) !important; } div.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 32px rgba(249,115,22,0.25) !important; border-color: rgba(249,115,22,0.5) !important; } div.stButton > button[kind="primary"], div.stFormSubmitButton > button { background: linear-gradient(135deg, rgba(249,115,22,0.6), rgba(91,82,245,0.5)) !important; color: #fff !important; font-weight: 700 !important; border-radius: 50px !important; border: 1px solid rgba(249,115,22,0.4) !important; padding: 12px 32px !important; font-family: 'Rajdhani', sans-serif !important; font-size: 1rem !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; transition: all 0.3s ease !important; width: 100% !important; } div.stButton > button[kind="primary"]:hover, div.stFormSubmitButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 12px 40px rgba(249,115,22,0.5) !important; }
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
    <p style="font-family:'DM Sans',sans-serif; font-size:0.7rem; letter-spacing:5px;
        color:rgba(255,255,255,0.35); text-transform:uppercase; margin:0 0 10px">
        SURGE 2025 · 5-ON-5
    </p>
    <h1 style="font-family:'Rajdhani',sans-serif; font-size:3rem; font-weight:800; margin:0;
        line-height:1.0; color:#fff; letter-spacing:-0.01em;">
        🏀 Basketball <span style="background:linear-gradient(90deg,#f97316,#5b52f5);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Module</span>
    </h1>
    <div style="width:52px; height:3px; background:linear-gradient(90deg,#f97316,transparent);
        border-radius:2px; margin:14px 0 12px 0;"></div>
    <p style="font-family:'DM Sans',sans-serif; color:#7a8499; font-size:0.95rem;
        margin:0; line-height:1.7;">
        Score entry · MVP leaderboard · Team stats & charts
    </p>
</div>
""", unsafe_allow_html=True)

role      = st.session_state.get("role","viewer")
CAN_ENTER = role in ("admin","organiser")
tab_entry, tab_lb, tab_chart = st.tabs(["📝 Enter Stats","📊 Leaderboard","📈 Team Charts"])

# ── ENTRY ─────────────────────────────────────────────────────
with tab_entry:
    if not CAN_ENTER:
        st.markdown("""
        <div style="padding:24px 28px; border-radius:16px; background:rgba(255,255,255,0.04);
            border:1px solid rgba(255,255,255,0.09); margin-top:24px; display:flex;
            align-items:center; gap:14px;">
            <span style="font-size:1.5rem;">🔒</span>
            <div>
                <div style="font-family:'Rajdhani',sans-serif; font-size:1rem; font-weight:700;
                    color:#e8ecf4; margin-bottom:4px;">Access Restricted</div>
                <div style="font-family:'DM Sans',sans-serif; font-size:0.875rem; color:#7a8499;">
                    Score entry is restricted to <strong style="color:#b0bac8;">Organisers</strong> and Admins.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

        matches = run_query("""
            SELECT m.Match_ID,
                   CONCAT(ta.Team_Name,' vs ',tb.Team_Name,'  (',m.Match_Date,')  [',m.Stage,']') AS Match_Desc,
                   m.Team_A_ID, m.Team_B_ID
            FROM Matches m JOIN Teams ta ON m.Team_A_ID=ta.Team_ID JOIN Teams tb ON m.Team_B_ID=tb.Team_ID
            WHERE m.Sport_ID=3 ORDER BY m.Match_Date DESC
        """)
        if not matches:
            st.warning("⚠️ No basketball matches found.")
        else:
            md = {r["Match_Desc"]: r for r in matches}

            st.markdown("""
            <div style="margin-bottom:6px;">
                <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
                    color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                    MATCH SELECTION
                </span>
            </div>""", unsafe_allow_html=True)

            sel = md[st.selectbox("Select Match", list(md.keys()), label_visibility="collapsed", key="bb_match_sel")]
            mid = sel["Match_ID"]

            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

            players = run_query("""
                SELECT p.Player_ID,CONCAT(p.Player_Name,'  (',t.Team_Name,')  — ',p.Role) AS PDesc
                FROM Players p JOIN Teams t ON p.Team_ID=t.Team_ID
                WHERE p.Team_ID IN (%s,%s) ORDER BY t.Team_Name, p.Player_Name
            """, (sel["Team_A_ID"], sel["Team_B_ID"]))
            if not players:
                st.warning("⚠️ No players found.")
            else:
                pd2 = {r["PDesc"]: r["Player_ID"] for r in players}

                st.markdown("""
                <div style="margin-bottom:6px;">
                    <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
                        color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                        PLAYER
                    </span>
                </div>""", unsafe_allow_html=True)

                pid = pd2[st.selectbox("Select Player", list(pd2.keys()), label_visibility="collapsed", key="bb_player_sel")]

                ex = run_query("SELECT COUNT(*) AS c FROM Scorecard_Basketball WHERE Match_ID=%s AND Player_ID=%s",
                               (mid,pid))
                if ex and ex[0]["c"] > 0:
                    st.markdown("""
                    <div style="margin:16px 0; padding:14px 18px; border-radius:12px;
                        background:rgba(249,115,22,0.08); border:1px solid rgba(249,115,22,0.2);">
                        <span style="font-family:'DM Sans',sans-serif; font-size:0.84rem; color:#fdba74;">
                            ⚠️ Entry exists for this player/match. Submitting adds another record.
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

                with st.form("bball_form", clear_on_submit=True):
                    st.markdown("""
                    <div style="margin-bottom:20px;">
                        <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
                            color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                            PLAYER STATS ENTRY
                        </span>
                        <div style="width:40px; height:2px; background:linear-gradient(90deg,#f97316,transparent);
                            border-radius:2px; margin-top:8px;"></div>
                    </div>
                    """, unsafe_allow_html=True)
                    c1,c2 = st.columns(2)
                    with c1:
                        pts = st.number_input("Points",   min_value=0, max_value=100, key="bb_pts")
                        reb = st.number_input("Rebounds", min_value=0, max_value=50,  key="bb_reb")
                    with c2:
                        ast = st.number_input("Assists",  min_value=0, max_value=30,  key="bb_ast")
                        stl = st.number_input("Steals",   min_value=0, max_value=20,  key="bb_stl")
                    if st.form_submit_button("🏀 Submit Stats", use_container_width=True):
                        with st.spinner("Writing to MySQL…"):
                            run_query(
                                "INSERT INTO Scorecard_Basketball "
                                "(Match_ID,Player_ID,Points,Rebounds,Assists,Steals) "
                                "VALUES (%s,%s,%s,%s,%s,%s)",
                                (mid,pid,pts,reb,ast,stl), fetch=False
                            )
                            time.sleep(0.4)
                        st.toast("Stats recorded!", icon="✅"); time.sleep(1); st.rerun()

            st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
            
            # --- MATCH RESULT ENTRY ---
            st.markdown("""
            <div style="margin-bottom:20px;">
                <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
                    color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                    MATCH RESULT ENTRY
                </span>
                <div style="width:40px; height:2px; background:linear-gradient(90deg,#f97316,transparent);
                    border-radius:2px; margin-top:8px;"></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Get Team Names
            team_a_name = run_query("SELECT Team_Name FROM Teams WHERE Team_ID=%s", (sel["Team_A_ID"],))[0]["Team_Name"]
            team_b_name = run_query("SELECT Team_Name FROM Teams WHERE Team_ID=%s", (sel["Team_B_ID"],))[0]["Team_Name"]
            
            with st.form("basketball_match_result", clear_on_submit=True):
                mc1, mc2 = st.columns(2)
                with mc1:
                    ta_score = st.text_input(f"{team_a_name} Overall Score", placeholder="e.g. 78")
                with mc2:
                    tb_score = st.text_input(f"{team_b_name} Overall Score", placeholder="e.g. 61")
                
                winner_label = st.radio("Who won?", [team_a_name, team_b_name], horizontal=True)
                wid = sel["Team_A_ID"] if winner_label == team_a_name else sel["Team_B_ID"]
                
                sub_res = st.form_submit_button("🏆 Update Match Result", use_container_width=True)
                
            if sub_res:
                with st.spinner("Updating match result…"):
                    from db_connection import call_procedure
                    _, err = call_procedure("UpdateMatchResult", (mid, wid, ta_score if ta_score else None, tb_score if tb_score else None))
                    time.sleep(0.4)
                if err:
                    st.error(f"❌ {err}")
                else:
                    st.success(f"✅ Match {mid} completed! Winner: {winner_label}")
                    st.balloons(); time.sleep(1.5); st.rerun()

# ── LEADERBOARD ────────────────────────────────────────────────
with tab_lb:
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    if not CAN_ENTER:
        st.markdown("""
        <div style="padding:12px 18px; border-radius:12px; background:rgba(255,255,255,0.04);
            border:1px solid rgba(255,255,255,0.09); margin-bottom:24px; display:inline-flex;
            align-items:center; gap:10px;">
            <span style="color:#7a8499; font-size:0.85rem; font-family:'DM Sans',sans-serif;">
                🔒 Score entry restricted to Organisers
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom:20px;">
        <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
            color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
            RANKINGS
        </span>
        <h3 style="font-family:'Rajdhani',sans-serif; font-size:1.6rem; font-weight:700;
            color:#fff; margin:6px 0 0 0; line-height:1.1;">
            🏀 MVP Leaderboard
        </h3>
        <div style="width:48px; height:3px; background:linear-gradient(90deg,#f97316,transparent);
            border-radius:2px; margin-top:10px;"></div>
    </div>
    """, unsafe_allow_html=True)

    data = run_query("""
        SELECT p.Player_Name, t.Team_Name,
               SUM(sb.Points) AS Total_Points, SUM(sb.Rebounds) AS Total_Rebounds,
               SUM(sb.Assists) AS Total_Assists, SUM(sb.Steals) AS Total_Steals,
               ROUND(AVG(sb.Points),1) AS Avg_Points, COUNT(DISTINCT sb.Match_ID) AS Games
        FROM Scorecard_Basketball sb JOIN Players p ON sb.Player_ID=p.Player_ID
        JOIN Teams t ON p.Team_ID=t.Team_ID
        GROUP BY sb.Player_ID ORDER BY Total_Points DESC
    """)
    if not data:
        st.markdown("""
        <div style="padding:40px; text-align:center; border-radius:16px;
            background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);">
            <span style="color:#7a8499; font-size:0.9rem;">No basketball data yet</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        df=pd.DataFrame(data); df.insert(0,"Rank",range(1,len(df)+1))
        mvp=df.iloc[0]
        st.markdown(f"""
        <div style="padding:20px 24px; border-radius:16px; border:1px solid rgba(249,115,22,0.25);
            background: rgba(249,115,22,0.07); margin-bottom:20px;
            backdrop-filter: blur(18px);">
            <div style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
                color:rgba(249,115,22,0.75); text-transform:uppercase; font-weight:500; margin-bottom:10px;">
                CURRENT MVP
            </div>
            <div style="display:flex; align-items:center; gap:20px; flex-wrap:wrap;">
                <div>
                    <div style="font-family:'Rajdhani',sans-serif; font-size:1.9rem; font-weight:800;
                        color:#fff; line-height:1;">🏀 {mvp['Player_Name']}</div>
                    <div style="font-family:'DM Sans',sans-serif; font-size:0.85rem; color:#7a8499;
                        margin-top:4px;">{mvp['Team_Name']}</div>
                </div>
                <div style="display:flex; gap:28px; margin-left:auto; flex-wrap:wrap;">
                    <div style="text-align:center;">
                        <div style="font-family:'Rajdhani',sans-serif; font-size:2rem;
                            font-weight:700; color:#fdba74; line-height:1;">{mvp['Total_Points']}</div>
                        <div style="font-size:0.65rem; letter-spacing:4px; color:#7a8499;
                            text-transform:uppercase; margin-top:2px;">PTS</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="font-family:'Rajdhani',sans-serif; font-size:2rem;
                            font-weight:700; color:#fdba74; line-height:1;">{mvp['Avg_Points']}</div>
                        <div style="font-size:0.65rem; letter-spacing:4px; color:#7a8499;
                            text-transform:uppercase; margin-top:2px;">AVG</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="font-family:'Rajdhani',sans-serif; font-size:2rem;
                            font-weight:700; color:#fdba74; line-height:1;">{mvp['Games']}</div>
                        <div style="font-size:0.65rem; letter-spacing:4px; color:#7a8499;
                            text-transform:uppercase; margin-top:2px;">GAMES</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        def hl(r): return ["background:rgba(249,115,22,.1)"]*len(r) if r["Rank"]==1 else [""]*len(r)
        st.dataframe(df.style.apply(hl,axis=1),use_container_width=True,hide_index=True)

# ── TEAM CHARTS ───────────────────────────────────────────────
with tab_chart:
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom:20px;">
        <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
            color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
            ANALYTICS
        </span>
        <h3 style="font-family:'Rajdhani',sans-serif; font-size:1.6rem; font-weight:700;
            color:#fff; margin:6px 0 0 0; line-height:1.1;">
            📈 Player & Team Charts
        </h3>
        <div style="width:48px; height:3px; background:linear-gradient(90deg,#5b52f5,transparent);
            border-radius:2px; margin-top:10px;"></div>
    </div>
    """, unsafe_allow_html=True)

    data2 = run_query("""
        SELECT p.Player_Name, t.Team_Name,
               SUM(sb.Points) AS Points, SUM(sb.Rebounds) AS Rebounds,
               SUM(sb.Assists) AS Assists, SUM(sb.Steals) AS Steals
        FROM Scorecard_Basketball sb JOIN Players p ON sb.Player_ID=p.Player_ID
        JOIN Teams t ON p.Team_ID=t.Team_ID
        GROUP BY sb.Player_ID ORDER BY Points DESC
    """)
    if data2:
        df3=pd.DataFrame(data2)
        fig=px.bar(df3.head(12), x="Player_Name",
                   y=["Points","Rebounds","Assists","Steals"],
                   barmode="group",
                   color_discrete_sequence=["#f97316","#5b52f5","#a855f7","#22c55e"],
                   labels={"Player_Name":"Player","value":"Count","variable":"Stat"},
                   title="Top Players — All Stats")
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                          font_color="#e8ecf4",margin=dict(t=36,b=0,l=0,r=0),
                          font=dict(family="DM Sans"),
                          title_font=dict(family="Rajdhani", size=16),
                          xaxis=dict(gridcolor="#1e2d45"),yaxis=dict(gridcolor="#1e2d45"),
                          legend=dict(orientation="h",y=1.1))
        st.plotly_chart(fig,use_container_width=True)

        # Team totals
        team_totals = run_query("""
            SELECT t.Team_Name,SUM(sb.Points) AS Points,SUM(sb.Rebounds) AS Rebounds,
                   SUM(sb.Assists) AS Assists
            FROM Scorecard_Basketball sb JOIN Players p ON sb.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY p.Team_ID ORDER BY Points DESC
        """)
        if team_totals:
            st.markdown("""
            <div style="margin:32px 0 16px 0;">
                <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
                    color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                    TEAM COMPARISON
                </span>
                <div style="width:48px; height:2px; background:linear-gradient(90deg,#f97316,transparent);
                    border-radius:2px; margin-top:8px;"></div>
            </div>
            """, unsafe_allow_html=True)
            fig2=px.bar(pd.DataFrame(team_totals), x="Team_Name",
                        y=["Points","Rebounds","Assists"], barmode="group",
                        color_discrete_sequence=["#f97316","#5b52f5","#a855f7"],
                        title="Team Comparison")
            fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                               font_color="#e8ecf4",margin=dict(t=36,b=0,l=0,r=0),
                               font=dict(family="DM Sans"),
                               title_font=dict(family="Rajdhani", size=16),
                               xaxis=dict(gridcolor="#1e2d45"),yaxis=dict(gridcolor="#1e2d45"))
            st.plotly_chart(fig2,use_container_width=True)
    else:
        st.markdown("""
        <div style="padding:40px; text-align:center; border-radius:16px;
            background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);">
            <span style="color:#7a8499; font-size:0.9rem;">No basketball data yet</span>
        </div>
        """, unsafe_allow_html=True)