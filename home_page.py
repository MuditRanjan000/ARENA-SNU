# home_page.py — ARENA SNU Dashboard v6
# SURGE 2025 · All 6 sports · System Architect: Mudit
import streamlit as st
import time
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from db_connection import run_query, call_procedure

try:
    st.set_page_config(page_title="ARENA SNU — Dashboard", page_icon="🏆", layout="wide")
except Exception:
    pass

# ── HERO BANNER ───────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#0d1117 0%,#161b24 50%,#0d1117 100%);
     border:1px solid #21262d;border-radius:16px;padding:28px 32px;margin-bottom:24px;
     position:relative;overflow:hidden">
  <div style="position:absolute;top:-30px;right:-30px;font-size:8rem;opacity:0.04;
       filter:blur(4px)">🏆</div>
  <div style="position:relative;z-index:1">
    <h1 style="background:linear-gradient(90deg,#6c63ff,#a855f7,#f5a623);
       -webkit-background-clip:text;-webkit-text-fill-color:transparent;
       font-size:2.8rem;font-weight:800;margin:0;letter-spacing:-1px;
       font-family:'Rajdhani',sans-serif">🏆 ARENA SNU</h1>
    <p style="color:#6b7a99;font-size:.95rem;margin-top:6px;max-width:600px">
       Athletic Resource &amp; Event Navigation Application ·
       <strong style="color:#f5a623">SURGE 2025</strong> — SNU Annual Sports Festival<br>
       <span style="font-size:.8rem">Shiv Nadar University, Greater Noida · 6 Sports · 38 Teams · 200+ Players</span></p>
    <div style="display:flex;gap:12px;margin-top:14px;flex-wrap:wrap">
      <span style="background:rgba(108,99,255,.15);border:1px solid rgba(108,99,255,.3);color:#8b85ff;
        font-size:12px;padding:4px 12px;border-radius:20px;font-weight:600">🏏 Cricket</span>
      <span style="background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.3);color:#22c55e;
        font-size:12px;padding:4px 12px;border-radius:20px;font-weight:600">⚽ Football</span>
      <span style="background:rgba(249,115,22,.1);border:1px solid rgba(249,115,22,.3);color:#f97316;
        font-size:12px;padding:4px 12px;border-radius:20px;font-weight:600">🏀 Basketball</span>
      <span style="background:rgba(6,182,212,.1);border:1px solid rgba(6,182,212,.3);color:#06b6d4;
        font-size:12px;padding:4px 12px;border-radius:20px;font-weight:600">🏸 Badminton</span>
      <span style="background:rgba(236,72,153,.1);border:1px solid rgba(236,72,153,.3);color:#ec4899;
        font-size:12px;padding:4px 12px;border-radius:20px;font-weight:600">🏓 Table Tennis</span>
      <span style="background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.3);color:#f59e0b;
        font-size:12px;padding:4px 12px;border-radius:20px;font-weight:600">🏐 Volleyball</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

role = st.session_state.get("role", "viewer")
can_edit = role in ("admin", "manager")

tab_labels = ["📊 Dashboard", "🏟️ Teams", "👤 Players"]
if can_edit:
    tab_labels.insert(1, "🏆 Match Results")

tabs        = st.tabs(tab_labels)
tab_dash    = tabs[0]
tab_results = tabs[1] if can_edit else None
tab_teams   = tabs[2] if can_edit else tabs[1]
tab_players = tabs[3] if can_edit else tabs[2]

# ═══════════════════════ TAB 1: DASHBOARD ═════════════════════
with tab_dash:
    # ── Top-level metrics ───────────────────────────────────
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    sports_cnt    = run_query("SELECT COUNT(*) AS cnt FROM Sports")
    teams_cnt     = run_query("SELECT COUNT(*) AS cnt FROM Teams")
    players_cnt   = run_query("SELECT COUNT(*) AS cnt FROM Players")
    matches_cnt   = run_query("SELECT COUNT(*) AS cnt FROM Matches")
    completed_cnt = run_query("SELECT COUNT(*) AS cnt FROM Matches WHERE Status='Completed'")
    scheduled_cnt = run_query("SELECT COUNT(*) AS cnt FROM Matches WHERE Status='Scheduled'")

    c1.metric("🏅 Sports",     sports_cnt[0]["cnt"]    if sports_cnt    else 0)
    c2.metric("🏟️ Teams",      teams_cnt[0]["cnt"]     if teams_cnt     else 0)
    c3.metric("👤 Players",    players_cnt[0]["cnt"]   if players_cnt   else 0)
    c4.metric("📅 Matches",    matches_cnt[0]["cnt"]   if matches_cnt   else 0)
    c5.metric("✅ Completed",  completed_cnt[0]["cnt"] if completed_cnt else 0)
    c6.metric("⏳ Scheduled",  scheduled_cnt[0]["cnt"] if scheduled_cnt else 0,
              delta="Finals upcoming" if run_query("SELECT COUNT(*) AS c FROM Matches WHERE Stage='Final' AND Status='Scheduled'")[0]["c"] > 0 else None)

    st.divider()

    # ── Finals Banner ───────────────────────────────────────
    finals = run_query("SELECT * FROM Finals_Overview")
    if finals:
        st.markdown("### 🏆 SURGE 2025 Finals")
        cols = st.columns(len(finals))
        sport_colors = {
            "Cricket":     "#a855f7", "Football": "#22c55e",
            "Basketball":  "#f97316", "Badminton": "#06b6d4",
            "Table Tennis":"#ec4899", "Volleyball":"#f59e0b",
        }
        for col, f in zip(cols, finals):
            color = sport_colors.get(f["Sport_Name"], "#6c63ff")
            champion = f["Champion"] if f["Champion"] != "TBD" else "🔜 TBD"
            col.markdown(f"""
            <div style="background:#161b24;border:1px solid {color}33;border-top:3px solid {color};
            border-radius:12px;padding:14px 16px;text-align:center">
              <div style="font-size:1.4rem">{f['Icon']}</div>
              <div style="font-size:13px;font-weight:700;color:{color};margin:4px 0">{f['Sport_Name']}</div>
              <div style="font-size:11px;color:#6b7a99">{f['Team_A']} vs {f['Team_B']}</div>
              <div style="font-size:11px;color:#6b7a99;margin-top:2px">📅 {f['Match_Date']}</div>
              {"<div style='margin-top:6px;font-size:12px;font-weight:700;color:#f5a623'>🏆 " + champion + "</div>" if f['Champion'] != "TBD" else "<div style='margin-top:6px;font-size:11px;color:#6b7a99'>Result pending</div>"}
            </div>
            """, unsafe_allow_html=True)
        st.divider()

    # ── Points Table ────────────────────────────────────────
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
                🏆 <strong>Leader</strong> [{leader['Sport_Name']}]: {leader['Team_Name']}
                <span style="color:#6b7a99">({leader['University']})</span> —
                <strong style="color:#fcd34d">{leader['Points']} pts</strong>
                · {leader['Wins']}W / {leader['Losses']}L
            </div>
            """, unsafe_allow_html=True)

            col_chart, col_tbl = st.columns([1.6, 1])
            with col_chart:
                fig = px.bar(filtered.head(12), x="Team_Name", y="Points", color="University",
                             hover_data=["Wins","Losses","Matches_Played","Sport_Name"],
                             color_discrete_sequence=px.colors.qualitative.Vivid,
                             labels={"Team_Name":"Team"})
                fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                  font_color="#e8ecf4", showlegend=False,
                                  margin=dict(t=10,b=10,l=0,r=0),
                                  xaxis=dict(gridcolor="#252c3d", tickangle=-30),
                                  yaxis=dict(gridcolor="#252c3d"))
                fig.update_traces(marker_line_width=0)
                st.plotly_chart(fig, use_container_width=True)
            with col_tbl:
                st.dataframe(filtered[["Team_Name","Sport_Name","Wins","Losses","Points"]].reset_index(drop=True),
                             use_container_width=True, hide_index=True)
    else:
        st.info("Standings appear once match results are entered.")

    st.divider()

    # ── Match Schedule ───────────────────────────────────────
    st.subheader("📅 Full Match Schedule")
    sport_f = st.selectbox("Filter schedule by sport", ["All Sports","Cricket","Football","Basketball",
                                                          "Badminton","Table Tennis","Volleyball"],
                           key="sched_filter", label_visibility="collapsed")
    q = "SELECT Sport_Icon, Sport_Name, Team_A, Team_B, Match_Date, Match_Time, Venue_Name, Stage, Status, Winner FROM Upcoming_Schedule"
    if sport_f != "All Sports":
        q += f" WHERE Sport_Name='{sport_f}'"
    sched_data = run_query(q + " LIMIT 60")
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

    # ── Awards Strip ─────────────────────────────────────────
    st.subheader("⭐ Live Tournament Awards")
    a1, a2, a3, a4, a5, a6 = st.columns(6)

    # Cricket — Orange Cap
    with a1:
        st.markdown("""<div style="background:#161b24;border:1px solid #21262d;border-top:3px solid #a855f7;
        border-radius:10px;padding:12px 14px;text-align:center;font-size:12px">
        <div style="font-size:1.4rem">🏏</div>
        <div style="color:#a855f7;font-weight:700;margin:4px 0">Orange Cap</div>
        <div style="color:#6b7a99;font-size:11px">Most Runs</div></div>""", unsafe_allow_html=True)
        oc = run_query("""SELECT p.Player_Name, t.Team_Name, SUM(sc.Runs_Scored) AS Total
                          FROM Scorecard_Cricket sc JOIN Players p ON sc.Player_ID=p.Player_ID
                          JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sc.Player_ID ORDER BY Total DESC LIMIT 1""")
        if oc: st.metric(oc[0]["Player_Name"], f"{oc[0]['Total']} runs", oc[0]["Team_Name"])
        else:  st.caption("No data yet")

    # Cricket — Purple Cap
    with a2:
        st.markdown("""<div style="background:#161b24;border:1px solid #21262d;border-top:3px solid #6c63ff;
        border-radius:10px;padding:12px 14px;text-align:center;font-size:12px">
        <div style="font-size:1.4rem">🏏</div>
        <div style="color:#6c63ff;font-weight:700;margin:4px 0">Purple Cap</div>
        <div style="color:#6b7a99;font-size:11px">Most Wickets</div></div>""", unsafe_allow_html=True)
        pc = run_query("""SELECT p.Player_Name, t.Team_Name, SUM(sc.Wickets_Taken) AS Total
                          FROM Scorecard_Cricket sc JOIN Players p ON sc.Player_ID=p.Player_ID
                          JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sc.Player_ID
                          HAVING Total>0 ORDER BY Total DESC LIMIT 1""")
        if pc: st.metric(pc[0]["Player_Name"], f"{pc[0]['Total']} wkts", pc[0]["Team_Name"])
        else:  st.caption("No data yet")

    # Football — Golden Boot
    with a3:
        st.markdown("""<div style="background:#161b24;border:1px solid #21262d;border-top:3px solid #22c55e;
        border-radius:10px;padding:12px 14px;text-align:center;font-size:12px">
        <div style="font-size:1.4rem">⚽</div>
        <div style="color:#22c55e;font-weight:700;margin:4px 0">Golden Boot</div>
        <div style="color:#6b7a99;font-size:11px">Most Goals</div></div>""", unsafe_allow_html=True)
        gb = run_query("""SELECT p.Player_Name, t.Team_Name, SUM(sf.Goals) AS Total
                          FROM Scorecard_Football sf JOIN Players p ON sf.Player_ID=p.Player_ID
                          JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sf.Player_ID ORDER BY Total DESC LIMIT 1""")
        if gb: st.metric(gb[0]["Player_Name"], f"{gb[0]['Total']} goals", gb[0]["Team_Name"])
        else:  st.caption("No data yet")

    # Basketball — MVP
    with a4:
        st.markdown("""<div style="background:#161b24;border:1px solid #21262d;border-top:3px solid #f97316;
        border-radius:10px;padding:12px 14px;text-align:center;font-size:12px">
        <div style="font-size:1.4rem">🏀</div>
        <div style="color:#f97316;font-weight:700;margin:4px 0">MVP</div>
        <div style="color:#6b7a99;font-size:11px">Avg Points</div></div>""", unsafe_allow_html=True)
        mvp = run_query("""SELECT p.Player_Name, t.Team_Name, ROUND(AVG(sb.Points),1) AS Total
                           FROM Scorecard_Basketball sb JOIN Players p ON sb.Player_ID=p.Player_ID
                           JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sb.Player_ID ORDER BY Total DESC LIMIT 1""")
        if mvp: st.metric(mvp[0]["Player_Name"], f"{mvp[0]['Total']} avg", mvp[0]["Team_Name"])
        else:   st.caption("No data yet")

    # Badminton — Top Player
    with a5:
        st.markdown("""<div style="background:#161b24;border:1px solid #21262d;border-top:3px solid #06b6d4;
        border-radius:10px;padding:12px 14px;text-align:center;font-size:12px">
        <div style="font-size:1.4rem">🏸</div>
        <div style="color:#06b6d4;font-weight:700;margin:4px 0">Best Smasher</div>
        <div style="color:#6b7a99;font-size:11px">Most Sets Won</div></div>""", unsafe_allow_html=True)
        bd = run_query("""SELECT p.Player_Name, t.Team_Name, SUM(sb.Sets_Won) AS Total
                          FROM Scorecard_Badminton sb JOIN Players p ON sb.Player_ID=p.Player_ID
                          JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sb.Player_ID ORDER BY Total DESC LIMIT 1""")
        if bd: st.metric(bd[0]["Player_Name"], f"{bd[0]['Total']} sets", bd[0]["Team_Name"])
        else:  st.caption("No data yet")

    # Volleyball — Top Attacker
    with a6:
        st.markdown("""<div style="background:#161b24;border:1px solid #21262d;border-top:3px solid #f59e0b;
        border-radius:10px;padding:12px 14px;text-align:center;font-size:12px">
        <div style="font-size:1.4rem">🏐</div>
        <div style="color:#f59e0b;font-weight:700;margin:4px 0">Top Spiker</div>
        <div style="color:#6b7a99;font-size:11px">Most Kills</div></div>""", unsafe_allow_html=True)
        vb = run_query("""SELECT p.Player_Name, t.Team_Name, SUM(sv.Kills) AS Total
                          FROM Scorecard_Volleyball sv JOIN Players p ON sv.Player_ID=p.Player_ID
                          JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sv.Player_ID ORDER BY Total DESC LIMIT 1""")
        if vb: st.metric(vb[0]["Player_Name"], f"{vb[0]['Total']} kills", vb[0]["Team_Name"])
        else:  st.caption("No data yet")


# ═══════════════ TAB 2: MATCH RESULTS (admin/manager only) ════
if can_edit:
    with tab_results:
        st.subheader("🏆 Update Match Result")
        st.markdown("""
        <div style="padding:10px 16px;border-radius:8px;border-left:3px solid #6c63ff;
        background:rgba(108,99,255,.07);font-size:13px;margin-bottom:20px">
            Uses the <strong>UpdateMatchResult</strong> stored procedure.
            Runs a full ACID transaction: validates → UPDATE Matches → INSERT Audit_Log → COMMIT.
            DB trigger auto-sets Status='Completed'.
        </div>""", unsafe_allow_html=True)

        scheduled_matches = run_query("""
            SELECT m.Match_ID,
                   CONCAT(sp.Sport_Name,' | ',ta.Team_Name,' vs ',tb.Team_Name,
                          '  (',m.Match_Date,')  [',m.Stage,']') AS Match_Desc,
                   ta.Team_Name AS Team_A, tb.Team_Name AS Team_B,
                   ta.Team_ID AS Team_A_ID, tb.Team_ID AS Team_B_ID
            FROM Matches m
            JOIN Teams ta ON m.Team_A_ID=ta.Team_ID
            JOIN Teams tb ON m.Team_B_ID=tb.Team_ID
            JOIN Sports sp ON m.Sport_ID=sp.Sport_ID
            WHERE m.Status='Scheduled'
            ORDER BY m.Match_Date
        """)

        if scheduled_matches:
            match_dict    = {row["Match_Desc"]: row for row in scheduled_matches}
            selected_desc = st.selectbox("Select a scheduled match", list(match_dict.keys()))
            sel           = match_dict[selected_desc]

            winner_label = st.radio("Who won?", [sel["Team_A"], sel["Team_B"]],
                                    horizontal=True, key="winner_radio")
            winner_id = sel["Team_A_ID"] if winner_label == sel["Team_A"] else sel["Team_B_ID"]

            if st.button("🏆 Confirm & Save Result", use_container_width=True):
                with st.spinner("Running ACID transaction…"):
                    result, error = call_procedure("UpdateMatchResult", (sel["Match_ID"], winner_id))
                    time.sleep(0.5)
                if error:
                    st.error(f"❌ {error}")
                else:
                    st.success(f"✅ **{winner_label}** marked as winner! Trigger auto-set Status='Completed'. Audit logged.")
                    st.balloons()
                    time.sleep(1.5)
                    st.rerun()
        else:
            st.info("No scheduled matches to update — all may already be completed or cancelled.")

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


# ═══════════════════ TAB 3: TEAM MANAGEMENT ══════════════════
with tab_teams:
    st.subheader("🏟️ Team Management")
    sports_list = run_query("SELECT Sport_ID, Sport_Name, Icon FROM Sports ORDER BY Sport_Name")
    sport_map   = {f"{s['Icon']} {s['Sport_Name']}": s["Sport_ID"] for s in sports_list} if sports_list else {}

    col_form, col_list = st.columns([1, 1.3])
    with col_form:
        st.markdown("**➕ Register a New Team**")
        with st.form("add_team", clear_on_submit=True):
            tname = st.text_input("Team Name *", placeholder="e.g. DTU Warriors")
            uni   = st.text_input("University *", placeholder="e.g. Delhi Technological University")
            sport = st.selectbox("Sport *", list(sport_map.keys()) if sport_map else ["—"])
            coach = st.text_input("Coach Name *", placeholder="e.g. Rahul Dravid")

            if st.form_submit_button("✅ Add Team", use_container_width=True):
                if not tname.strip() or not uni.strip() or not coach.strip():
                    st.error("❌ All fields are required.")
                elif not sport_map:
                    st.error("❌ No sports found in the database.")
                else:
                    rows = run_query(
                        "INSERT INTO Teams (Team_Name,University,Sport_ID,Coach_Name) VALUES (%s,%s,%s,%s)",
                        (tname.strip(), uni.strip(), sport_map[sport], coach.strip()), fetch=False
                    )
                    time.sleep(0.4)
                    if rows:
                        st.balloons()
                        st.toast(f"'{tname}' added!", icon="✅")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Failed — this team name may already exist for this sport.")

    with col_list:
        st.markdown("**📋 All Registered Teams**")
        teams_data = run_query("""
            SELECT t.Team_Name, t.University, sp.Sport_Name AS Sport,
                   t.Coach_Name, t.Group_Name AS `Group`,
                   COUNT(p.Player_ID) AS Players
            FROM Teams t
            JOIN Sports sp ON t.Sport_ID=sp.Sport_ID
            LEFT JOIN Players p ON p.Team_ID=t.Team_ID
            GROUP BY t.Team_ID
            ORDER BY sp.Sport_Name, t.Team_Name
        """)
        if teams_data:
            st.dataframe(pd.DataFrame(teams_data), use_container_width=True, hide_index=True)


# ═══════════════════ TAB 4: PLAYER MANAGEMENT ══════════════════
with tab_players:
    st.subheader("👤 Player Management")
    all_teams = run_query("""
        SELECT t.Team_ID, t.Team_Name, t.University, sp.Sport_Name, sp.Icon
        FROM Teams t JOIN Sports sp ON t.Sport_ID=sp.Sport_ID
        ORDER BY sp.Sport_Name, t.Team_Name
    """)
    team_map = {
        f"{t['Icon']} {t['Team_Name']} ({t['University']}) — {t['Sport_Name']}": t["Team_ID"]
        for t in all_teams
    } if all_teams else {}

    col_form, col_list = st.columns([1, 1.3])
    with col_form:
        st.markdown("**➕ Register a New Player**")
        with st.form("add_player", clear_on_submit=True):
            pname  = st.text_input("Player Name *", placeholder="e.g. Arjun Mehta")
            tsel   = st.selectbox("Team *", list(team_map.keys()) if team_map else ["—"])
            prole  = st.text_input("Role *", placeholder="e.g. Batsman, Striker, Point Guard")
            jersey = st.number_input("Jersey No *", min_value=1, max_value=99, value=10,
                                      help="Must be unique within the team (1–99)")

            if st.form_submit_button("✅ Register Player", use_container_width=True):
                if not pname.strip() or not prole.strip():
                    st.error("❌ Name and role are required.")
                elif not team_map:
                    st.error("❌ No teams in the database yet.")
                else:
                    result, error = call_procedure(
                        "RegisterPlayer", (pname.strip(), team_map[tsel], prole.strip(), int(jersey))
                    )
                    time.sleep(0.4)
                    if error:
                        if "jersey" in error.lower():
                            st.error(f"❌ Jersey #{jersey} is already taken. Pick a different number.")
                        else:
                            st.error(f"❌ {error}")
                    else:
                        st.toast(f"{pname} registered!", icon="✅")
                        time.sleep(1)
                        st.rerun()

    with col_list:
        st.markdown("**📋 All Registered Players**")
        # Sport filter for player list
        sport_filt = st.selectbox("Filter by sport", ["All"] + [s["Sport_Name"] for s in sports_list],
                                  key="player_sport_filt", label_visibility="collapsed")
        qp = """
            SELECT p.Player_Name, t.Team_Name, sp.Sport_Name AS Sport,
                   p.Role, p.Jersey_No AS Jersey, p.Form_Status
            FROM Players p
            JOIN Teams t ON p.Team_ID=t.Team_ID
            JOIN Sports sp ON t.Sport_ID=sp.Sport_ID
        """
        if sport_filt != "All":
            qp += f" WHERE sp.Sport_Name='{sport_filt}'"
        qp += " ORDER BY sp.Sport_Name, t.Team_Name, p.Player_Name"

        players_data = run_query(qp)
        if players_data:
            pl_df = pd.DataFrame(players_data)
            def color_form(val):
                if val == "In Form":     return "color:#10b981;font-weight:bold"
                if val == "Out of Form": return "color:#ef4444;font-weight:bold"
                return "color:#6b7a99"
            st.dataframe(pl_df.style.map(color_form, subset=["Form_Status"]),
                         use_container_width=True, hide_index=True)
        else:
            st.info("No players registered yet.")