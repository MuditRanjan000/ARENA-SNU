# page_cricket.py — ARENA SNU Cricket Module (v5)
# Assigned: Ashank | Reviewed & improved: Mudit
import streamlit as st
import time
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from db_connection import run_query

try:
    st.set_page_config(page_title="Cricket — ARENA SNU", page_icon="🏏", layout="wide")
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
<h2 style="background:linear-gradient(90deg,#a855f7,#6c63ff);
   -webkit-background-clip:text;-webkit-text-fill-color:transparent;
   font-size:2rem;font-weight:800;margin:0">🏏 Cricket Module</h2>
<p style="color:#6b7a99;font-size:.875rem;margin-top:4px">T20 Format · Score Entry · Leaderboards · Player Form</p>
""", unsafe_allow_html=True)
st.divider()

# Role check — organisers get score entry tab, others only see leaderboards
user_role = st.session_state.get("role", "viewer")
CAN_ENTER = user_role in ("admin", "organiser")

tabs = ["📝 Enter Score", "📊 Leaderboards", "🔥 Player Form"] if CAN_ENTER else ["📊 Leaderboards", "🔥 Player Form"]
tab_list = st.tabs(tabs)

tab_entry  = tab_list[0] if CAN_ENTER else None
tab_boards = tab_list[1] if CAN_ENTER else tab_list[0]
tab_form   = tab_list[2] if CAN_ENTER else tab_list[1]

# ═══════════════════════ TAB: SCORE ENTRY ═══════════════════
if CAN_ENTER:
    with tab_entry:
        matches_data = run_query("""
            SELECT m.Match_ID,
                   CONCAT(ta.Team_Name, ' vs ', tb.Team_Name, '  (', m.Match_Date, ')  [', m.Stage, ']') AS Match_Desc
            FROM Matches m
            JOIN Teams ta ON m.Team_A_ID=ta.Team_ID
            JOIN Teams tb ON m.Team_B_ID=tb.Team_ID
            WHERE m.Sport_ID=1 AND m.Status='Scheduled'
            ORDER BY m.Match_Date
        """)

        if not matches_data:
            st.warning("⚠️ No scheduled cricket matches available. Schedule a match first.")
        else:
            match_df   = pd.DataFrame(matches_data)
            match_dict = dict(zip(match_df["Match_Desc"], match_df["Match_ID"]))
            selected_match_desc = st.selectbox("Select Match", list(match_dict.keys()))
            match_id = match_dict[selected_match_desc]

            players_data = run_query(f"""
                SELECT p.Player_ID,
                       CONCAT(p.Player_Name, '  (', t.Team_Name, ')  — ', p.Role) AS Player_Desc
                FROM Players p
                JOIN Teams t ON p.Team_ID=t.Team_ID
                JOIN Matches m ON (t.Team_ID=m.Team_A_ID OR t.Team_ID=m.Team_B_ID)
                WHERE m.Match_ID={match_id}
                ORDER BY t.Team_Name, p.Player_Name
            """)

            if not players_data:
                st.warning("⚠️ No players found for this match.")
            else:
                player_df   = pd.DataFrame(players_data)
                player_dict = dict(zip(player_df["Player_Desc"], player_df["Player_ID"]))
                selected_player_desc = st.selectbox("Select Player", list(player_dict.keys()))
                player_id = player_dict[selected_player_desc]

                existing = run_query(f"""
                    SELECT Runs_Scored, Wickets_Taken, Overs_Bowled, Catches
                    FROM Scorecard_Cricket
                    WHERE Match_ID={match_id} AND Player_ID={player_id}
                """)
                if existing:
                    ex = existing[0]
                    st.markdown("""<div style="padding:10px 16px;border-radius:8px;border-left:3px solid #f59e0b;
                    background:rgba(245,158,11,.07);font-size:13px;margin-bottom:8px">
                        ⚠️ Entry already exists. Submitting will add another record.</div>""",
                    unsafe_allow_html=True)
                    st.caption(f"Existing → Runs: {ex['Runs_Scored']} | Wickets: {ex['Wickets_Taken']} | Overs: {ex['Overs_Bowled']} | Catches: {ex['Catches']}")

                with st.form("score_form", clear_on_submit=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        runs    = st.number_input("Runs Scored",   min_value=0, max_value=200)
                        wickets = st.number_input("Wickets Taken", min_value=0, max_value=10)
                    with col2:
                        overs   = st.number_input("Overs Bowled",  min_value=0.0, max_value=20.0, step=0.1)
                        catches = st.number_input("Catches",       min_value=0, max_value=10)

                    submitted = st.form_submit_button("🏏 Submit Score", use_container_width=True)

                if submitted:
                    over_decimal = round(overs % 1, 1)
                    if over_decimal > 0.5:
                        st.error("❌ Invalid overs — decimal must be 0–5 (e.g. 3.4, not 3.7)")
                    else:
                        with st.spinner("Recording to MySQL…"):
                            run_query(
                                "INSERT INTO Scorecard_Cricket "
                                "(Match_ID, Player_ID, Runs_Scored, Wickets_Taken, Overs_Bowled, Catches) "
                                "VALUES (%s, %s, %s, %s, %s, %s)",
                                (match_id, player_id, runs, wickets, overs, catches), fetch=False
                            )
                            time.sleep(0.5)
                        st.toast("Score recorded! Form status auto-updated by trigger.", icon="✅")
                        time.sleep(1)
                        st.rerun()

else:
    # Non-organiser attempting score entry → show notice
    pass  # Tab is hidden for non-organisers

# ════════════════════════ TAB: LEADERBOARDS ═════════════════
with tab_boards:
    board_left, board_right = st.columns(2)

    with board_left:
        st.subheader("🏅 Orange Cap — Top Runs")
        oc_data = run_query("""
            SELECT p.Player_Name, t.Team_Name, t.University,
                   SUM(sc.Runs_Scored) AS Runs,
                   COUNT(DISTINCT sc.Match_ID) AS Innings
            FROM Scorecard_Cricket sc
            JOIN Players p ON sc.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID
            GROUP BY sc.Player_ID ORDER BY Runs DESC
        """)
        if oc_data:
            oc_df = pd.DataFrame(oc_data)
            oc_df.insert(0, "Rank", range(1, len(oc_df) + 1))
            def hl_top(row): return ["background-color:rgba(168,85,247,.12)"]*len(row) if row["Rank"]==1 else [""]*len(row)
            st.dataframe(oc_df.style.apply(hl_top, axis=1), use_container_width=True, hide_index=True)
            fig = px.bar(oc_df.head(8), x="Player_Name", y="Runs", color="Team_Name",
                         color_discrete_sequence=px.colors.qualitative.Vivid,
                         labels={"Player_Name":"Player","Runs":"Total Runs"}, title="Top Run Scorers")
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              font_color="#e8ecf4", showlegend=False, margin=dict(t=36,b=0,l=0,r=0),
                              xaxis=dict(gridcolor="#252c3d"), yaxis=dict(gridcolor="#252c3d"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No batting data yet.")

    with board_right:
        st.subheader("💜 Purple Cap — Top Wickets")
        pc_data = run_query("""
            SELECT p.Player_Name, t.Team_Name,
                   SUM(sc.Wickets_Taken) AS Wickets,
                   ROUND(SUM(sc.Overs_Bowled),1) AS Overs_Bowled
            FROM Scorecard_Cricket sc
            JOIN Players p ON sc.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID
            GROUP BY sc.Player_ID HAVING Wickets > 0 ORDER BY Wickets DESC
        """)
        if pc_data:
            pc_df = pd.DataFrame(pc_data)
            pc_df.insert(0, "Rank", range(1, len(pc_df) + 1))
            def hl_top_pc(row): return ["background-color:rgba(168,85,247,.12)"]*len(row) if row["Rank"]==1 else [""]*len(row)
            st.dataframe(pc_df.style.apply(hl_top_pc, axis=1), use_container_width=True, hide_index=True)
            fig2 = px.bar(pc_df.head(8), x="Player_Name", y="Wickets", color="Team_Name",
                          color_discrete_sequence=["#a855f7","#8b5cf6","#7c3aed","#6d28d9"],
                          labels={"Player_Name":"Player","Wickets":"Total Wickets"}, title="Top Wicket Takers")
            fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               font_color="#e8ecf4", showlegend=False, margin=dict(t=36,b=0,l=0,r=0),
                               xaxis=dict(gridcolor="#252c3d"), yaxis=dict(gridcolor="#252c3d"))
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No bowling data yet.")

    st.divider()
    with st.expander("📋 Full Scorecard — All Players"):
        full_data = run_query("""
            SELECT p.Player_Name, t.Team_Name,
                   SUM(sc.Runs_Scored) AS Total_Runs, SUM(sc.Wickets_Taken) AS Total_Wickets,
                   ROUND(SUM(sc.Overs_Bowled),1) AS Total_Overs, SUM(sc.Catches) AS Total_Catches,
                   COUNT(DISTINCT sc.Match_ID) AS Matches
            FROM Scorecard_Cricket sc
            JOIN Players p ON sc.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID
            GROUP BY sc.Player_ID ORDER BY Total_Runs DESC
        """)
        if full_data:
            st.dataframe(pd.DataFrame(full_data), use_container_width=True, hide_index=True)
        else:
            st.info("No scorecard data available.")

# ════════════════════════ TAB: PLAYER FORM ══════════════════
with tab_form:
    st.subheader("🔥 Player Form Tracker")
    st.markdown("""
    <div style="padding:10px 16px;border-radius:8px;border-left:3px solid #6c63ff;
    background:rgba(108,99,255,.07);font-size:13px;margin-bottom:16px">
        Form is updated by <strong>trg_player_form</strong> after every score entry.
        🟢 In Form = last-5 avg ≥ 120% of overall · 🔴 Out of Form = ≤ 80%
    </div>""", unsafe_allow_html=True)

    form_data = run_query("""
        SELECT p.Player_Name, t.Team_Name, p.Form_Status,
               IFNULL(ROUND(AVG(sc.Runs_Scored),1),'—') AS Avg_Runs,
               IFNULL(SUM(sc.Wickets_Taken),0) AS Wickets
        FROM Players p
        JOIN Teams t ON p.Team_ID=t.Team_ID
        LEFT JOIN Scorecard_Cricket sc ON sc.Player_ID=p.Player_ID
        WHERE t.Sport_ID=1
        GROUP BY p.Player_ID
        ORDER BY CASE p.Form_Status WHEN 'In Form' THEN 1 WHEN 'Neutral' THEN 2 ELSE 3 END, Avg_Runs DESC
    """)

    if form_data:
        form_df = pd.DataFrame(form_data)
        form_df["Status"] = form_df["Form_Status"].map({
            "In Form":"🔥 In Form","Out of Form":"❄️ Out of Form","Neutral":"➖ Neutral"
        }).fillna("➖ Neutral")
        def color_status(val):
            if "In Form" in str(val):     return "color:#10b981;font-weight:bold"
            if "Out of Form" in str(val): return "color:#ef4444;font-weight:bold"
            return "color:#6b7a99"
        st.dataframe(form_df[["Player_Name","Team_Name","Status","Avg_Runs","Wickets"]]
                     .style.map(color_status, subset=["Status"]),
                     use_container_width=True, hide_index=True)
    else:
        st.info("No player data available.")