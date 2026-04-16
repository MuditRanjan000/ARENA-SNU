import streamlit as st
import time
import pandas as pd
from db_connection import run_query, call_procedure

try:
    st.set_page_config(page_title="Schedule — ARENA SNU", page_icon="📅", layout="wide")
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
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h2 style="background:linear-gradient(90deg,#3b82f6,#6c63ff);
   -webkit-background-clip:text;-webkit-text-fill-color:transparent;
   font-size:2rem;font-weight:800;margin:0">📅 Schedule a Match</h2>
<p style="color:#6b7a99;font-size:.875rem;margin-top:4px">
   Calls the <strong>ScheduleMatch</strong> stored procedure — venue conflict prevention built in</p>
""", unsafe_allow_html=True)
st.divider()

# RBAC Verification
role = st.session_state.get("role", "viewer")
CAN_SCHEDULE = role in ("admin", "organiser")

if CAN_SCHEDULE:
    st.markdown("""
    <div style="padding:10px 16px;border-radius:8px;border-left:3px solid #6c63ff;
    background:rgba(108,99,255,.07);font-size:13px;margin-bottom:20px">
        The <strong>ScheduleMatch</strong> procedure checks: (1) venue not double-booked at same date+time,
        (2) teams are different. If either check fails, MySQL raises a <code>SIGNAL SQLSTATE</code> error.
    </div>
    """, unsafe_allow_html=True)

    sports = run_query("SELECT Sport_ID, Sport_Name FROM Sports")
    if not sports:
        st.error("❌ No sports found in database")
        st.stop()

    sport_dict = {s["Sport_Name"]: s["Sport_ID"] for s in sports}
    selected_sport = st.selectbox("Select Sport", list(sport_dict.keys()))

    teams = run_query("SELECT Team_ID, Team_Name FROM Teams WHERE Sport_ID = %s", (sport_dict[selected_sport],))
    if not teams:
        st.warning("⚠️ No teams found for this sport")
        st.stop()

    team_dict = {t["Team_Name"]: t["Team_ID"] for t in teams}

    venues = run_query("SELECT Venue_ID, Venue_Name FROM Venues")
    if not venues:
        st.error("❌ No venues found in database")
        st.stop()

    venue_dict = {v["Venue_Name"]: v["Venue_ID"] for v in venues}

    with st.form("schedule_form"):
        col1, col2 = st.columns(2)
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
    st.info("🔒 Match scheduling is restricted to **Admins** and **Organisers**.")

st.divider()
st.subheader("📅 Full Match Schedule")
matches = run_query("SELECT Sport_Name, Team_A, Team_B, Match_Date, Match_Time, Venue_Name, Stage, Status, Winner FROM Upcoming_Schedule")
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
    st.info("No matches scheduled yet.")