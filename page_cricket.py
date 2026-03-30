import streamlit as st
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="A5HANK",
        database="ARENA_SNU"
    )

def run():
    st.title("🏏 Cricket Module")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT Match_ID FROM Matches WHERE Sport_ID = 1")
    matches = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT Player_ID, Player_Name FROM Players")
    players = cursor.fetchall()
    player_dict = {p[1]: p[0] for p in players}

    st.subheader("Add Cricket Score")

    match_id = st.selectbox("Select Match", matches)
    player_name = st.selectbox("Select Player", list(player_dict.keys()))

    runs = st.number_input("Runs Scored", min_value=0)
    wickets = st.number_input("Wickets Taken", min_value=0)
    overs_options = []

    for over in range(0, 5):  # 0 to 4 overs
        for ball in range(0, 6):  # 0 to 5 balls
            overs_options.append(f"{over}.{ball}")

    selected_overs = st.selectbox("Overs Bowled", overs_options)
    catches = st.number_input("Catches", min_value=0)

    if st.button("Submit Score"):
        try:
            cursor.execute("""
                INSERT INTO Scorecard_Cricket
                (Match_ID, Player_ID, Runs_Scored, Wickets_Taken, Overs_Bowled, Catches)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (match_id, player_dict[player_name], runs, wickets, float(selected_overs), catches))

            conn.commit()
            st.success("✅ Score added successfully!")

        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("🏆 Orange Cap (Top Runs)")

    cursor.execute("""
        SELECT p.Player_Name, t.Team_Name, SUM(sc.Runs_Scored) AS Total_Runs
        FROM Scorecard_Cricket sc
        JOIN Players p ON sc.Player_ID = p.Player_ID
        JOIN Teams t ON p.Team_ID = t.Team_ID
        GROUP BY sc.Player_ID
        ORDER BY Total_Runs DESC
    """)

    results = cursor.fetchall()

    if results:
        st.table(results)
    else:
        st.write("No data available")

    st.subheader("🔥 Player Form Status")

    cursor.execute("""
        SELECT Player_Name, Form_Status FROM Players
    """)

    form_data = cursor.fetchall()
    st.table(form_data)

    cursor.close()
    conn.close()

run()