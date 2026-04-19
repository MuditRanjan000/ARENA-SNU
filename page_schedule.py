import streamlit as st
import time
import pandas as pd
from db_connection import run_query, call_procedure

try:
    st.set_page_config(page_title="Schedule — ARENA SNU", page_icon="📅", layout="wide")
except Exception:
    pass

# ── UNIFIED CSS ───────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
/* Base */ html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background: #080c14 !important; font-family: 'DM Sans', sans-serif; color: #b0bac8; } [data-testid="stSidebar"] { background: rgba(8,12,20,0.95) !important; border-right: 1px solid rgba(255,255,255,0.06); } [data-testid="stHeader"] { background: transparent !important; } section[data-testid="stMain"] > div { background: transparent !important; } p, label, div { color: #b0bac8; font-family: 'DM Sans', sans-serif; }
/* Dividers */ hr { border: none; border-top: 1px solid rgba(255,255,255,0.07) !important; margin: 2rem 0 !important; }
/* Buttons */ div.stButton > button { background: transparent !important; color: #fff !important; font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; font-size: 0.875rem !important; border-radius: 40px !important; border: 1px solid rgba(255,255,255,0.3) !important; padding: 0.55rem 1.6rem !important; letter-spacing: 0.03em !important; transition: all 0.25s ease !important; backdrop-filter: blur(8px) !important; } div.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 32px rgba(108,99,255,0.25) !important; border-color: rgba(108,99,255,0.5) !important; } div.stButton > button[kind="primary"], div.stFormSubmitButton > button { background: linear-gradient(135deg, rgba(108,99,255,0.6), rgba(91,82,245,0.5)) !important; color: #fff !important; font-weight: 700 !important; border-radius: 50px !important; border: 1px solid rgba(108,99,255,0.4) !important; padding: 12px 32px !important; font-family: 'Rajdhani', sans-serif !important; font-size: 1rem !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; transition: all 0.3s ease !important; width: 100% !important; } div.stButton > button[kind="primary"]:hover, div.stFormSubmitButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 12px 40px rgba(108,99,255,0.5) !important; }
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
    <div style="display: inline-block; background: rgba(108,99,255,0.1); border: 1px solid rgba(108,99,255,0.22);
        border-radius: 20px; padding: 4px 14px; margin-bottom: 18px;">
        <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
            color:rgba(255,255,255,0.45); text-transform:uppercase; font-weight:500;">
            SURGE 2025 · VENUE CONFLICT PREVENTION
        </span>
    </div>
    <h1 style="font-family:'Rajdhani',sans-serif; font-size:3rem; font-weight:800; margin:0;
        line-height:1.0; color:#fff; letter-spacing:-0.01em;">
        📅 Schedule <span style="background:linear-gradient(90deg,#3b82f6,#6c63ff);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;">a Match</span>
    </h1>
    <div style="width:52px; height:3px; background:linear-gradient(90deg,#6c63ff,transparent);
        border-radius:2px; margin:14px 0 12px 0;"></div>
    <p style="font-family:'DM Sans',sans-serif; color:#7a8499; font-size:0.95rem;
        margin:0; line-height:1.7;">
        Calls the <code style="background:rgba(255,255,255,0.07); padding:2px 7px; border-radius:5px;
        font-size:0.85rem; color:#8b85ff;">ScheduleMatch</code> stored procedure — venue conflict prevention built in
    </p>
</div>
""", unsafe_allow_html=True)

# RBAC Verification
role = st.session_state.get("role", "viewer")
CAN_SCHEDULE = role in ("admin", "organiser")

if CAN_SCHEDULE:
    st.markdown("""
    <div style="padding:16px 20px; border-radius:14px; background:rgba(108,99,255,0.07);
        border:1px solid rgba(108,99,255,0.2); margin-bottom:32px;">
        <div style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:4px;
            color:rgba(108,99,255,0.8); text-transform:uppercase; font-weight:500; margin-bottom:8px;">
            PROCEDURE GUARD RAILS
        </div>
        <p style="font-family:'DM Sans',sans-serif; font-size:0.875rem; color:#b0bac8; margin:0; line-height:1.7;">
            The <strong style="color:#e8ecf4;">ScheduleMatch</strong> procedure checks:
            (1) venue not double-booked at same date+time,
            (2) teams are different. If either check fails, MySQL raises a
            <code style="background:rgba(255,255,255,0.08); padding:1px 6px; border-radius:4px;
            font-size:0.8rem; color:#8b85ff;">SIGNAL SQLSTATE</code> error.
        </p>
    </div>
    """, unsafe_allow_html=True)

    sports = run_query("SELECT Sport_ID, Sport_Name FROM Sports", fetch=True)
    if not sports:
        st.error("❌ No sports found in database")
        st.stop()

    sport_dict = {s["Sport_Name"]: s["Sport_ID"] for s in sports}

    st.markdown("""
    <div style="margin-bottom:6px;">
        <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
            color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
            SPORT
        </span>
    </div>""", unsafe_allow_html=True)
    selected_sport = st.selectbox("Select Sport", list(sport_dict.keys()), label_visibility="collapsed")

    teams = run_query("SELECT Team_ID, Team_Name FROM Teams WHERE Sport_ID = %s", (sport_dict[selected_sport],), fetch=True)
    if not teams:
        st.warning("⚠️ No teams found for this sport")
        st.stop()

    team_dict = {t["Team_Name"]: t["Team_ID"] for t in teams}

    venues = run_query("SELECT Venue_ID, Venue_Name FROM Venues", fetch=True)
    if not venues:
        st.error("❌ No venues found in database")
        st.stop()

    venue_dict = {v["Venue_Name"]: v["Venue_ID"] for v in venues}

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    with st.form("schedule_form"):
        st.markdown("""
        <div style="margin-bottom:20px;">
            <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
                color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                MATCH DETAILS
            </span>
            <div style="width:40px; height:2px; background:linear-gradient(90deg,#6c63ff,transparent);
                border-radius:2px; margin-top:8px;"></div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="large")
        with col1:
            team1 = st.selectbox("Team 1", list(team_dict.keys()))
            match_date = st.date_input("Match Date")
            selected_stage = st.selectbox("Stage", ["Group Stage", "Quarter-Final", "Semi-Final", "Final"])
        with col2:
            team2 = st.selectbox("Team 2", list(team_dict.keys()), index=1 if len(team_dict) > 1 else 0)
            match_time = st.time_input("Match Time")
            selected_venue = st.selectbox("Venue", list(venue_dict.keys()))

        submit = st.form_submit_button("✅ Schedule Match", use_container_width=True)

        if submit:
            if team1 == team2:
                st.error("❌ Teams cannot be the same")
            else:
                args = (
                    sport_dict[selected_sport],
                    team_dict[team1],
                    team_dict[team2],
                    str(match_date),
                    str(match_time),
                    venue_dict[selected_venue],
                    selected_stage
                )
                result, error = call_procedure("ScheduleMatch", args)
                if error:
                    if "already booked" in error:
                        st.error("❌ Venue is already booked at that date and time. Choose a different slot.")
                    elif "same" in error.lower():
                        st.error("❌ Team A and Team B cannot be the same team.")
                    else:
                        st.error(f"❌ {error}")
                else:
                    st.toast("Match scheduled!", icon="✅")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
else:
    st.markdown("""
    <div style="padding:24px 28px; border-radius:16px; background:rgba(255,255,255,0.04);
        border:1px solid rgba(255,255,255,0.09); margin-bottom:32px; display:flex;
        align-items:center; gap:14px;">
        <span style="font-size:1.5rem;">🔒</span>
        <div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:1rem; font-weight:700;
                color:#e8ecf4; margin-bottom:4px;">Access Restricted</div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.875rem; color:#7a8499;">
                Match scheduling is restricted to <strong style="color:#b0bac8;">Admins</strong>
                and <strong style="color:#b0bac8;">Organisers</strong>.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom:20px;">
    <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
        color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
        OVERVIEW
    </span>
    <h3 style="font-family:'Rajdhani',sans-serif; font-size:1.6rem; font-weight:700;
        color:#fff; margin:6px 0 0 0; line-height:1.1;">
        📅 Full Match Schedule
    </h3>
    <div style="width:48px; height:3px; background:linear-gradient(90deg,#3b82f6,transparent);
        border-radius:2px; margin-top:10px;"></div>
</div>
""", unsafe_allow_html=True)

matches = run_query("SELECT Sport_Name, Team_A, Team_B, Match_Date, Match_Time, Venue_Name, Stage, Status, Winner FROM Upcoming_Schedule", fetch=True)
if matches:
    sched_df = pd.DataFrame(matches)
    def style_status(val):
        if val == "Completed": return "color:#10b981;font-weight:bold"
        if val == "Scheduled": return "color:#8b85ff;font-weight:bold"
        if val == "Cancelled": return "color:#ef4444;font-weight:bold"
        return ""
    st.dataframe(sched_df.style.map(style_status, subset=["Status"]),
                 use_container_width=True, hide_index=True)
else:
    st.markdown("""
    <div style="padding:40px; text-align:center; border-radius:16px;
        background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);">
        <span style="color:#7a8499; font-size:0.9rem;">No matches scheduled yet</span>
    </div>
    """, unsafe_allow_html=True)