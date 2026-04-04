import streamlit as st
import time
import pandas as pd
from db_connection import run_query

try:
    st.set_page_config(page_title="Football — ARENA SNU", page_icon="⚽", layout="wide")
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
<h2 style="background:linear-gradient(90deg,#22c55e,#6c63ff);
   -webkit-background-clip:text;-webkit-text-fill-color:transparent;
   font-size:2rem;font-weight:800;margin:0">⚽ Football Module</h2>
<p style="color:#6b7a99;font-size:.875rem;margin-top:4px">Score Entry · Golden Boot · Suspension Tracker</p>
""", unsafe_allow_html=True)
st.divider()

user_role = st.session_state.get("role", "viewer")
CAN_ENTER = user_role in ("admin", "organiser")

def get_football_matches():
    return run_query("""
        SELECT m.Match_ID,
               CONCAT(ta.Team_Name,' vs ',tb.Team_Name,' | ',m.Stage,' | ',DATE_FORMAT(m.Match_Date,'%d %b %Y'),' @ ',v.Venue_Name) AS Match_Label,
               m.Team_A_ID, m.Team_B_ID
        FROM Matches m
        JOIN Sports s ON m.Sport_ID=s.Sport_ID
        JOIN Teams ta ON m.Team_A_ID=ta.Team_ID
        JOIN Teams tb ON m.Team_B_ID=tb.Team_ID
        JOIN Venues v ON m.Venue_ID=v.Venue_ID
        WHERE s.Sport_Name='Football'
        ORDER BY m.Match_Date DESC, m.Match_Time DESC
    """, fetch=True) or []

def get_players_for_match(team_a_id, team_b_id):
    return run_query("""
        SELECT p.Player_ID,
               CONCAT(p.Player_Name,' (',t.Team_Name,' | #',p.Jersey_No,')') AS Player_Label,
               p.Role
        FROM Players p JOIN Teams t ON p.Team_ID=t.Team_ID
        WHERE p.Team_ID IN (%s,%s)
        ORDER BY t.Team_Name, p.Player_Name
    """, params=(team_a_id, team_b_id), fetch=True) or []

def get_golden_boot():
    return run_query("""
        SELECT p.Player_Name AS Player, t.Team_Name AS Team, t.University,
               SUM(sf.Goals) AS Goals, SUM(sf.Assists) AS Assists,
               SUM(sf.Yellow_Cards) AS Yellow_Cards, SUM(sf.Red_Cards) AS Red_Cards,
               COUNT(sf.Match_ID) AS Matches_Played
        FROM Scorecard_Football sf
        JOIN Players p ON sf.Player_ID=p.Player_ID
        JOIN Teams t ON p.Team_ID=t.Team_ID
        GROUP BY sf.Player_ID, p.Player_Name, t.Team_Name, t.University
        HAVING SUM(sf.Goals) > 0
        ORDER BY Goals DESC, Assists DESC LIMIT 15
    """, fetch=True) or []

def get_suspended_players():
    return run_query("""
        SELECT p.Player_Name AS Player, t.Team_Name AS Team, t.University,
               p.Jersey_No AS Jersey,
               SUM(sf.Yellow_Cards) AS Total_Yellow_Cards, SUM(sf.Red_Cards) AS Total_Red_Cards
        FROM Players p
        JOIN Teams t ON p.Team_ID=t.Team_ID
        JOIN Scorecard_Football sf ON sf.Player_ID=p.Player_ID
        WHERE p.Role='SUSPENDED'
        GROUP BY p.Player_ID, p.Player_Name, t.Team_Name, t.University, p.Jersey_No
        ORDER BY t.Team_Name, p.Player_Name
    """, fetch=True) or []

# ── SCORE ENTRY (organiser/admin only) ──────────────────────
if CAN_ENTER:
    st.subheader("📋 Enter Match Score")
    matches = get_football_matches()

    if not matches:
        st.warning("No football matches found.")
    else:
        match_options = {row["Match_Label"]: row for row in matches}
        selected_match = match_options[st.selectbox("Select Match", list(match_options.keys()))]
        match_id = selected_match["Match_ID"]

        players = get_players_for_match(selected_match["Team_A_ID"], selected_match["Team_B_ID"])
        if not players:
            st.warning("No players found for the selected match.")
        else:
            player_options   = {row["Player_Label"]: row for row in players}
            selected_player  = player_options[st.selectbox("Select Player", list(player_options.keys()))]
            player_id        = selected_player["Player_ID"]

            if selected_player.get("Role") == "SUSPENDED":
                st.warning(f"⚠️ This player is SUSPENDED. Confirm with referee before entering stats.")

            with st.form("football_score"):
                c1, c2, c3, c4 = st.columns(4)
                with c1: goals        = st.number_input("⚽ Goals",       min_value=0, max_value=20, value=0)
                with c2: assists      = st.number_input("🎯 Assists",     min_value=0, max_value=20, value=0)
                with c3: yellow_cards = st.number_input("🟨 Yellow Cards",min_value=0, max_value=2,  value=0)
                with c4: red_cards    = st.number_input("🟥 Red Cards",   min_value=0, max_value=1,  value=0)

                if st.form_submit_button("✅ Submit Score", type="primary"):
                    existing = run_query("SELECT COUNT(*) AS cnt FROM Scorecard_Football WHERE Match_ID=%s AND Player_ID=%s",
                                         (match_id, player_id), fetch=True)
                    if existing and existing[0]["cnt"] > 0:
                        st.error("🚫 Score already submitted for this player in this match.")
                    else:
                        with st.spinner("Recording to MySQL…"):
                            run_query("""INSERT INTO Scorecard_Football
                                        (Match_ID,Player_ID,Goals,Assists,Yellow_Cards,Red_Cards)
                                        VALUES (%s,%s,%s,%s,%s,%s)""",
                                      params=(match_id,player_id,goals,assists,yellow_cards,red_cards), fetch=False)
                            time.sleep(0.4)
                        st.toast("Score saved!", icon="✅")
                        time.sleep(1)
                        st.rerun()

    st.divider()
else:
    st.info("🔒 Score entry is restricted to **Organisers**. Contact an admin to get access.")
    st.divider()

# ── LEADERBOARDS (everyone) ────────────────────────────────
st.subheader("🏆 Golden Boot — Top Goal Scorers")
leaderboard = get_golden_boot()
if leaderboard:
    df_lb = pd.DataFrame(leaderboard)
    df_lb.insert(0, "Rank", range(1, len(df_lb)+1))
    medals = {1:"🥇",2:"🥈",3:"🥉"}
    df_lb["Rank"] = df_lb["Rank"].map(lambda r: f"{medals.get(r,str(r))} {r}" if r<=3 else str(r))
    df_lb = df_lb.rename(columns={"Goals":"⚽ Goals","Assists":"🎯 Assists",
                                   "Yellow_Cards":"🟨 Yellow","Red_Cards":"🟥 Red","Matches_Played":"Matches"})
    st.dataframe(df_lb, use_container_width=True, hide_index=True)
else:
    st.info("No goals recorded yet.")

st.divider()
st.subheader("🚫 Suspended Players")
suspended = get_suspended_players()
if suspended:
    df_sus = pd.DataFrame(suspended).rename(columns={"Total_Yellow_Cards":"🟨 Total Yellows",
                                                       "Total_Red_Cards":"🟥 Total Reds","Jersey":"Jersey #"})
    st.dataframe(df_sus, use_container_width=True, hide_index=True)
else:
    st.success("✅ No players are currently suspended.")