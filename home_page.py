# home_page.py
import streamlit as st
import time
import plotly.express as px
import pandas as pd
from db_connection import run_query, call_procedure

st.set_page_config(page_title="ARENA SNU", page_icon="🏆", layout="wide")

# Custom CSS for global styling
st.markdown("""
<style>
    div.stButton > button {
        background: linear-gradient(90deg, #6c63ff, #a855f7);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0px 4px 15px rgba(108, 99, 255, 0.4);
    }
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align:center;background:linear-gradient(90deg,#6c63ff,#a855f7);
-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:2.5rem;font-weight:800'>
🏆 ARENA SNU</h1>
<p style='text-align:center;color:#888;font-size:1rem'>Athletic Resource & Event Navigation Application |
Shiv Nadar University | SURGE Sports Festival</p>
""", unsafe_allow_html=True)
st.divider()

tab1, tab2, tab3 = st.tabs(["📊 Dashboard & Live Stats", "➕ Team Management", "👤 Player Management"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    teams     = run_query("SELECT COUNT(*) AS cnt FROM Teams")
    players   = run_query("SELECT COUNT(*) AS cnt FROM Players")
    matches   = run_query("SELECT COUNT(*) AS cnt FROM Matches")
    completed = run_query("SELECT COUNT(*) AS cnt FROM Matches WHERE Status='Completed'")

    col1.metric("🏅 Teams",    teams[0]["cnt"]     if teams     else 0)
    col2.metric("👤 Players",  players[0]["cnt"]   if players   else 0)
    col3.metric("📅 Matches",  matches[0]["cnt"]   if matches   else 0)
    col4.metric("✅ Completed",completed[0]["cnt"] if completed else 0)
    st.divider()

    st.subheader("🏆 Tournament Standings")
    points_data = run_query("SELECT Team_Name,University,Sport_Name,Matches_Played,Wins,Losses,Points FROM Points_Table")
    
    if points_data:
        points = pd.DataFrame(points_data)
        leader = points.iloc[0]['Team_Name']
        st.markdown(f"""
            <div style="padding: 15px; border-radius: 10px; border-left: 5px solid #f5a623; background-color: rgba(245, 166, 35, 0.1);">
                <strong>🏆 Current Tournament Leader:</strong> {leader}
            </div>
            <br>
        """, unsafe_allow_html=True)

        fig = px.bar(
            points, 
            x="Team_Name", 
            y="Points", 
            color="University",
            hover_data=["Wins", "Losses", "Matches_Played"],
            labels={"Team_Name": "Team", "Points": "Total Points"}
        )
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("View Full Points Data Table"):
            st.dataframe(points, use_container_width=True, hide_index=True)
    else:
        st.info("No points data available yet.")

    st.divider()
    st.subheader("📅 Match Schedule")
    schedule_data = run_query("SELECT Sport_Name,Team_A,Team_B,Match_Date,Match_Time,Venue_Name,Stage,Status,Winner FROM Upcoming_Schedule LIMIT 15")
    if schedule_data:
        st.dataframe(pd.DataFrame(schedule_data), use_container_width=True, hide_index=True)
    else:
        st.info("No upcoming matches scheduled.")

with tab2:
    st.subheader("Team Management")
    sports_list = run_query("SELECT Sport_ID, Sport_Name FROM Sports")
    sport_map   = {s["Sport_Name"]: s["Sport_ID"] for s in sports_list} if sports_list else {}

    with st.expander("➕ Click to Register a New Team", expanded=True):
        with st.form("add_team", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                tname = st.text_input("Team Name *", placeholder="e.g. IIT Delhi Warriors")
                uni   = st.text_input("University *", placeholder="e.g. IIT Delhi")
            with c2:
                sport = st.selectbox("Sport *", list(sport_map.keys()) if sport_map else ["No sports available"])
                coach = st.text_input("Coach Name *", placeholder="e.g. Rahul Dravid")
            
            if st.form_submit_button("✅ Add Team", use_container_width=True):
                if not tname.strip() or not uni.strip() or not coach.strip() or not sport_map:
                    st.error("All fields required!")
                else:
                    with st.spinner("Writing to database..."):
                        time.sleep(0.5)
                        rows = run_query(
                            "INSERT INTO Teams (Team_Name,University,Sport_ID,Coach_Name) VALUES (%s,%s,%s,%s)",
                            (tname.strip(), uni.strip(), sport_map[sport], coach.strip()), fetch=False)
                        if rows:
                            st.balloons()
                            st.toast(f"'{tname}' added to MySQL!", icon='✅')
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Failed — team may already exist for this sport.")

with tab3:
    st.subheader("Player Management")
    all_teams = run_query("SELECT Team_ID,Team_Name,University FROM Teams ORDER BY Team_Name")
    team_map  = {f"{t['Team_Name']} ({t['University']})": t["Team_ID"] for t in all_teams} if all_teams else {}

    with st.expander("👤 Click to Register a New Player", expanded=True):
        with st.form("add_player", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                pname  = st.text_input("Player Name *", placeholder="e.g. Arjun Mehta")
                tsel   = st.selectbox("Team *", list(team_map.keys()) if team_map else ["No teams yet"])
            with c2:
                prole  = st.text_input("Role *", placeholder="e.g. Batsman, Striker")
                jersey = st.number_input("Jersey No *", min_value=1, max_value=99, value=10, help="Must be unique within the team (1-99).")
            
            if st.form_submit_button("✅ Register Player", use_container_width=True):
                if not pname.strip() or not prole.strip() or not team_map:
                    st.error("All fields required!")
                else:
                    with st.spinner("Verifying jersey uniqueness and registering..."):
                        time.sleep(0.5)
                        result, error = call_procedure("RegisterPlayer",
                            (pname.strip(), team_map[tsel], prole.strip(), int(jersey)))
                        if error:
                            st.error(f"❌ {error}")
                        else:
                            st.toast(f"{pname} added to MySQL!", icon='✅')
                            time.sleep(1)
                            st.rerun()