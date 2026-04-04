import streamlit as st
from db_connection import run_query, call_procedure

st.title("🏆 Schedule Match")

# -------------------------
# LOAD DATA (FIXED CASE)
# -------------------------
sports = run_query("SELECT Sport_ID, Sport_Name FROM sports")

if not sports:
    st.error("❌ No sports found in database")
    st.stop()

sport_dict = {s["Sport_Name"]: s["Sport_ID"] for s in sports}
selected_sport = st.selectbox("Select Sport", list(sport_dict.keys()))

# -------------------------
# TEAMS (FIXED CASE)
# -------------------------
teams = run_query(
    "SELECT Team_ID, Team_Name FROM teams WHERE Sport_ID = %s",
    (sport_dict[selected_sport],)
)

if not teams:
    st.warning("⚠️ No teams found for this sport")
    st.stop()

team_dict = {t["Team_Name"]: t["Team_ID"] for t in teams}

team1 = st.selectbox("Team 1", list(team_dict.keys()))
team2 = st.selectbox("Team 2", list(team_dict.keys()))

# -------------------------
# VENUES (FIXED CASE)
# -------------------------
venues = run_query("SELECT Venue_ID, Venue_Name FROM venues")

if not venues:
    st.error("❌ No venues found in database")
    st.stop()

venue_dict = {v["Venue_Name"]: v["Venue_ID"] for v in venues}
selected_venue = st.selectbox("Venue", list(venue_dict.keys()))

# -------------------------
# STAGE (FIXED VALUES)
# -------------------------
stages = ["Group Stage", "Quarter-Final", "Semi-Final", "Final"]
selected_stage = st.selectbox("Stage", stages)

match_date = st.date_input("Match Date")
match_time = st.time_input("Match Time")

# -------------------------
# VALIDATION
# -------------------------
if team1 == team2:
    st.error("❌ Teams cannot be the same")

# -------------------------
# BUTTON (FIXED ARGS ORDER)
# -------------------------
if st.button("Schedule Match"):
    if team1 != team2:
        args = (
            sport_dict[selected_sport],   # sport_id
            team_dict[team1],             # team A
            team_dict[team2],             # team B
            str(match_date),              # date
            str(match_time),              # time
            venue_dict[selected_venue],   # venue
            selected_stage                # stage
        )

        result, error = call_procedure("ScheduleMatch", args)

        if error:
            st.error(f"❌ Error: {error}")
        else:
            st.success("✅ Match Scheduled!")

# -------------------------
# SHOW TABLE
# -------------------------
st.subheader("📅 Upcoming Matches")

matches = run_query("SELECT * FROM Upcoming_Schedule")

if matches:
    st.dataframe(matches)
else:
    st.info("No matches scheduled yet.")