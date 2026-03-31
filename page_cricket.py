# page_cricket.py
import streamlit as st
import time
import plotly.express as px
import pandas as pd
from db_connection import run_query

st.set_page_config(page_title="Cricket Module", page_icon="🏏", layout="wide")

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
</style>
""", unsafe_allow_html=True)

st.title("🏏 Cricket Module")

tab1, tab2 = st.tabs(["📝 Enter Score", "📊 Leaderboards & Form"])

with tab1:
    matches_query = """
        SELECT m.Match_ID, CONCAT(ta.Team_Name, ' vs ', tb.Team_Name, ' (', m.Match_Date, ')') AS Match_Desc
        FROM Matches m
        JOIN Teams ta ON m.Team_A_ID = ta.Team_ID
        JOIN Teams tb ON m.Team_B_ID = tb.Team_ID
        WHERE m.Sport_ID = 1 AND m.Status = 'Scheduled'
    """
    matches_data = run_query(matches_query)

    if matches_data:
        match_df = pd.DataFrame(matches_data)
        match_dict = dict(zip(match_df['Match_Desc'], match_df['Match_ID']))
        selected_match_desc = st.selectbox("Select Match", list(match_dict.keys()))
        match_id = match_dict[selected_match_desc]

        players_query = f"""
            SELECT p.Player_ID, CONCAT(p.Player_Name, ' (', t.Team_Name, ')') AS Player_Desc
            FROM Players p
            JOIN Teams t ON p.Team_ID = t.Team_ID
            JOIN Matches m ON (t.Team_ID = m.Team_A_ID OR t.Team_ID = m.Team_B_ID)
            WHERE m.Match_ID = {match_id}
        """
        players_data = run_query(players_query)
        
        if players_data:
            player_df = pd.DataFrame(players_data)
            player_dict = dict(zip(player_df['Player_Desc'], player_df['Player_ID']))
            selected_player_desc = st.selectbox("Select Player", list(player_dict.keys()))
            player_id = player_dict[selected_player_desc]

            with st.form("score_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    runs = st.number_input("Runs Scored", min_value=0)
                    wickets = st.number_input("Wickets Taken", min_value=0, max_value=10, help="Maximum 10 wickets possible per innings.")
                with col2:
                    overs = st.number_input("Overs Bowled", min_value=0.0, max_value=20.0, step=0.1, help="T20 format allows a maximum of 20 overs.")
                    catches = st.number_input("Catches", min_value=0)

                if st.form_submit_button("Submit Score", use_container_width=True):
                    with st.spinner("Recording stats..."):
                        insert_query = f"""
                            INSERT INTO Scorecard_Cricket (Match_ID, Player_ID, Runs_Scored, Wickets_Taken, Overs_Bowled, Catches)
                            VALUES ({match_id}, {player_id}, {runs}, {wickets}, {overs}, {catches})
                        """
                        run_query(insert_query, fetch=False)
                        time.sleep(0.5)
                        st.toast("Score added successfully!", icon='✅')
                        time.sleep(1)
                        st.rerun()
        else:
            st.warning("No players found for this match.")
    else:
        st.warning("No scheduled cricket matches available.")

with tab2:
    st.subheader("🏆 Orange Cap (Top Runs)")
    orange_cap_query = """
        SELECT p.Player_Name, t.Team_Name, SUM(sc.Runs_Scored) AS Total_Runs
        FROM Scorecard_Cricket sc
        JOIN Players p ON sc.Player_ID = p.Player_ID
        JOIN Teams t ON p.Team_ID = t.Team_ID
        GROUP BY sc.Player_ID
        ORDER BY Total_Runs DESC
    """
    orange_cap_data = run_query(orange_cap_query)

    if orange_cap_data:
        orange_cap_df = pd.DataFrame(orange_cap_data)
        col1, col2 = st.columns([1, 1.5])
        with col1:
            st.dataframe(orange_cap_df, use_container_width=True, hide_index=True)
        with col2:
            top_df = orange_cap_df.head(10)
            fig = px.bar(
                top_df, 
                x="Player_Name", 
                y="Total_Runs", 
                color="Team_Name",
                title="Top 10 Run Scorers",
                labels={"Player_Name": "Player", "Total_Runs": "Runs"}
            )
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available")

    st.divider()
    st.subheader("🔥 Player Form Status")
    form_query = """
        SELECT p.Player_Name, t.Team_Name, p.Form_Status 
        FROM Players p
        JOIN Teams t ON p.Team_ID = t.Team_ID
        WHERE t.Sport_ID = 1
    """
    form_data = run_query(form_query)
    
    if form_data:
        form_df = pd.DataFrame(form_data)
        def color_form(val):
            color = '#10b981' if val == 'In Form' else ('#ef4444' if val == 'Out of Form' else '')
            return f'color: {color}; font-weight: bold;'
            
        styled_form = form_df.style.map(color_form, subset=['Form_Status'])
        st.dataframe(styled_form, use_container_width=True, hide_index=True)
    else:
        st.info("No player data available.")