# page_cricket.py — ARENA SNU Cricket Module (v2)
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

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
    div.stButton > button {
        background: linear-gradient(90deg, #6c63ff, #a855f7);
        color: white; font-weight: 700; border-radius: 8px;
        border: none; transition: all .3s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 20px rgba(108,99,255,.45);
    }
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

tab_entry, tab_boards, tab_form = st.tabs([
    "📝 Enter Score", "📊 Leaderboards", "🔥 Player Form"
])

# ═══════════════════════ TAB 1: SCORE ENTRY ═══════════════════
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
        st.stop()

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
        st.warning("⚠️ No players found for this match. Register players for these teams first.")
        st.stop()

    player_df   = pd.DataFrame(players_data)
    player_dict = dict(zip(player_df["Player_Desc"], player_df["Player_ID"]))

    selected_player_desc = st.selectbox("Select Player", list(player_dict.keys()))
    player_id = player_dict[selected_player_desc]

    # Show existing entry for this player+match if any
    existing = run_query(f"""
        SELECT Runs_Scored, Wickets_Taken, Overs_Bowled, Catches
        FROM Scorecard_Cricket
        WHERE Match_ID={match_id} AND Player_ID={player_id}
    """)
    if existing:
        st.markdown("""
        <div style="padding:10px 16px;border-radius:8px;border-left:3px solid #f59e0b;
        background:rgba(245,158,11,.07);font-size:13px;margin-bottom:8px">
            ⚠️ A scorecard entry already exists for this player in this match.
            Submitting again will add a new record.
        </div>""", unsafe_allow_html=True)
        ex = existing[0]
        st.caption(
            f"Existing entry → Runs: {ex['Runs_Scored']} | "
            f"Wickets: {ex['Wickets_Taken']} | "
            f"Overs: {ex['Overs_Bowled']} | "
            f"Catches: {ex['Catches']}"
        )

    with st.form("score_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            runs    = st.number_input("Runs Scored", min_value=0, max_value=200,
                                       help="Maximum realistic innings score")
            wickets = st.number_input("Wickets Taken", min_value=0, max_value=10,
                                       help="Max 10 wickets per innings")
        with col2:
            overs   = st.number_input("Overs Bowled", min_value=0.0, max_value=20.0, step=0.1,
                                       help="T20 max is 20 overs")
            catches = st.number_input("Catches", min_value=0, max_value=10)

        submitted = st.form_submit_button("🏏 Submit Score", use_container_width=True)

    if submitted:
        # Validate overs format (legal values: x.0 to x.5 only)
        over_decimal = round(overs % 1, 1)
        if over_decimal > 0.5:
            st.error("❌ Invalid overs value — decimal part must be 0–5 (e.g. 3.4, not 3.7)")
        else:
            with st.spinner("Recording to MySQL…"):
                run_query(
                    "INSERT INTO Scorecard_Cricket "
                    "(Match_ID, Player_ID, Runs_Scored, Wickets_Taken, Overs_Bowled, Catches) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (match_id, player_id, runs, wickets, overs, catches),
                    fetch=False
                )
                time.sleep(0.5)
            st.toast("Score recorded! Form status auto-updated by trigger.", icon="✅")
            time.sleep(1)
            st.rerun()


# ════════════════════════ TAB 2: LEADERBOARDS ═════════════════
with tab_boards:
    board_left, board_right = st.columns(2)

    # ── Orange Cap ───────────────────────────────────────────
    with board_left:
        st.subheader("🏅 Orange Cap — Top Runs")
        oc_data = run_query("""
            SELECT p.Player_Name, t.Team_Name, t.University,
                   SUM(sc.Runs_Scored) AS Runs,
                   COUNT(DISTINCT sc.Match_ID) AS Innings
            FROM Scorecard_Cricket sc
            JOIN Players p ON sc.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID
            GROUP BY sc.Player_ID
            ORDER BY Runs DESC
        """)
        if oc_data:
            oc_df = pd.DataFrame(oc_data)
            oc_df.insert(0, "Rank", range(1, len(oc_df) + 1))

            # Highlight top row
            def hl_top(row):
                if row["Rank"] == 1:
                    return ["background-color:rgba(168,85,247,.12)"] * len(row)
                return [""] * len(row)

            st.dataframe(
                oc_df.style.apply(hl_top, axis=1),
                use_container_width=True, hide_index=True
            )

            fig = px.bar(
                oc_df.head(8), x="Player_Name", y="Runs", color="Team_Name",
                color_discrete_sequence=px.colors.qualitative.Vivid,
                labels={"Player_Name": "Player", "Runs": "Total Runs"},
                title="Top Run Scorers"
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="#e8ecf4", showlegend=False,
                margin=dict(t=36, b=0, l=0, r=0),
                xaxis=dict(gridcolor="#252c3d"),
                yaxis=dict(gridcolor="#252c3d"),
            )
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No batting data yet.")

    # ── Purple Cap ───────────────────────────────────────────
    with board_right:
        st.subheader("💜 Purple Cap — Top Wickets")
        pc_data = run_query("""
            SELECT p.Player_Name, t.Team_Name, t.University,
                   SUM(sc.Wickets_Taken) AS Wickets,
                   ROUND(SUM(sc.Overs_Bowled), 1) AS Overs_Bowled
            FROM Scorecard_Cricket sc
            JOIN Players p ON sc.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID
            GROUP BY sc.Player_ID
            HAVING Wickets > 0
            ORDER BY Wickets DESC
        """)
        if pc_data:
            pc_df = pd.DataFrame(pc_data)
            pc_df.insert(0, "Rank", range(1, len(pc_df) + 1))

            def hl_top_pc(row):
                if row["Rank"] == 1:
                    return ["background-color:rgba(168,85,247,.12)"] * len(row)
                return [""] * len(row)

            st.dataframe(
                pc_df.style.apply(hl_top_pc, axis=1),
                use_container_width=True, hide_index=True
            )

            fig2 = px.bar(
                pc_df.head(8), x="Player_Name", y="Wickets", color="Team_Name",
                color_discrete_sequence=["#a855f7", "#8b5cf6", "#7c3aed", "#6d28d9",
                                         "#5b21b6", "#4c1d95", "#3b0764"],
                labels={"Player_Name": "Player", "Wickets": "Total Wickets"},
                title="Top Wicket Takers"
            )
            fig2.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="#e8ecf4", showlegend=False,
                margin=dict(t=36, b=0, l=0, r=0),
                xaxis=dict(gridcolor="#252c3d"),
                yaxis=dict(gridcolor="#252c3d"),
            )
            fig2.update_traces(marker_line_width=0)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No bowling data yet.")

    # ── All-Rounder Stats (catches + combined) ────────────────
    st.divider()
    with st.expander("📋 Full Scorecard — All Players"):
        full_data = run_query("""
            SELECT p.Player_Name, t.Team_Name,
                   SUM(sc.Runs_Scored)   AS Total_Runs,
                   SUM(sc.Wickets_Taken) AS Total_Wickets,
                   ROUND(SUM(sc.Overs_Bowled), 1) AS Total_Overs,
                   SUM(sc.Catches)       AS Total_Catches,
                   COUNT(DISTINCT sc.Match_ID) AS Matches
            FROM Scorecard_Cricket sc
            JOIN Players p ON sc.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID
            GROUP BY sc.Player_ID
            ORDER BY Total_Runs DESC
        """)
        if full_data:
            st.dataframe(pd.DataFrame(full_data), use_container_width=True, hide_index=True)
        else:
            st.info("No scorecard data available.")


# ════════════════════════ TAB 3: PLAYER FORM ══════════════════
with tab_form:
    st.subheader("🔥 Player Form Tracker")
    st.markdown("""
    <div style="padding:10px 16px;border-radius:8px;border-left:3px solid #6c63ff;
    background:rgba(108,99,255,.07);font-size:13px;margin-bottom:16px">
        Form status is updated automatically by <strong>trg_player_form</strong> after every
        score entry — compares last 5 match average vs overall average.
        🟢 In Form = last 5 avg ≥ 120% of overall · 🔴 Out of Form = ≤ 80%
    </div>
    """, unsafe_allow_html=True)

    form_data = run_query("""
        SELECT p.Player_Name, t.Team_Name,
               p.Form_Status,
               IFNULL(ROUND(AVG(sc.Runs_Scored),1), '—') AS Avg_Runs,
               IFNULL(SUM(sc.Wickets_Taken), 0)          AS Wickets
        FROM Players p
        JOIN Teams t ON p.Team_ID=t.Team_ID
        LEFT JOIN Scorecard_Cricket sc ON sc.Player_ID=p.Player_ID
        WHERE t.Sport_ID=1
        GROUP BY p.Player_ID
        ORDER BY
            CASE p.Form_Status WHEN 'In Form' THEN 1 WHEN 'Neutral' THEN 2 ELSE 3 END,
            Avg_Runs DESC
    """)

    if form_data:
        form_df = pd.DataFrame(form_data)

        # Add icon column
        form_df["Status"] = form_df["Form_Status"].map({
            "In Form":     "🔥 In Form",
            "Out of Form": "❄️ Out of Form",
            "Neutral":     "➖ Neutral"
        }).fillna("➖ Neutral")

        def color_status(val):
            if "In Form"     in str(val): return "color:#10b981;font-weight:bold"
            if "Out of Form" in str(val): return "color:#ef4444;font-weight:bold"
            return "color:#6b7a99"

        display_df = form_df[["Player_Name", "Team_Name", "Status", "Avg_Runs", "Wickets"]]
        st.dataframe(
            display_df.style.map(color_status, subset=["Status"]),
            use_container_width=True, hide_index=True
        )

        # Form summary chart
        st.divider()
        summary = form_df["Form_Status"].value_counts().reset_index()
        summary.columns = ["Form_Status", "Count"]
        color_map = {
            "In Form":     "#10b981",
            "Neutral":     "#6b7a99",
            "Out of Form": "#ef4444"
        }
        fig = px.pie(
            summary, names="Form_Status", values="Count",
            color="Form_Status", color_discrete_map=color_map,
            title="Squad Form Distribution",
            hole=0.45
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#e8ecf4", margin=dict(t=36, b=0)
        )
        col_pie, col_space = st.columns([1, 1.5])
        with col_pie:
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No player data available.")