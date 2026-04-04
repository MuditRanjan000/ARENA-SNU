# home_page.py — ARENA SNU Dashboard (v2)
# System Architect: Mudit
import streamlit as st
import time
import plotly.express as px
import pandas as pd
from db_connection import run_query, call_procedure

try:
    st.set_page_config(page_title="ARENA SNU", page_icon="🏆", layout="wide")
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
    [data-testid="stMetric"] {
        background: #1c2030; border: 1px solid #252c3d;
        border-radius: 12px; padding: 16px 20px;
        border-top: 3px solid #6c63ff;
    }
    .stTabs [data-baseweb="tab"] { font-weight: 600; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────
st.markdown("""
<div style="padding:24px 0 8px">
  <h1 style="background:linear-gradient(90deg,#6c63ff,#a855f7);
     -webkit-background-clip:text;-webkit-text-fill-color:transparent;
     font-size:2.4rem;font-weight:800;letter-spacing:-1px;margin:0">
     🏆 ARENA SNU</h1>
  <p style="color:#6b7a99;font-size:.9rem;margin-top:4px">
     Athletic Resource &amp; Event Navigation Application ·
     SURGE Sports Festival · Shiv Nadar University</p>
</div>
""", unsafe_allow_html=True)
st.divider()

role = st.session_state.get("role", "viewer")
can_edit = role in ("admin", "manager")

tab_labels = ["📊 Dashboard", "🏟️ Team Management", "👤 Player Management"]
if can_edit:
    tab_labels.insert(1, "🏆 Match Results")

tabs = st.tabs(tab_labels)
tab1 = tabs[0]
tab_results = tabs[1] if can_edit else None
tab_teams   = tabs[2] if can_edit else tabs[1]
tab_players = tabs[3] if can_edit else tabs[2]

# ═══════════════════════ TAB 1: DASHBOARD ═════════════════════
with tab1:
    c1, c2, c3, c4, c5 = st.columns(5)
    sports_cnt    = run_query("SELECT COUNT(*) AS cnt FROM Sports")
    teams_cnt     = run_query("SELECT COUNT(*) AS cnt FROM Teams")
    players_cnt   = run_query("SELECT COUNT(*) AS cnt FROM Players")
    matches_cnt   = run_query("SELECT COUNT(*) AS cnt FROM Matches")
    completed_cnt = run_query("SELECT COUNT(*) AS cnt FROM Matches WHERE Status='Completed'")
    scheduled_cnt = run_query("SELECT COUNT(*) AS cnt FROM Matches WHERE Status='Scheduled'")

    c1.metric("🏅 Sports",     sports_cnt[0]["cnt"]    if sports_cnt    else 0)
    c2.metric("🏟️ Teams",     teams_cnt[0]["cnt"]     if teams_cnt     else 0)
    c3.metric("👤 Players",   players_cnt[0]["cnt"]   if players_cnt   else 0)
    c4.metric("📅 Matches",   matches_cnt[0]["cnt"]   if matches_cnt   else 0)
    c5.metric("✅ Completed", completed_cnt[0]["cnt"] if completed_cnt else 0,
              delta=f"{scheduled_cnt[0]['cnt'] if scheduled_cnt else 0} scheduled")

    st.divider()

    # ── Points Table with sport filter ───────────────────────
    st.subheader("🏆 Tournament Standings")
    points_data = run_query(
        "SELECT Team_Name, University, Sport_Name, Matches_Played, Wins, Losses, Points FROM Points_Table"
    )

    if points_data:
        points_df = pd.DataFrame(points_data)
        sport_options = ["All Sports"] + sorted(points_df["Sport_Name"].unique().tolist())
        col_filter, _ = st.columns([1, 3])
        with col_filter:
            sport_filter = st.selectbox("Filter by sport", sport_options, label_visibility="collapsed")

        filtered = points_df if sport_filter == "All Sports" \
                   else points_df[points_df["Sport_Name"] == sport_filter]

        if not filtered.empty:
            leader = filtered.iloc[0]
            st.markdown(f"""
                <div style="padding:12px 18px;border-radius:10px;border-left:4px solid #f5a623;
                background:rgba(245,166,35,.08);margin-bottom:16px;font-size:14px">
                    🏆 <strong>Leader:</strong> {leader['Team_Name']}
                    <span style="color:#6b7a99">({leader['University']})</span> —
                    <strong style="color:#fcd34d">{leader['Points']} pts</strong>
                    · {leader['Wins']}W / {leader['Losses']}L
                </div>
            """, unsafe_allow_html=True)

            col_chart, col_tbl = st.columns([1.6, 1])
            with col_chart:
                fig = px.bar(
                    filtered.head(10), x="Team_Name", y="Points", color="University",
                    hover_data=["Wins", "Losses", "Matches_Played"],
                    color_discrete_sequence=px.colors.qualitative.Vivid,
                    labels={"Team_Name": "Team"}
                )
                fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#e8ecf4", showlegend=False,
                    margin=dict(t=10, b=10, l=0, r=0),
                    xaxis=dict(gridcolor="#252c3d"),
                    yaxis=dict(gridcolor="#252c3d"),
                )
                fig.update_traces(marker_line_width=0)
                st.plotly_chart(fig, use_container_width=True)
            with col_tbl:
                st.dataframe(
                    filtered[["Team_Name", "Wins", "Losses", "Points"]].reset_index(drop=True),
                    use_container_width=True, hide_index=True
                )
    else:
        st.info("Standings appear here once match results are entered.")

    st.divider()

    # ── Match Schedule ────────────────────────────────────────
    st.subheader("📅 Match Schedule")
    sched_data = run_query(
        "SELECT Sport_Name, Team_A, Team_B, Match_Date, Match_Time, Venue_Name, Stage, Status, Winner "
        "FROM Upcoming_Schedule LIMIT 20"
    )
    if sched_data:
        sched_df = pd.DataFrame(sched_data)
        def style_status(val):
            if val == "Completed": return "color:#10b981;font-weight:bold"
            if val == "Scheduled": return "color:#8b85ff;font-weight:bold"
            if val == "Cancelled": return "color:#ef4444;font-weight:bold"
            return ""
        st.dataframe(sched_df.style.map(style_status, subset=["Status"]),
                     use_container_width=True, hide_index=True)
    else:
        st.info("No matches in the schedule yet.")

    st.divider()

    # ── Tournament Awards strip ───────────────────────────────
    st.subheader("⭐ Live Tournament Awards")
    a1, a2, a3 = st.columns(3)

    with a1:
        st.markdown("🏏 **Orange Cap** — *Most Runs*")
        oc = run_query("""
            SELECT p.Player_Name, t.Team_Name, SUM(sc.Runs_Scored) AS Total
            FROM Scorecard_Cricket sc
            JOIN Players p ON sc.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID
            GROUP BY sc.Player_ID ORDER BY Total DESC LIMIT 1
        """)
        if oc: st.metric(oc[0]["Player_Name"], f"{oc[0]['Total']} runs", oc[0]["Team_Name"])
        else:  st.caption("No data yet")

    with a2:
        st.markdown("⚽ **Golden Boot** — *Most Goals*")
        gb = run_query("""
            SELECT p.Player_Name, t.Team_Name, SUM(sf.Goals) AS Total
            FROM Scorecard_Football sf
            JOIN Players p ON sf.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID
            GROUP BY sf.Player_ID ORDER BY Total DESC LIMIT 1
        """)
        if gb: st.metric(gb[0]["Player_Name"], f"{gb[0]['Total']} goals", gb[0]["Team_Name"])
        else:  st.caption("No data yet")

    with a3:
        st.markdown("🏀 **MVP** — *Avg Points*")
        mvp = run_query("""
            SELECT p.Player_Name, t.Team_Name, ROUND(AVG(sb.Points),1) AS Total
            FROM Scorecard_Basketball sb
            JOIN Players p ON sb.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID
            GROUP BY sb.Player_ID HAVING COUNT(*) >= 1 ORDER BY Total DESC LIMIT 1
        """)
        if mvp: st.metric(mvp[0]["Player_Name"], f"{mvp[0]['Total']} avg pts", mvp[0]["Team_Name"])
        else:   st.caption("No data yet")


# ═══════════════════ TAB 2: MATCH RESULTS (admin/manager only) ═
if can_edit:
  with tab_results:
    st.subheader("🏆 Update Match Result")
    st.markdown("""
    <div style="padding:12px 18px;border-radius:10px;border-left:4px solid #f5a623;
    background:rgba(245,166,35,.08);margin-bottom:20px;font-size:13px;line-height:1.7">
        Calls the <strong>UpdateMatchResult</strong> stored procedure — a full ACID transaction.<br>
        It validates the winner, updates the match status, fires
        <strong>trg_match_completed</strong>, and writes to <strong>Audit_Log</strong> — all automatically.
    </div>
    """, unsafe_allow_html=True)

    scheduled_matches = run_query("""
        SELECT m.Match_ID,
               CONCAT(sp.Sport_Name, ': ', ta.Team_Name, ' vs ', tb.Team_Name,
                      '  (', m.Match_Date, ')  [', m.Stage, ']') AS Match_Desc,
               m.Team_A_ID, m.Team_B_ID,
               ta.Team_Name AS Team_A, tb.Team_Name AS Team_B
        FROM Matches m
        JOIN Teams ta ON m.Team_A_ID=ta.Team_ID
        JOIN Teams tb ON m.Team_B_ID=tb.Team_ID
        JOIN Sports sp ON m.Sport_ID=sp.Sport_ID
        WHERE m.Status='Scheduled'
        ORDER BY m.Match_Date
    """)

    if scheduled_matches:
        match_df   = pd.DataFrame(scheduled_matches)
        match_dict = {row["Match_Desc"]: row for row in scheduled_matches}

        selected_desc = st.selectbox("Select a scheduled match", list(match_dict.keys()))
        sel = match_dict[selected_desc]

        winner_label = st.radio(
            "Who won?",
            [sel["Team_A"], sel["Team_B"]],
            horizontal=True,
            key="winner_radio"
        )
        winner_id = sel["Team_A_ID"] if winner_label == sel["Team_A"] else sel["Team_B_ID"]

        if st.button("🏆 Confirm & Save Result", use_container_width=True):
            with st.spinner("Running transaction…"):
                result, error = call_procedure("UpdateMatchResult", (sel["Match_ID"], winner_id))
                time.sleep(0.5)
            if error:
                if "not found" in error.lower() or "already" in error.lower():
                    st.error(f"❌ {error}")
                else:
                    st.error(f"❌ Database error: {error}")
            else:
                st.success(
                    f"✅ **{winner_label}** marked as winner! "
                    f"Match status set to 'Completed' by trigger. Audit log updated."
                )
                st.balloons()
                time.sleep(1.5)
                st.rerun()
    else:
        st.info("No scheduled matches to update — all may already be completed.")

    st.divider()
    st.subheader("✅ Completed Results")
    completed_data = run_query("""
        SELECT sp.Sport_Name, ta.Team_Name AS Team_A, tb.Team_Name AS Team_B,
               tw.Team_Name AS Winner, m.Match_Date, m.Stage
        FROM Matches m
        JOIN Sports sp ON m.Sport_ID=sp.Sport_ID
        JOIN Teams ta ON m.Team_A_ID=ta.Team_ID
        JOIN Teams tb ON m.Team_B_ID=tb.Team_ID
        JOIN Teams tw ON m.Winner_Team_ID=tw.Team_ID
        WHERE m.Status='Completed'
        ORDER BY m.Match_Date DESC
    """)
    if completed_data:
        st.dataframe(pd.DataFrame(completed_data), use_container_width=True, hide_index=True)
    else:
        st.info("No completed matches yet.")


# ══════════════════ TAB 3: TEAM MANAGEMENT ════════════════════
with tab_teams:
    st.subheader("🏟️ Team Management")
    sports_list = run_query("SELECT Sport_ID, Sport_Name FROM Sports ORDER BY Sport_Name")
    sport_map   = {s["Sport_Name"]: s["Sport_ID"] for s in sports_list} if sports_list else {}

    col_form, col_list = st.columns([1, 1.3])

    with col_form:
        st.markdown("**➕ Register a New Team**")
        with st.form("add_team", clear_on_submit=True):
            tname = st.text_input("Team Name *", placeholder="e.g. IIT Delhi Warriors")
            uni   = st.text_input("University *",  placeholder="e.g. IIT Delhi")
            sport = st.selectbox("Sport *", list(sport_map.keys()) if sport_map else ["—"])
            coach = st.text_input("Coach Name *",  placeholder="e.g. Rahul Dravid")

            if st.form_submit_button("✅ Add Team", use_container_width=True):
                errors = []
                if not tname.strip(): errors.append("Team name is required.")
                if not uni.strip():   errors.append("University is required.")
                if not coach.strip(): errors.append("Coach name is required.")

                if errors:
                    for e in errors: st.error(f"❌ {e}")
                elif not sport_map:
                    st.error("❌ No sports found in the database.")
                else:
                    with st.spinner("Writing to database…"):
                        rows = run_query(
                            "INSERT INTO Teams (Team_Name,University,Sport_ID,Coach_Name) VALUES (%s,%s,%s,%s)",
                            (tname.strip(), uni.strip(), sport_map[sport], coach.strip()), fetch=False
                        )
                        time.sleep(0.4)
                    if rows:
                        st.balloons()
                        st.toast(f"'{tname}' added to MySQL!", icon="✅")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Failed — this team name may already exist for this sport.")

    with col_list:
        st.markdown("**📋 All Teams**")
        teams_data = run_query("""
            SELECT t.Team_Name, t.University, sp.Sport_Name, t.Coach_Name,
                   COUNT(p.Player_ID) AS Squad_Size
            FROM Teams t
            JOIN Sports sp ON t.Sport_ID=sp.Sport_ID
            LEFT JOIN Players p ON p.Team_ID=t.Team_ID
            GROUP BY t.Team_ID
            ORDER BY sp.Sport_Name, t.Team_Name
        """)
        if teams_data:
            st.dataframe(pd.DataFrame(teams_data), use_container_width=True, hide_index=True)


# ══════════════════ TAB 4: PLAYER MANAGEMENT ══════════════════
with tab_players:
    st.subheader("👤 Player Management")
    all_teams = run_query("""
        SELECT t.Team_ID, t.Team_Name, t.University, sp.Sport_Name
        FROM Teams t JOIN Sports sp ON t.Sport_ID=sp.Sport_ID
        ORDER BY sp.Sport_Name, t.Team_Name
    """)
    team_map = {
        f"{t['Team_Name']} ({t['University']}) — {t['Sport_Name']}": t["Team_ID"]
        for t in all_teams
    } if all_teams else {}

    col_form, col_list = st.columns([1, 1.3])

    with col_form:
        st.markdown("**➕ Register a New Player**")
        with st.form("add_player", clear_on_submit=True):
            pname  = st.text_input("Player Name *", placeholder="e.g. Arjun Mehta")
            tsel   = st.selectbox("Team *", list(team_map.keys()) if team_map else ["—"])
            prole  = st.text_input("Role *", placeholder="e.g. Batsman, Striker, Guard")
            jersey = st.number_input("Jersey No *", min_value=1, max_value=99, value=10,
                                      help="Must be unique within the team (1–99).")

            if st.form_submit_button("✅ Register Player", use_container_width=True):
                errors = []
                if not pname.strip(): errors.append("Player name is required.")
                if not prole.strip(): errors.append("Role is required.")

                if errors:
                    for e in errors: st.error(f"❌ {e}")
                elif not team_map:
                    st.error("❌ No teams in the database yet.")
                else:
                    with st.spinner("Verifying jersey & registering…"):
                        result, error = call_procedure(
                            "RegisterPlayer",
                            (pname.strip(), team_map[tsel], prole.strip(), int(jersey))
                        )
                        time.sleep(0.4)
                    if error:
                        if "jersey" in error.lower() or "Jersey" in error:
                            st.error(f"❌ Jersey #{jersey} is already taken in this team. Pick a different number.")
                        else:
                            st.error(f"❌ {error}")
                    else:
                        st.toast(f"{pname} registered!", icon="✅")
                        time.sleep(1)
                        st.rerun()

    with col_list:
        st.markdown("**📋 All Players**")
        players_data = run_query("""
            SELECT p.Player_Name, t.Team_Name, sp.Sport_Name,
                   p.Role, p.Jersey_No, p.Form_Status
            FROM Players p
            JOIN Teams t ON p.Team_ID=t.Team_ID
            JOIN Sports sp ON t.Sport_ID=sp.Sport_ID
            ORDER BY sp.Sport_Name, t.Team_Name, p.Player_Name
        """)
        if players_data:
            pl_df = pd.DataFrame(players_data)
            def color_form(val):
                if val == "In Form":     return "color:#10b981;font-weight:bold"
                if val == "Out of Form": return "color:#ef4444;font-weight:bold"
                return "color:#6b7a99"
            st.dataframe(
                pl_df.style.map(color_form, subset=["Form_Status"]),
                use_container_width=True, hide_index=True
            )