# home_page.py — ARENA SNU | System Architect: Mudit
# Dashboard + Add Team + Add Player
# Every form submission writes directly to MySQL
import streamlit as st
from db_connection import run_query, call_procedure

st.set_page_config(page_title="ARENA SNU", page_icon="🏆", layout="wide")

st.markdown("""
<h1 style='text-align:center;background:linear-gradient(90deg,#6c63ff,#a855f7);
-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:2.5rem;font-weight:800'>
🏆 ARENA SNU</h1>
<p style='text-align:center;color:#888;font-size:1rem'>Athletic Resource & Event Navigation Application |
Shiv Nadar University | SURGE Sports Festival</p>
""", unsafe_allow_html=True)
st.divider()

# Live stats — fetched fresh from MySQL on every load
col1,col2,col3,col4 = st.columns(4)
teams     = run_query("SELECT COUNT(*) AS cnt FROM Teams")
players   = run_query("SELECT COUNT(*) AS cnt FROM Players")
matches   = run_query("SELECT COUNT(*) AS cnt FROM Matches")
completed = run_query("SELECT COUNT(*) AS cnt FROM Matches WHERE Status='Completed'")
col1.metric("🏅 Teams",    teams[0]["cnt"]     if teams     else 0)
col2.metric("👤 Players",  players[0]["cnt"]   if players   else 0)
col3.metric("📅 Matches",  matches[0]["cnt"]   if matches   else 0)
col4.metric("✅ Completed",completed[0]["cnt"] if completed else 0)
st.divider()

# Live match schedule from VIEW
st.subheader("📅 Match Schedule")
st.caption("Live from MySQL view Upcoming_Schedule — auto-updates when new matches are scheduled")
schedule = run_query("SELECT Sport_Name,Team_A,Team_B,Match_Date,Match_Time,Venue_Name,Stage,Status,Winner FROM Upcoming_Schedule LIMIT 15")
st.dataframe(schedule if schedule else [], use_container_width=True)
st.divider()

# Live points table from VIEW
st.subheader("🏆 Points Table")
st.caption("Auto-updates when match results are entered")
points = run_query("SELECT Team_Name,University,Sport_Name,Matches_Played,Wins,Losses,Points FROM Points_Table")
st.dataframe(points if points else [], use_container_width=True)
st.divider()

# Add team form — directly INSERTs into MySQL
st.subheader("➕ Register New Team")
st.caption("Submitting this form immediately adds to MySQL database — visible everywhere instantly")
sports_list = run_query("SELECT Sport_ID, Sport_Name FROM Sports")
sport_map   = {s["Sport_Name"]: s["Sport_ID"] for s in sports_list}
with st.form("add_team", clear_on_submit=True):
    c1,c2 = st.columns(2)
    with c1:
        tname = st.text_input("Team Name *", placeholder="e.g. IIT Delhi Warriors")
        uni   = st.text_input("University *", placeholder="e.g. IIT Delhi")
    with c2:
        sport = st.selectbox("Sport *", list(sport_map.keys()))
        coach = st.text_input("Coach Name *", placeholder="e.g. Rahul Dravid")
    if st.form_submit_button("✅ Add Team to Database", use_container_width=True):
        if not tname.strip() or not uni.strip() or not coach.strip():
            st.error("All fields required!")
        else:
            rows = run_query(
                "INSERT INTO Teams (Team_Name,University,Sport_ID,Coach_Name) VALUES (%s,%s,%s,%s)",
                (tname.strip(), uni.strip(), sport_map[sport], coach.strip()), fetch=False)
            if rows:
                st.success(f"✅ '{tname}' added to MySQL! Stats above updated.")
                st.rerun()
            else:
                st.error("Failed — team may already exist for this sport.")

st.divider()

# Add player form — calls RegisterPlayer stored procedure
st.subheader("👤 Register New Player")
st.caption("Uses RegisterPlayer stored procedure — jersey uniqueness enforced at DB level")
all_teams = run_query("SELECT Team_ID,Team_Name,University FROM Teams ORDER BY Team_Name")
team_map  = {f"{t['Team_Name']} ({t['University']})": t["Team_ID"] for t in all_teams}
with st.form("add_player", clear_on_submit=True):
    c1,c2 = st.columns(2)
    with c1:
        pname  = st.text_input("Player Name *", placeholder="e.g. Arjun Mehta")
        tsel   = st.selectbox("Team *", list(team_map.keys()) if team_map else ["No teams yet"])
    with c2:
        prole  = st.text_input("Role *", placeholder="e.g. Batsman, Striker")
        jersey = st.number_input("Jersey No *", min_value=1, max_value=99, value=10)
    if st.form_submit_button("✅ Register Player to Database", use_container_width=True):
        if not pname.strip() or not prole.strip() or not team_map:
            st.error("All fields required!")
        else:
            result, error = call_procedure("RegisterPlayer",
                (pname.strip(), team_map[tsel], prole.strip(), int(jersey)))
            if error:
                st.error(f"❌ {error}")
            else:
                st.success(f"✅ {pname} added to MySQL!")
                st.rerun()

st.divider()
st.caption("ARENA SNU | Shiv Nadar University | System Architect: Mudit | All changes sync to MySQL instantly")
