import streamlit as st
import pandas as pd
from db_connection import get_connection, run_query, call_procedure

st.title("🏏 Cricket Module")

# Fetch only scheduled cricket matches with readable team names
matches_query = """
    SELECT m.Match_ID, CONCAT(ta.Team_Name, ' vs ', tb.Team_Name, ' (', m.Match_Date, ')') AS Match_Desc
    FROM Matches m
    JOIN Teams ta ON m.Team_A_ID = ta.Team_ID
    JOIN Teams tb ON m.Team_B_ID = tb.Team_ID
    WHERE m.Sport_ID = 1 AND m.Status = 'Scheduled'
"""
match_df = run_query(matches_query)

if not match_df.empty:
    match_dict = dict(zip(match_df['Match_Desc'], match_df['Match_ID']))
    selected_match_desc = st.selectbox("Select Match", list(match_dict.keys()))
    match_id = match_dict[selected_match_desc]

    # Filter players to only those in the selected match
    players_query = f"""
        SELECT p.Player_ID, CONCAT(p.Player_Name, ' (', t.Team_Name, ')') AS Player_Desc
        FROM Players p
        JOIN Teams t ON p.Team_ID = t.Team_ID
        JOIN Matches m ON (t.Team_ID = m.Team_A_ID OR t.Team_ID = m.Team_B_ID)
        WHERE m.Match_ID = {match_id}
    """
    player_df = run_query(players_query)
    
    if not player_df.empty:
        player_dict = dict(zip(player_df['Player_Desc'], player_df['Player_ID']))
        selected_player_desc = st.selectbox("Select Player", list(player_dict.keys()))
        player_id = player_dict[selected_player_desc]

        runs = st.number_input("Runs Scored", min_value=0)
        wickets = st.number_input("Wickets Taken", min_value=0, max_value=10)
        overs = st.number_input("Overs Bowled", min_value=0.0, max_value=20.0, step=0.1)
        catches = st.number_input("Catches", min_value=0)

        if st.button("Submit Score"):
            # Execute the insert query to record the player's performance
            insert_query = f"""
                INSERT INTO Scorecard_Cricket (Match_ID, Player_ID, Runs_Scored, Wickets_Taken, Overs_Bowled, Catches)
                VALUES ({match_id}, {player_id}, {runs}, {wickets}, {overs}, {catches})
            """
            run_query(insert_query, fetch=False)
            st.success("✅ Score added successfully!")
            st.rerun()
    else:
        st.warning("No players found for this match.")
else:
    st.warning("No scheduled cricket matches available.")

st.subheader("🏆 Orange Cap (Top Runs)")
orange_cap_query = """
    SELECT p.Player_Name, t.Team_Name, SUM(sc.Runs_Scored) AS Total_Runs
    FROM Scorecard_Cricket sc
    JOIN Players p ON sc.Player_ID = p.Player_ID
    JOIN Teams t ON p.Team_ID = t.Team_ID
    GROUP BY sc.Player_ID
    ORDER BY Total_Runs DESC
"""
orange_cap_df = run_query(orange_cap_query)

if not orange_cap_df.empty:
    st.table(orange_cap_df)
    
    # Generate bar chart for top 5 scorers
    top5_df = orange_cap_df.head(5)
    chart_data = top5_df.set_index('Player_Name')['Total_Runs']
    st.bar_chart(chart_data)
else:
    st.write("No data available")

st.subheader("🔥 Player Form Status")
form_query = """
    SELECT p.Player_Name, t.Team_Name, p.Form_Status 
    FROM Players p
    JOIN Teams t ON p.Team_ID = t.Team_ID
    WHERE t.Sport_ID = 1
"""
form_df = run_query(form_query)
st.table(form_df)