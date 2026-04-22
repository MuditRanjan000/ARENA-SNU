# page_football.py — ARENA SNU Football Module v7
# SURGE 2025 · Assigned: Aayush · Reviewed: Mudit
import streamlit as st, time, pandas as pd
import plotly.express as px
from db_connection import run_query

try: st.set_page_config(page_title="Football — ARENA SNU", page_icon="⚽", layout="wide")
except: pass

# ── UNIFIED CSS ───────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
/* Base */ html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background: #080c14 !important; font-family: 'DM Sans', sans-serif; color: #b0bac8; } [data-testid="stSidebar"] { background: rgba(8,12,20,0.95) !important; border-right: 1px solid rgba(255,255,255,0.06); } [data-testid="stHeader"] { background: transparent !important; } section[data-testid="stMain"] > div { background: transparent !important; } p, label, div { color: #b0bac8; font-family: 'DM Sans', sans-serif; }
/* Dividers */ hr { border: none; border-top: 1px solid rgba(255,255,255,0.07) !important; margin: 2rem 0 !important; }
/* Buttons */ div.stButton > button { background: transparent !important; color: #fff !important; font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; font-size: 0.875rem !important; border-radius: 40px !important; border: 1px solid rgba(255,255,255,0.3) !important; padding: 0.55rem 1.6rem !important; letter-spacing: 0.03em !important; transition: all 0.25s ease !important; backdrop-filter: blur(8px) !important; } div.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 32px rgba(34,197,94,0.25) !important; border-color: rgba(34,197,94,0.5) !important; } div.stButton > button[kind="primary"], div.stFormSubmitButton > button { background: linear-gradient(135deg, rgba(34,197,94,0.6), rgba(91,82,245,0.5)) !important; color: #fff !important; font-weight: 700 !important; border-radius: 50px !important; border: 1px solid rgba(34,197,94,0.4) !important; padding: 12px 32px !important; font-family: 'Rajdhani', sans-serif !important; font-size: 1rem !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; transition: all 0.3s ease !important; width: 100% !important; } div.stButton > button[kind="primary"]:hover, div.stFormSubmitButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 12px 40px rgba(34,197,94,0.5) !important; }
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
    <div style="display: inline-block; background: rgba(34,197,94,0.1); border: 1px solid rgba(34,197,94,0.22);
        border-radius: 20px; padding: 4px 14px; margin-bottom: 18px;">
        <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
            color:rgba(255,255,255,0.45); text-transform:uppercase; font-weight:500;">
            SURGE 2025 · 11-A-SIDE
        </span>
    </div>
    <h1 style="font-family:'Rajdhani',sans-serif; font-size:3rem; font-weight:800; margin:0;
        line-height:1.0; color:#fff; letter-spacing:-0.01em;">
        ⚽ Football <span style="color:#22c55e;">Module</span>
    </h1>
    <div style="width:52px; height:3px; background:linear-gradient(90deg,#22c55e,transparent);
        border-radius:2px; margin:14px 0 12px 0;"></div>
    <p style="font-family:'DM Sans',sans-serif; color:#7a8499; font-size:0.95rem;
        margin:0; line-height:1.7;">
        Score entry · Golden Boot leaderboard · Suspension tracking — all live from MySQL.
    </p>
</div>
""", unsafe_allow_html=True)

role      = st.session_state.get("role","viewer")
CAN_ENTER = role in ("admin","organiser")

def get_matches():
    return run_query("""
        SELECT m.Match_ID,
               CONCAT(ta.Team_Name,' vs ',tb.Team_Name,' | ',m.Stage,
                      ' | ',DATE_FORMAT(m.Match_Date,'%d %b %Y'),' @ ',v.Venue_Name) AS Label,
               m.Team_A_ID, m.Team_B_ID
        FROM Matches m JOIN Sports sp ON m.Sport_ID=sp.Sport_ID
        JOIN Teams ta ON m.Team_A_ID=ta.Team_ID JOIN Teams tb ON m.Team_B_ID=tb.Team_ID
        JOIN Venues v  ON m.Venue_ID=v.Venue_ID
        WHERE sp.Sport_Name='Football' ORDER BY m.Match_Date DESC
    """, fetch=True) or []

def get_players(ta, tb):
    return run_query("""
        SELECT p.Player_ID,
               CONCAT(p.Player_Name,' (',t.Team_Name,' | #',p.Jersey_No,')') AS Label, p.Role
        FROM Players p JOIN Teams t ON p.Team_ID=t.Team_ID
        WHERE p.Team_ID IN (%s,%s) ORDER BY t.Team_Name, p.Player_Name
    """, (ta,tb), fetch=True) or []

# ── SCORE ENTRY ───────────────────────────────────────────────
if CAN_ENTER:
    st.markdown("""
    <div style="margin: 2rem 0 0.75rem;">
      <p style="font-family:'DM Sans',sans-serif; font-size:0.7rem; letter-spacing:5px;
         color:rgba(255,255,255,0.35); text-transform:uppercase; margin:0 0 8px">Score Entry</p>
      <h3 style="font-family:'Rajdhani',sans-serif; font-size:1.5rem; font-weight:700;
         color:#e8ecf4; margin:0 0 4px; line-height:1.1;">Enter Match Score</h3>
      <div style="width:36px; height:3px; background:linear-gradient(90deg,#22c55e,transparent);
         border-radius:2px; margin-bottom:1rem;"></div>
    </div>
    """, unsafe_allow_html=True)

    matches = get_matches()
    if not matches:
        st.warning("No football matches found.")
    else:
        mdict = {r["Label"]: r for r in matches}
        left_col, right_col = st.columns([3, 2], gap="large")
        with left_col:
            sel   = mdict[st.selectbox("Select Match", list(mdict.keys()))]
            mid   = sel["Match_ID"]
            players = get_players(sel["Team_A_ID"], sel["Team_B_ID"])

        if not players:
            st.warning("No players for this match.")
        else:
            pdict = {r["Label"]: r for r in players}
            with right_col:
                psel  = pdict[st.selectbox("Select Player", list(pdict.keys()))]
            pid   = psel["Player_ID"]

            if psel.get("Role") == "SUSPENDED":
                st.markdown("""
                <div style="padding:12px 18px; border-radius:12px;
                   border-left:3px solid #f97316; background:rgba(249,115,22,0.08);
                   font-family:'DM Sans',sans-serif; font-size:0.875rem; color:#fdba74;
                   margin-bottom:1rem;">
                  ⚠️ &nbsp; Player is <strong>SUSPENDED</strong>. Verify with referee before entering stats.
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            with st.form("football_score"):
                c1, c2, c3, c4 = st.columns(4, gap="medium")
                with c1: goals   = st.number_input("⚽ Goals",        min_value=0, max_value=20)
                with c2: assists = st.number_input("🎯 Assists",      min_value=0, max_value=20)
                with c3: yc      = st.number_input("🟨 Yellow Cards", min_value=0, max_value=2)
                with c4: rc      = st.number_input("🟥 Red Cards",    min_value=0, max_value=1)

                st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
                btn_col, _ = st.columns([1, 3])
                with btn_col:
                    submit = st.form_submit_button("✅ Submit Score", type="primary", use_container_width=True)

                if submit:
                    ex = run_query("SELECT COUNT(*) AS c FROM Scorecard_Football WHERE Match_ID=%s AND Player_ID=%s",
                                   (mid,pid), fetch=True)
                    if ex and ex[0]["c"] > 0:
                        st.error("🚫 Score already recorded for this player in this match.")
                    else:
                        with st.spinner("Writing to MySQL…"):
                            run_query(
                                "INSERT INTO Scorecard_Football "
                                "(Match_ID,Player_ID,Goals,Assists,Yellow_Cards,Red_Cards) "
                                "VALUES (%s,%s,%s,%s,%s,%s)",
                                (mid,pid,goals,assists,yc,rc), fetch=False
                            )
                            time.sleep(0.4)
                        st.toast("Saved! trg_suspend_player may have fired.", icon="✅")
                        time.sleep(1); st.rerun()

            st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
            
            # --- MATCH RESULT ENTRY ---
            st.markdown("""
            <div style="margin-bottom:20px;">
                <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
                    color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                    MATCH RESULT ENTRY
                </span>
                <div style="width:40px; height:2px; background:linear-gradient(90deg,#22c55e,transparent);
                    border-radius:2px; margin-top:8px;"></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Get Team Names from the label or query. 
            # Luckily, the 'matches' query has m.Team_A_ID and m.Team_B_ID. Let's just fetch the team names.
            # We will just fetch team names using Team IDs.
            team_a_name = run_query("SELECT Team_Name FROM Teams WHERE Team_ID=%s", (sel["Team_A_ID"],))[0]["Team_Name"]
            team_b_name = run_query("SELECT Team_Name FROM Teams WHERE Team_ID=%s", (sel["Team_B_ID"],))[0]["Team_Name"]
            
            with st.form("football_match_result", clear_on_submit=True):
                mc1, mc2 = st.columns(2)
                with mc1:
                    ta_score = st.text_input(f"{team_a_name} Overall Score", placeholder="e.g. 3")
                with mc2:
                    tb_score = st.text_input(f"{team_b_name} Overall Score", placeholder="e.g. 1")
                
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
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.divider()
else:
    st.markdown("""
    <div style="padding:16px 20px; border-radius:14px;
       background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
       font-family:'DM Sans',sans-serif; font-size:0.875rem; color:#7a8499;
       margin-bottom:1.5rem; display:flex; align-items:center; gap:10px;">
      <span style="font-size:1.1rem;">🔒</span>
      <span>Score entry is restricted to <strong style='color:#b0bac8'>Organisers</strong> and Admins.</span>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

# ── GOLDEN BOOT ────────────────────────────────────────────────
st.markdown("""
<div style="margin: 1.5rem 0 0.75rem;">
  <p style="font-family:'DM Sans',sans-serif; font-size:0.7rem; letter-spacing:5px;
     color:rgba(255,255,255,0.35); text-transform:uppercase; margin:0 0 8px">Leaderboard</p>
  <h3 style="font-family:'Rajdhani',sans-serif; font-size:1.5rem; font-weight:700;
     color:#e8ecf4; margin:0 0 4px; line-height:1.1;">🏆 Golden Boot — Top Scorers</h3>
  <div style="width:36px; height:3px; background:linear-gradient(90deg,#22c55e,transparent);
     border-radius:2px; margin-bottom:1rem;"></div>
</div>
""", unsafe_allow_html=True)

gb = run_query("""
    SELECT p.Player_Name AS Player, t.Team_Name AS Team, t.University,
           SUM(sf.Goals) AS Goals, SUM(sf.Assists) AS Assists,
           SUM(sf.Yellow_Cards) AS Yellow_Cards, SUM(sf.Red_Cards) AS Red_Cards,
           COUNT(DISTINCT sf.Match_ID) AS Matches
    FROM Scorecard_Football sf JOIN Players p ON sf.Player_ID=p.Player_ID
    JOIN Teams t ON p.Team_ID=t.Team_ID
    GROUP BY sf.Player_ID HAVING Goals>0 ORDER BY Goals DESC, Assists DESC LIMIT 15
""", fetch=True)
if gb:
    df=pd.DataFrame(gb); df.insert(0,"Rank",range(1,len(df)+1))
    medals={1:"🥇",2:"🥈",3:"🥉"}
    df["Rank"]=df["Rank"].map(lambda r: f"{medals.get(r,str(r))} {r}" if r<=3 else str(r))
    df=df.rename(columns={"Goals":"⚽ Goals","Assists":"🎯 Assists",
                           "Yellow_Cards":"🟨 Yellow","Red_Cards":"🟥 Red","Matches":"Matches"})

    table_col, chart_col = st.columns([1, 1.2], gap="large")
    with table_col:
        st.dataframe(df, width='stretch', hide_index=True)

    with chart_col:
        df2 = pd.DataFrame(gb)
        fig = px.bar(df2.head(10), x="Player", y=["Goals","Assists"],
                     barmode="group",
                     color_discrete_sequence=["#22c55e","#5b52f5"],
                     title="Goals & Assists — Top 10")
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#b0bac8", font_family="DM Sans",
            title_font=dict(family="Rajdhani", size=16, color="#e8ecf4"),
            margin=dict(t=40, b=10, l=0, r=0),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.05)",
                       tickfont=dict(size=11)),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.05)"),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#7a8499")),
            bargap=0.25,
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)
else:
    st.markdown("""
    <div style="padding:20px 24px; border-radius:16px; background:rgba(255,255,255,0.03);
       border:1px solid rgba(255,255,255,0.07); text-align:center;
       font-family:'DM Sans',sans-serif; color:#7a8499; font-size:0.9rem;">
      No goals recorded yet — enter match scores to populate the leaderboard.
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
st.divider()

# ── SUSPENSION TRACKER ─────────────────────────────────────────
st.markdown("""
<div style="margin: 1.5rem 0 0.75rem;">
  <p style="font-family:'DM Sans',sans-serif; font-size:0.7rem; letter-spacing:5px;
     color:rgba(255,255,255,0.35); text-transform:uppercase; margin:0 0 8px">Discipline</p>
  <h3 style="font-family:'Rajdhani',sans-serif; font-size:1.5rem; font-weight:700;
     color:#e8ecf4; margin:0 0 4px; line-height:1.1;">🚫 Suspension Tracker</h3>
  <div style="width:36px; height:3px; background:linear-gradient(90deg,#f97316,transparent);
     border-radius:2px; margin-bottom:0.75rem;"></div>
</div>
<div style="padding:10px 16px; border-radius:10px; border-left:3px solid rgba(249,115,22,0.6);
   background:rgba(249,115,22,0.06); font-family:'DM Sans',sans-serif;
   font-size:0.8rem; color:#7a8499; margin-bottom:1.25rem;">
  Powered by <code style="background:rgba(255,255,255,0.06); padding:1px 6px; border-radius:4px; color:#b0bac8;">trg_suspend_player</code>
  — auto-suspends when yellow card total ≥ 3.
</div>
""", unsafe_allow_html=True)

susp = run_query("""
    SELECT p.Player_Name AS Player, t.Team_Name AS Team, t.University,
           p.Jersey_No AS Jersey,
           SUM(sf.Yellow_Cards) AS Total_Yellows, SUM(sf.Red_Cards) AS Total_Reds
    FROM Players p JOIN Teams t ON p.Team_ID=t.Team_ID
    JOIN Scorecard_Football sf ON sf.Player_ID=p.Player_ID
    WHERE p.Role='SUSPENDED'
    GROUP BY p.Player_ID ORDER BY t.Team_Name
""", fetch=True)
if susp:
    st.dataframe(pd.DataFrame(susp).rename(columns={"Total_Yellows":"🟨 Yellows","Total_Reds":"🟥 Reds","Jersey":"Jersey #"}),
                 width='stretch', hide_index=True)
else:
    st.markdown("""
    <div style="padding:16px 20px; border-radius:12px; background:rgba(34,197,94,0.06);
       border:1px solid rgba(34,197,94,0.2); font-family:'DM Sans',sans-serif;
       font-size:0.875rem; color:#86efac; display:flex; align-items:center; gap:10px;">
      <span>✅</span>
      <span>No players currently suspended.</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
st.divider()

# ── FULL STATS TABLE ──────────────────────────────────────────
with st.expander("📋 All Football Stats"):
    all_stats = run_query("""
        SELECT p.Player_Name,t.Team_Name,SUM(sf.Goals) AS Goals,SUM(sf.Assists) AS Assists,
               SUM(sf.Yellow_Cards) AS Yellows,SUM(sf.Red_Cards) AS Reds,
               COUNT(DISTINCT sf.Match_ID) AS Matches
        FROM Scorecard_Football sf JOIN Players p ON sf.Player_ID=p.Player_ID
        JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sf.Player_ID ORDER BY Goals DESC
    """)
    if all_stats: st.dataframe(pd.DataFrame(all_stats),width='stretch',hide_index=True)
    else:         st.info("No data yet.")

st.markdown("""
<div style="padding: 2rem 0 0.5rem; font-family:'DM Sans',sans-serif;
   font-size:0.75rem; color:rgba(255,255,255,0.2); text-align:center; letter-spacing:2px;">
  ARENA SNU v7 · Football Module · System Architect: Mudit
</div>
""", unsafe_allow_html=True)