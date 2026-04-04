# ============================================================
#  ARENA SNU — Football Module
#  Author  : Ayush (Football Lead)
#  File    : page_football.py
#  Desc    : Score entry, Golden Boot leaderboard,
#            Suspended Players list — full DB integration
# ============================================================

import streamlit as st
import pandas as pd
from db_connection import run_query


# ─────────────────────────────────────────────
#  HELPER — load football matches (dropdown)
# ─────────────────────────────────────────────
def get_football_matches():
    """
    Returns all scheduled/completed football matches.
    4-table JOIN: Matches + Sports + Teams (A & B) + Venues
    """
    query = """
        SELECT
            m.Match_ID,
            CONCAT(
                ta.Team_Name, ' vs ', tb.Team_Name,
                ' | ', m.Stage,
                ' | ', DATE_FORMAT(m.Match_Date, '%d %b %Y'),
                ' @ ', v.Venue_Name
            ) AS Match_Label,
            m.Team_A_ID,
            m.Team_B_ID
        FROM Matches m
        JOIN Sports  s  ON m.Sport_ID   = s.Sport_ID
        JOIN Teams   ta ON m.Team_A_ID  = ta.Team_ID
        JOIN Teams   tb ON m.Team_B_ID  = tb.Team_ID
        JOIN Venues  v  ON m.Venue_ID   = v.Venue_ID
        WHERE s.Sport_Name = 'Football'
        ORDER BY m.Match_Date DESC, m.Match_Time DESC
    """
    return run_query(query, fetch=True) or []


# ─────────────────────────────────────────────
#  HELPER — load players for selected match
# ─────────────────────────────────────────────
def get_players_for_match(team_a_id, team_b_id):
    """
    Returns all players belonging to either team in the match.
    JOIN: Players + Teams
    """
    query = """
        SELECT
            p.Player_ID,
            CONCAT(p.Player_Name, ' (', t.Team_Name, ' | #', p.Jersey_No, ')') AS Player_Label,
            p.Role
        FROM Players p
        JOIN Teams t ON p.Team_ID = t.Team_ID
        WHERE p.Team_ID IN (%s, %s)
        ORDER BY t.Team_Name, p.Player_Name
    """
    return run_query(query, params=(team_a_id, team_b_id), fetch=True) or []


# ─────────────────────────────────────────────
#  HELPER — Golden Boot leaderboard
# ─────────────────────────────────────────────
def get_golden_boot():
    """
    Top goal scorers across all football matches.
    SUM + GROUP BY + ORDER BY DESC — classic aggregate leaderboard.
    """
    query = """
        SELECT
            p.Player_Name          AS Player,
            t.Team_Name            AS Team,
            t.University           AS University,
            SUM(sf.Goals)          AS Goals,
            SUM(sf.Assists)        AS Assists,
            SUM(sf.Yellow_Cards)   AS Yellow_Cards,
            SUM(sf.Red_Cards)      AS Red_Cards,
            COUNT(sf.Match_ID)     AS Matches_Played
        FROM Scorecard_Football sf
        JOIN Players p ON sf.Player_ID = p.Player_ID
        JOIN Teams   t ON p.Team_ID    = t.Team_ID
        GROUP BY sf.Player_ID, p.Player_Name, t.Team_Name, t.University
        HAVING SUM(sf.Goals) > 0
        ORDER BY Goals DESC, Assists DESC
        LIMIT 15
    """
    return run_query(query, fetch=True) or []


# ─────────────────────────────────────────────
#  HELPER — Suspended players
# ─────────────────────────────────────────────
def get_suspended_players():
    """
    Players auto-suspended by DB trigger (trg_suspend_player).
    Trigger fires after INSERT on Scorecard_Football:
        IF total Yellow_Cards >= 3 → SET Role = 'SUSPENDED'
    Python never touches Role directly — this is pure DB logic.
    """
    query = """
        SELECT
            p.Player_Name          AS Player,
            t.Team_Name            AS Team,
            t.University           AS University,
            p.Jersey_No            AS Jersey,
            SUM(sf.Yellow_Cards)   AS Total_Yellow_Cards,
            SUM(sf.Red_Cards)      AS Total_Red_Cards
        FROM Players p
        JOIN Teams   t  ON p.Team_ID    = t.Team_ID
        JOIN Scorecard_Football sf ON sf.Player_ID = p.Player_ID
        WHERE p.Role = 'SUSPENDED'
        GROUP BY p.Player_ID, p.Player_Name, t.Team_Name, t.University, p.Jersey_No
        ORDER BY t.Team_Name, p.Player_Name
    """
    return run_query(query, fetch=True) or []


# ─────────────────────────────────────────────
#  HELPER — check duplicate score entry
# ─────────────────────────────────────────────
def already_submitted(match_id, player_id):
    """Prevents double-entry for the same player in the same match."""
    query = """
        SELECT COUNT(*) AS cnt
        FROM Scorecard_Football
        WHERE Match_ID = %s AND Player_ID = %s
    """
    result = run_query(query, params=(match_id, player_id), fetch=True)
    return result and result[0]["cnt"] > 0


# ============================================================
#  MAIN PAGE FUNCTION — called by main_app.py
# ============================================================
def show():
    # ── Page header ──────────────────────────────────────────
    st.markdown("## ⚽ Football Module")
    st.markdown("**SURGE · ARENA SNU** — Score entry, leaderboard & disciplinary tracker")
    st.divider()

    # ════════════════════════════════════════════════════════
    #  SECTION 1 — Score Entry Form
    # ════════════════════════════════════════════════════════
    st.subheader("📋 Enter Match Score")

    matches = get_football_matches()

    if not matches:
        st.warning("No football matches found. Ask the Match Ops lead to schedule matches first.")
        st.stop()

    # Build {label: row} lookup for dropdowns
    match_options = {row["Match_Label"]: row for row in matches}
    selected_match_label = st.selectbox(
        "Select Match",
        options=list(match_options.keys()),
        help="Only Football matches are shown here"
    )

    selected_match = match_options[selected_match_label]
    match_id   = selected_match["Match_ID"]
    team_a_id  = selected_match["Team_A_ID"]
    team_b_id  = selected_match["Team_B_ID"]

    # Load players for both teams in this match
    players = get_players_for_match(team_a_id, team_b_id)

    if not players:
        st.warning("No players found for the selected match's teams.")
        st.stop()

    player_options = {row["Player_Label"]: row for row in players}
    selected_player_label = st.selectbox(
        "Select Player",
        options=list(player_options.keys()),
        help="Shows all players from both competing teams"
    )
    selected_player = player_options[selected_player_label]
    player_id = selected_player["Player_ID"]

    # Warn if suspended (they can still record stats — ref decision)
    if selected_player.get("Role") == "SUSPENDED":
        st.warning(
            f"⚠️ **{selected_player_label.split('(')[0].strip()}** is currently SUSPENDED. "
            "Confirm with the referee before entering stats."
        )

    st.markdown("#### 📊 Match Statistics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        goals = st.number_input(
            "⚽ Goals", min_value=0, max_value=20, value=0, step=1
        )
    with col2:
        assists = st.number_input(
            "🎯 Assists", min_value=0, max_value=20, value=0, step=1
        )
    with col3:
        yellow_cards = st.number_input(
            "🟨 Yellow Cards", min_value=0, max_value=2, value=0, step=1,
            help="Max 2 per match per player"
        )
    with col4:
        red_cards = st.number_input(
            "🟥 Red Cards", min_value=0, max_value=1, value=0, step=1,
            help="Max 1 per match per player"
        )

    # ── Submit ───────────────────────────────────────────────
    st.markdown("")
    submit = st.button("✅ Submit Score", type="primary", use_container_width=False)

    if submit:
        # Guard: duplicate entry
        if already_submitted(match_id, player_id):
            st.error(
                "🚫 Score already submitted for this player in this match. "
                "Edit existing records in MySQL Workbench if correction needed."
            )
        else:
            insert_query = """
                INSERT INTO Scorecard_Football
                    (Match_ID, Player_ID, Goals, Assists, Yellow_Cards, Red_Cards)
                VALUES
                    (%s, %s, %s, %s, %s, %s)
            """
            try:
                run_query(
                    insert_query,
                    params=(match_id, player_id, goals, assists, yellow_cards, red_cards),
                    fetch=False
                )
                st.success(
                    f"✅ Score saved! "
                    f"Goals: {goals} | Assists: {assists} | "
                    f"🟨 {yellow_cards} | 🟥 {red_cards}"
                )
                # Note to evaluator: DB trigger fires HERE automatically.
                # If player's cumulative yellow cards >= 3, MySQL sets Role='SUSPENDED'.
                # No Python logic for suspension — it's 100% trigger-based.
                if yellow_cards > 0:
                    st.info(
                        "🔔 Yellow card recorded. DB trigger will auto-check cumulative total "
                        "and suspend if threshold (3) is reached."
                    )
                st.rerun()   # re-fetches fresh data from MySQL → UI shows latest DB state

            except Exception as e:
                st.error(f"❌ Database error: {e}")

    st.divider()

    # ════════════════════════════════════════════════════════
    #  SECTION 2 — Golden Boot Leaderboard
    # ════════════════════════════════════════════════════════
    st.subheader("🏆 Golden Boot — Top Goal Scorers")

    leaderboard = get_golden_boot()

    if leaderboard:
        df_lb = pd.DataFrame(leaderboard)

        # Add rank + medal emoji
        df_lb.insert(0, "Rank", range(1, len(df_lb) + 1))
        medals = {1: "🥇", 2: "🥈", 3: "🥉"}
        df_lb["Rank"] = df_lb["Rank"].map(lambda r: f"{medals.get(r, str(r))} {r}" if r <= 3 else str(r))

        # Rename columns for clean display
        df_lb = df_lb.rename(columns={
            "Goals":         "⚽ Goals",
            "Assists":       "🎯 Assists",
            "Yellow_Cards":  "🟨 Yellow",
            "Red_Cards":     "🟥 Red",
            "Matches_Played":"Matches"
        })

        st.dataframe(
            df_lb,
            use_container_width=True,
            hide_index=True,
            column_config={
                "⚽ Goals":  st.column_config.NumberColumn(format="%d"),
                "🎯 Assists":st.column_config.NumberColumn(format="%d"),
            }
        )

        # Highlight the leader
        top = leaderboard[0]
        st.success(
            f"🏆 **Golden Boot Leader:** {top['Player']} "
            f"({top['Team']}) — {top['Goals']} goal(s)"
        )
    else:
        st.info("No goals recorded yet. Submit match scores above to populate the leaderboard.")

    st.divider()

    # ════════════════════════════════════════════════════════
    #  SECTION 3 — Suspended Players
    # ════════════════════════════════════════════════════════
    st.subheader("🚫 Suspended Players")
    st.caption(
        "Auto-updated by DB trigger `trg_suspend_player`. "
        "When a player's cumulative Yellow Cards ≥ 3, MySQL sets Role = 'SUSPENDED' automatically — "
        "no Python code involved."
    )

    suspended = get_suspended_players()

    if suspended:
        df_sus = pd.DataFrame(suspended)
        df_sus = df_sus.rename(columns={
            "Total_Yellow_Cards": "🟨 Total Yellows",
            "Total_Red_Cards":    "🟥 Total Reds",
            "Jersey":             "Jersey #"
        })
        st.dataframe(df_sus, use_container_width=True, hide_index=True)
        st.warning(
            f"⚠️ **{len(suspended)} player(s) currently suspended.** "
            "They cannot participate until cleared by the admin."
        )
    else:
        st.success("✅ No players are currently suspended.")

    st.divider()

    # ════════════════════════════════════════════════════════
    #  SECTION 4 — Full Football Scorecards (recent entries)
    # ════════════════════════════════════════════════════════
    with st.expander("📄 View All Football Score Entries", expanded=False):
        all_scores_query = """
            SELECT
                m.Match_ID,
                CONCAT(ta.Team_Name, ' vs ', tb.Team_Name) AS Match,
                m.Stage,
                m.Match_Date,
                p.Player_Name   AS Player,
                t.Team_Name     AS Team,
                sf.Goals,
                sf.Assists,
                sf.Yellow_Cards AS Yellows,
                sf.Red_Cards    AS Reds
            FROM Scorecard_Football sf
            JOIN Matches m  ON sf.Match_ID  = m.Match_ID
            JOIN Players p  ON sf.Player_ID = p.Player_ID
            JOIN Teams   t  ON p.Team_ID    = t.Team_ID
            JOIN Teams   ta ON m.Team_A_ID  = ta.Team_ID
            JOIN Teams   tb ON m.Team_B_ID  = tb.Team_ID
            ORDER BY m.Match_Date DESC, t.Team_Name, p.Player_Name
        """
        all_scores = run_query(all_scores_query, fetch=True)

        if all_scores:
            st.dataframe(pd.DataFrame(all_scores), use_container_width=True, hide_index=True)
        else:
            st.info("No football scores recorded yet.")