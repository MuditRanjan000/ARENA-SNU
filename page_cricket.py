# page_cricket.py — ARENA SNU Cricket Module v7
# SURGE 2025 · Assigned: Ashank · Reviewed: Mudit
import streamlit as st, time, pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db_connection import run_query

try: st.set_page_config(page_title="Cricket — ARENA SNU", page_icon="🏏", layout="wide")
except: pass

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

# ── HERO HEADER ───────────────────────────────────────────────
st.markdown("""
<div style="padding: 2.5rem 0 1rem; position: relative;">
    <p style="font-family:'DM Sans',sans-serif; font-size:0.7rem; letter-spacing:5px;
        color:rgba(255,255,255,0.35); text-transform:uppercase; margin:0 0 10px">
        SURGE 2025 · T20 FORMAT
    </p>
    <h1 style="font-family:'Rajdhani',sans-serif; font-size:3rem; font-weight:800; margin:0;
        line-height:1.0; color:#fff; letter-spacing:-0.01em;">
        🏏 Cricket <span style="background:linear-gradient(90deg,#a855f7,#5b52f5);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Module</span>
    </h1>
    <div style="width:52px; height:3px; background:linear-gradient(90deg,#a855f7,transparent);
        border-radius:2px; margin:14px 0 12px 0;"></div>
    <p style="font-family:'DM Sans',sans-serif; color:#7a8499; font-size:0.95rem;
        margin:0; line-height:1.7;">
        Score entry · Orange & Purple Cap leaderboards · Player form tracking
    </p>
</div>
""", unsafe_allow_html=True)

role      = st.session_state.get("role","viewer")
CAN_ENTER = role in ("admin","organiser")
tab_entry, tab_boards, tab_form = st.tabs(["📝 Enter Score","📊 Leaderboards","🔥 Player Form"])

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
                   CONCAT(ta.Team_Name,' vs ',tb.Team_Name,' (',m.Match_Date,') [',m.Stage,']') AS Match_Desc,
                   m.Team_A_ID, m.Team_B_ID
            FROM Matches m
            JOIN Teams ta ON m.Team_A_ID=ta.Team_ID JOIN Teams tb ON m.Team_B_ID=tb.Team_ID
            WHERE m.Sport_ID=1 AND m.Status='Scheduled' ORDER BY m.Match_Date
        """)
        if not matches:
            st.warning("⚠️ No scheduled cricket matches found. Schedule one first.")
        else:
            md = {r["Match_Desc"]: r for r in matches}

            st.markdown("""
            <div style="margin-bottom:6px;">
                <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
                    color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                    MATCH SELECTION
                </span>
            </div>""", unsafe_allow_html=True)

            sel = md[st.selectbox("Select Match", list(md.keys()), label_visibility="collapsed", key="cr_match_sel")]
            mid = sel["Match_ID"]

            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

            players = run_query("""
                SELECT p.Player_ID,
                       CONCAT(p.Player_Name,'  (',t.Team_Name,')  — ',p.Role) AS PDesc
                FROM Players p JOIN Teams t ON p.Team_ID=t.Team_ID
                WHERE p.Team_ID IN (%s,%s) ORDER BY t.Team_Name, p.Player_Name
            """, (sel["Team_A_ID"], sel["Team_B_ID"]))
            if not players:
                st.warning("⚠️ No players for these teams.")
            else:
                pd2 = {r["PDesc"]: r["Player_ID"] for r in players}

                st.markdown("""
                <div style="margin-bottom:6px;">
                    <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
                        color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                        PLAYER
                    </span>
                </div>""", unsafe_allow_html=True)

                pid = pd2[st.selectbox("Select Player", list(pd2.keys()), label_visibility="collapsed", key="cr_player_sel")]

                ex = run_query("SELECT Runs_Scored,Wickets_Taken,Overs_Bowled,Catches "
                               "FROM Scorecard_Cricket WHERE Match_ID=%s AND Player_ID=%s",
                               (mid, pid))
                if ex:
                    e=ex[0]
                    st.markdown(f"""
                    <div style="margin: 20px 0; padding:16px 20px; border-radius:14px;
                        background:rgba(168,85,247,0.08); border:1px solid rgba(168,85,247,0.2);">
                        <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:4px;
                            color:rgba(168,85,247,0.8); text-transform:uppercase; font-weight:500;">
                            EXISTING ENTRY
                        </span>
                        <div style="display:flex; gap:32px; margin-top:12px; flex-wrap:wrap;">
                            <div><div style="font-family:'Rajdhani',sans-serif; font-size:1.8rem;
                                font-weight:700; color:#e8ecf4; line-height:1;">{e['Runs_Scored']}</div>
                                <div style="font-size:0.72rem; letter-spacing:3px; color:#7a8499;
                                text-transform:uppercase; margin-top:2px;">RUNS</div></div>
                            <div><div style="font-family:'Rajdhani',sans-serif; font-size:1.8rem;
                                font-weight:700; color:#e8ecf4; line-height:1;">{e['Wickets_Taken']}</div>
                                <div style="font-size:0.72rem; letter-spacing:3px; color:#7a8499;
                                text-transform:uppercase; margin-top:2px;">WICKETS</div></div>
                            <div><div style="font-family:'Rajdhani',sans-serif; font-size:1.8rem;
                                font-weight:700; color:#e8ecf4; line-height:1;">{e['Overs_Bowled']}</div>
                                <div style="font-size:0.72rem; letter-spacing:3px; color:#7a8499;
                                text-transform:uppercase; margin-top:2px;">OVERS</div></div>
                            <div><div style="font-family:'Rajdhani',sans-serif; font-size:1.8rem;
                                font-weight:700; color:#e8ecf4; line-height:1;">{e['Catches']}</div>
                                <div style="font-size:0.72rem; letter-spacing:3px; color:#7a8499;
                                text-transform:uppercase; margin-top:2px;">CATCHES</div></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

                with st.form("cricket_form", clear_on_submit=True):
                    st.markdown("""
                    <div style="margin-bottom:20px;">
                        <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
                            color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                            SCORECARD ENTRY
                        </span>
                        <div style="width:40px; height:2px; background:linear-gradient(90deg,#a855f7,transparent);
                            border-radius:2px; margin-top:8px;"></div>
                    </div>
                    """, unsafe_allow_html=True)
                    c1,c2 = st.columns(2)
                    with c1:
                        runs    = st.number_input("Runs Scored",   min_value=0, max_value=200,              key="cr_runs")
                        wickets = st.number_input("Wickets Taken", min_value=0, max_value=10,               key="cr_wkts")
                    with c2:
                        overs   = st.number_input("Overs Bowled",  min_value=0.0, max_value=20.0, step=0.1, key="cr_overs")
                        catches = st.number_input("Catches",        min_value=0, max_value=10,              key="cr_ctch")
                    sub = st.form_submit_button("🏏 Submit Score", use_container_width=True)

                if sub:
                    if round(overs % 1, 1) > 0.5:
                        st.error("❌ Invalid overs — decimal must be 0–5 (e.g. 3.4, not 3.7)")
                    else:
                        with st.spinner("Writing to MySQL…"):
                            run_query(
                                "INSERT INTO Scorecard_Cricket "
                                "(Match_ID,Player_ID,Runs_Scored,Wickets_Taken,Overs_Bowled,Catches) "
                                "VALUES (%s,%s,%s,%s,%s,%s)",
                                (mid,pid,runs,wickets,overs,catches), fetch=False
                            )
                            time.sleep(0.4)
                        st.toast("Score recorded! trg_player_form fired.", icon="✅")
                        time.sleep(1); st.rerun()
            
            st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
            
            # --- MATCH RESULT ENTRY ---
            st.markdown("""
            <div style="margin-bottom:20px;">
                <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
                    color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                    MATCH RESULT ENTRY
                </span>
                <div style="width:40px; height:2px; background:linear-gradient(90deg,#a855f7,transparent);
                    border-radius:2px; margin-top:8px;"></div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("cricket_match_result", clear_on_submit=True):
                mc1, mc2 = st.columns(2)
                with mc1:
                    ta_score = st.text_input(f"{sel.get('Team_A', 'Team A')} Overall Score", placeholder="e.g. 174/6")
                with mc2:
                    tb_score = st.text_input(f"{sel.get('Team_B', 'Team B')} Overall Score", placeholder="e.g. 149/10")
                
                winner_label = st.radio("Who won?", [sel.get("Team_A", "Team A"), sel.get("Team_B", "Team B")], horizontal=True)
                wid = sel["Team_A_ID"] if winner_label == sel.get("Team_A", "Team A") else sel["Team_B_ID"]
                
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

# ── LEADERBOARDS ──────────────────────────────────────────────
with tab_boards:
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

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown("""
        <div style="margin-bottom:20px;">
            <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
                color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                BATTING
            </span>
            <h3 style="font-family:'Rajdhani',sans-serif; font-size:1.6rem; font-weight:700;
                color:#fff; margin:6px 0 0 0; line-height:1.1;">
                🏅 Orange Cap
            </h3>
            <div style="width:48px; height:3px; background:linear-gradient(90deg,#f97316,transparent);
                border-radius:2px; margin-top:10px;"></div>
        </div>
        """, unsafe_allow_html=True)

        oc = run_query("""
            SELECT p.Player_Name,t.Team_Name,t.University,
                   SUM(sc.Runs_Scored) AS Runs, COUNT(DISTINCT sc.Match_ID) AS Innings
            FROM Scorecard_Cricket sc JOIN Players p ON sc.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sc.Player_ID ORDER BY Runs DESC
        """)
        if oc:
            df=pd.DataFrame(oc); df.insert(0,"Rank",range(1,len(df)+1))
            def hl(r): return ["background:rgba(168,85,247,.12)"]*len(r) if r["Rank"]==1 else [""]*len(r)
            st.dataframe(df.style.apply(hl,axis=1),use_container_width=True,hide_index=True)
            fig=px.bar(df.head(8),x="Player_Name",y="Runs",color="Team_Name",
                       color_discrete_sequence=px.colors.qualitative.Vivid,
                       title="Top Run Scorers")
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                              font_color="#e8ecf4",showlegend=False,
                              margin=dict(t=36,b=0,l=0,r=0),
                              font=dict(family="DM Sans"),
                              title_font=dict(family="Rajdhani", size=16),
                              xaxis=dict(gridcolor="#1e2d45"),yaxis=dict(gridcolor="#1e2d45"))
            st.plotly_chart(fig,use_container_width=True)
        else:
            st.markdown("""
            <div style="padding:32px; text-align:center; border-radius:16px;
                background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);">
                <span style="color:#7a8499; font-size:0.9rem;">No batting data yet</span>
            </div>
            """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div style="margin-bottom:20px;">
            <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
                color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                BOWLING
            </span>
            <h3 style="font-family:'Rajdhani',sans-serif; font-size:1.6rem; font-weight:700;
                color:#fff; margin:6px 0 0 0; line-height:1.1;">
                💜 Purple Cap
            </h3>
            <div style="width:48px; height:3px; background:linear-gradient(90deg,#a855f7,transparent);
                border-radius:2px; margin-top:10px;"></div>
        </div>
        """, unsafe_allow_html=True)

        pc = run_query("""
            SELECT p.Player_Name,t.Team_Name,SUM(sc.Wickets_Taken) AS Wickets,
                   ROUND(SUM(sc.Overs_Bowled),1) AS Overs
            FROM Scorecard_Cricket sc JOIN Players p ON sc.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID
            GROUP BY sc.Player_ID HAVING Wickets>0 ORDER BY Wickets DESC
        """)
        if pc:
            df2=pd.DataFrame(pc); df2.insert(0,"Rank",range(1,len(df2)+1))
            def hl2(r): return ["background:rgba(91,82,245,.12)"]*len(r) if r["Rank"]==1 else [""]*len(r)
            st.dataframe(df2.style.apply(hl2,axis=1),use_container_width=True,hide_index=True)
            fig2=px.bar(df2.head(8),x="Player_Name",y="Wickets",
                        color_discrete_sequence=["#a855f7"],title="Top Wicket Takers")
            fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                               font_color="#e8ecf4",showlegend=False,
                               margin=dict(t=36,b=0,l=0,r=0),
                               font=dict(family="DM Sans"),
                               title_font=dict(family="Rajdhani", size=16),
                               xaxis=dict(gridcolor="#1e2d45"),yaxis=dict(gridcolor="#1e2d45"))
            st.plotly_chart(fig2,use_container_width=True)
        else:
            st.markdown("""
            <div style="padding:32px; text-align:center; border-radius:16px;
                background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);">
                <span style="color:#7a8499; font-size:0.9rem;">No bowling data yet</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    with st.expander("📋 Full Scorecard — All Players"):
        full = run_query("""
            SELECT p.Player_Name,t.Team_Name,SUM(sc.Runs_Scored) AS Runs,
                   SUM(sc.Wickets_Taken) AS Wickets,ROUND(SUM(sc.Overs_Bowled),1) AS Overs,
                   SUM(sc.Catches) AS Catches,COUNT(DISTINCT sc.Match_ID) AS Matches
            FROM Scorecard_Cricket sc JOIN Players p ON sc.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sc.Player_ID ORDER BY Runs DESC
        """)
        if full: st.dataframe(pd.DataFrame(full),use_container_width=True,hide_index=True)
        else:    st.markdown("<p style='color:#7a8499;'>No data yet.</p>", unsafe_allow_html=True)

# ── FORM TRACKER ──────────────────────────────────────────────
with tab_form:
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom:20px;">
        <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
            color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
            ANALYTICS
        </span>
        <h3 style="font-family:'Rajdhani',sans-serif; font-size:1.6rem; font-weight:700;
            color:#fff; margin:6px 0 0 0; line-height:1.1;">
            🔥 Player Form Tracker
        </h3>
        <div style="width:48px; height:3px; background:linear-gradient(90deg,#5b52f5,transparent);
            border-radius:2px; margin-top:10px;"></div>
    </div>

    <div style="padding:14px 18px; border-radius:12px; background:rgba(91,82,245,0.07);
        border:1px solid rgba(91,82,245,0.2); margin-bottom:24px;">
        <p style="font-family:'DM Sans',sans-serif; font-size:0.84rem; color:#b0bac8; margin:0; line-height:1.7;">
            Form auto-updated by <code style="background:rgba(255,255,255,0.08); padding:1px 6px;
            border-radius:4px; font-size:0.8rem; color:#a855f7;">trg_player_form</code>
            after every score entry.
            <br>
            <span style="color:#4ade80; font-weight:600;">🟢 In Form</span> = last-5 avg ≥ 120% of overall &nbsp;·&nbsp;
            <span style="color:#f87171; font-weight:600;">🔴 Out of Form</span> = ≤ 80%
        </p>
    </div>
    """, unsafe_allow_html=True)

    fdata = run_query("""
        SELECT p.Player_Name,t.Team_Name,p.Form_Status,
               ROUND(IFNULL(AVG(sc.Runs_Scored),0),1) AS Avg_Runs,
               IFNULL(SUM(sc.Wickets_Taken),0) AS Wickets
        FROM Players p JOIN Teams t ON p.Team_ID=t.Team_ID
        LEFT JOIN Scorecard_Cricket sc ON sc.Player_ID=p.Player_ID
        WHERE t.Sport_ID=1
        GROUP BY p.Player_ID
        ORDER BY CASE p.Form_Status WHEN 'In Form' THEN 1 WHEN 'Neutral' THEN 2 ELSE 3 END, Avg_Runs DESC
    """)
    if fdata:
        fdf=pd.DataFrame(fdata)
        fdf["Status"]=fdf["Form_Status"].map({"In Form":"🔥 In Form","Out of Form":"❄️ Out of Form","Neutral":"➖ Neutral"}).fillna("➖ Neutral")
        def cf(v):
            if "In Form" in str(v):     return "color:#4ade80;font-weight:bold"
            if "Out of Form" in str(v): return "color:#f87171;font-weight:bold"
            return "color:#4a5568"
        st.dataframe(fdf[["Player_Name","Team_Name","Status","Avg_Runs","Wickets"]].style.map(cf,subset=["Status"]),
                     use_container_width=True,hide_index=True)
    else:
        st.markdown("""
        <div style="padding:40px; text-align:center; border-radius:16px;
            background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);">
            <span style="color:#7a8499; font-size:0.9rem;">No player data available</span>
        </div>
        """, unsafe_allow_html=True)