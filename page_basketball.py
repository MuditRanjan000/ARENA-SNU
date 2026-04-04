import streamlit as st
import time
import pandas as pd
import plotly.express as px
from db_connection import run_query

st.title("🏀 Basketball Module")

# Tabs
tab1, tab2 = st.tabs(["📝 Enter Stats", "📊 Leaderboards"])

# ─────────────────────────────
# 📝 TAB 1: ENTER STATS
# ─────────────────────────────
with tab1:

    st.subheader("Enter Player Stats")

    matches = run_query("SELECT Match_ID FROM matches", fetch=True)
    players = run_query("SELECT Player_ID, Player_Name FROM players", fetch=True)

    if not matches or not players:
        st.warning("⚠️ Matches or Players not found in DB")
        st.stop()

    match_list = [m["Match_ID"] for m in matches]
    player_dict = {p["Player_Name"]: p["Player_ID"] for p in players}

    selected_match = st.selectbox("Select Match", match_list)
    selected_player = st.selectbox("Select Player", list(player_dict.keys()))

    col1, col2 = st.columns(2)

    with col1:
        points = st.number_input("Points", 0, 100)
        rebounds = st.number_input("Rebounds", 0, 50)

    with col2:
        assists = st.number_input("Assists", 0, 30)
        steals = st.number_input("Steals", 0, 20)

    if st.button("Submit Stats"):
        run_query("""
            INSERT INTO scorecard_basketball
            (Match_ID, Player_ID, Points, Rebounds, Assists, Steals)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            selected_match,
            player_dict[selected_player],
            points,
            rebounds,
            assists,
            steals
        ), fetch=False)

        st.success("✅ Stats Added Successfully")
        time.sleep(1)
        st.rerun()


# ─────────────────────────────
# 📊 TAB 2: LEADERBOARD
# ─────────────────────────────
with tab2:

    st.subheader("🏆 Top Basketball Players")

    # 🔥 FINAL SQL QUERY (WITH STEALS)
    data = run_query("""
        SELECT 
            p.Player_Name,
            SUM(sb.Points) AS Total_Points,
            SUM(sb.Rebounds) AS Total_Rebounds,
            SUM(sb.Assists) AS Total_Assists,
            SUM(sb.Steals) AS Total_Steals
        FROM scorecard_basketball sb
        JOIN players p ON sb.Player_ID = p.Player_ID
        GROUP BY sb.Player_ID
        ORDER BY Total_Points DESC
    """, fetch=True)

    if data:
        df = pd.DataFrame(data)

        # Add Rank
        df.insert(0, "Rank", range(1, len(df)+1))

        # Show Table
        st.dataframe(df, use_container_width=True, hide_index=True)

        # 📊 Chart
        st.subheader("📊 Performance Comparison")

        fig = px.bar(
            df.head(10),
            x="Player_Name",
            y=[
                "Total_Points",
                "Total_Rebounds",
                "Total_Assists",
                "Total_Steals"
            ],
            barmode="group",
            title="Top Players Performance"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No basketball data available yet")