# home_page.py — ARENA SNU Dashboard v7
# SURGE 2025 · System Architect: Mudit
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
<div style="
  background:linear-gradient(135deg,#0a0f1a 0%,#111827 60%,#0a0f1a 100%);
  border:1px solid #1e2d45;border-radius:18px;
  padding:28px 32px;margin-bottom:24px;position:relative;overflow:hidden">
  <!-- decorative glow -->
  <div style="position:absolute;top:-60px;right:-60px;width:260px;height:260px;
    background:radial-gradient(circle,rgba(91,82,245,.18) 0%,transparent 70%);
    border-radius:50%;pointer-events:none"></div>
  <div style="position:absolute;bottom:-60px;left:-40px;width:220px;height:220px;
    background:radial-gradient(circle,rgba(168,85,247,.12) 0%,transparent 70%);
    border-radius:50%;pointer-events:none"></div>

  <div style="position:relative;z-index:1">
    <h1 style="
      background:linear-gradient(100deg,#5b52f5,#a855f7,#f5a623);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;
      font-family:'Rajdhani',sans-serif;font-size:2.8rem;font-weight:700;
      margin:0;letter-spacing:-1px">🏆 ARENA SNU</h1>
    <p style="color:#4a5568;font-size:.95rem;margin:6px 0 14px;max-width:560px">
      Athletic Resource &amp; Event Navigation Application ·
      <strong style="color:#f5a623">SURGE 2025</strong> — SNU Annual Sports Festival<br>
      <span style="font-size:.82rem">Shiv Nadar University · 3 Sports · 18 Teams · 150+ Players</span>
    </p>
    <div style="display:flex;gap:10px">
      <span style="background:rgba(168,85,247,.15);border:1px solid rgba(168,85,247,.35);
        color:#c084fc;font-size:12px;font-weight:600;padding:4px 14px;border-radius:20px">🏏 Cricket</span>
      <span style="background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.3);
        color:#4ade80;font-size:12px;font-weight:600;padding:4px 14px;border-radius:20px">⚽ Football</span>
      <span style="background:rgba(249,115,22,.1);border:1px solid rgba(249,115,22,.3);
        color:#fb923c;font-size:12px;font-weight:600;padding:4px 14px;border-radius:20px">🏀 Basketball</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

role     = st.session_state.get("role", "viewer")
can_edit = role in ("admin", "manager")

tab_labels = ["📊 Dashboard", "🏟️ Teams", "👤 Players"]
if can_edit:
    tab_labels.insert(1, "🏆 Match Results")

tabs        = st.tabs(tab_labels)
tab_dash    = tabs[0]
tab_results = tabs[1] if can_edit else None
tab_teams   = tabs[2] if can_edit else tabs[1]
tab_players = tabs[3] if can_edit else tabs[2]


# ═══════════ TAB 1 — DASHBOARD ═══════════════════════════════
with tab_dash:
    # ── KPI row ───────────────────────────────────────────────
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    def q1(sql): r=run_query(sql); return r[0]["cnt"] if r else 0
    c1.metric("🏅 Sports",    q1("SELECT COUNT(*) AS cnt FROM Sports"))
    c2.metric("🏟️ Teams",     q1("SELECT COUNT(*) AS cnt FROM Teams"))
    c3.metric("👤 Players",   q1("SELECT COUNT(*) AS cnt FROM Players"))
    c4.metric("📅 Matches",   q1("SELECT COUNT(*) AS cnt FROM Matches"))
    c5.metric("✅ Done",      q1("SELECT COUNT(*) AS cnt FROM Matches WHERE Status='Completed'"))
    c6.metric("⏳ Scheduled", q1("SELECT COUNT(*) AS cnt FROM Matches WHERE Status='Scheduled'"))

    st.divider()

    # ── Finals strip ──────────────────────────────────────────
    finals = run_query("SELECT * FROM Finals_Overview")
    if finals:
        st.markdown("### 🏆 SURGE 2025 — Finals")
        sport_colors = {"Cricket":"#a855f7","Football":"#22c55e","Basketball":"#f97316"}
        fcols = st.columns(len(finals))
        for col, f in zip(fcols, finals):
            clr = sport_colors.get(f["Sport_Name"],"#5b52f5")
            champ = f["Champion"] if f["Champion"] != "TBD" else "🔜 TBD"
            col.markdown(f"""
            <div style="background:#101726;border:1px solid {clr}44;border-top:3px solid {clr};
            border-radius:14px;padding:14px 16px;text-align:center">
              <div style="font-size:1.5rem">{f['Icon']}</div>
              <div style="font-size:13px;font-weight:700;color:{clr};margin:4px 0">{f['Sport_Name']}</div>
              <div style="font-size:11px;color:#4a5568">{f['Team_A']}</div>
              <div style="font-size:10px;color:#2a3a52">vs</div>
              <div style="font-size:11px;color:#4a5568">{f['Team_B']}</div>
              <div style="font-size:11px;color:#3a4a6a;margin-top:4px">📅 {f['Match_Date']}</div>
              {'<div style="margin-top:8px;font-size:12px;font-weight:700;color:#f5a623">🏆 ' + champ + '</div>'
               if f['Champion'] != 'TBD'
               else '<div style="margin-top:8px;font-size:11px;color:#3a4a6a">Pending</div>'}
            </div>""", unsafe_allow_html=True)
        st.divider()

    # ── Standings ─────────────────────────────────────────────
    st.subheader("🏆 Tournament Standings")
    pts = run_query("SELECT Team_Name,University,Sport_Name,Matches_Played,Wins,Losses,Points FROM Points_Table")
    if pts:
        df_pts = pd.DataFrame(pts)
        sport_opts = ["All Sports"] + sorted(df_pts["Sport_Name"].unique().tolist())
        col_f, _ = st.columns([1,3])
        with col_f:
            sf = st.selectbox("Filter", sport_opts, label_visibility="collapsed", key="stand_f")
        filtered = df_pts if sf == "All Sports" else df_pts[df_pts["Sport_Name"]==sf]
        if not filtered.empty:
            leader = filtered.iloc[0]
            st.markdown(f"""
            <div style="padding:12px 18px;border-radius:10px;
            border-left:4px solid #f5a623;background:rgba(245,166,35,.07);
            margin-bottom:16px;font-size:14px">
            🏆 <strong>Leader</strong> [{leader['Sport_Name']}]: {leader['Team_Name']}
            <span style="color:#4a5568">({leader['University']})</span> —
            <strong style="color:#fbbf24">{leader['Points']} pts</strong>
            · {leader['Wins']}W/{leader['Losses']}L
            </div>""", unsafe_allow_html=True)

            chart_col, tbl_col = st.columns([1.6,1])
            with chart_col:
                fig = px.bar(filtered.head(12), x="Team_Name", y="Points",
                             color="University",
                             hover_data=["Wins","Losses","Matches_Played","Sport_Name"],
                             color_discrete_sequence=px.colors.qualitative.Vivid,
                             labels={"Team_Name":"Team"})
                fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                                  font_color="#e8ecf4",showlegend=False,
                                  margin=dict(t=10,b=10,l=0,r=0),
                                  xaxis=dict(gridcolor="#1e2d45",tickangle=-30),
                                  yaxis=dict(gridcolor="#1e2d45"))
                fig.update_traces(marker_line_width=0)
                st.plotly_chart(fig, use_container_width=True)
            with tbl_col:
                st.dataframe(
                    filtered[["Team_Name","Sport_Name","Wins","Losses","Points"]].reset_index(drop=True),
                    use_container_width=True, hide_index=True)
    else:
        st.info("Standings appear once match results are recorded.")

    st.divider()

    # ── Schedule ──────────────────────────────────────────────
    st.subheader("📅 Match Schedule")
    col_sf, _ = st.columns([1,3])
    with col_sf:
        sf2 = st.selectbox("Sport filter", ["All","Cricket","Football","Basketball"],
                           label_visibility="collapsed", key="sched_sf")
    sq = ("SELECT Sport_Icon,Sport_Name,Team_A,Team_B,Match_Date,Match_Time,"
          "Venue_Name,Stage,Status,Winner FROM Upcoming_Schedule")
    if sf2 != "All":
        sq += f" WHERE Sport_Name='{sf2}'"
    sched = run_query(sq + " LIMIT 60")
    if sched:
        sdf = pd.DataFrame(sched)
        def style_status(v):
            if v=="Completed": return "color:#4ade80;font-weight:bold"
            if v=="Scheduled": return "color:#818cf8;font-weight:bold"
            if v=="Cancelled": return "color:#f87171;font-weight:bold"
            return ""
        st.dataframe(sdf.style.map(style_status,subset=["Status"]),
                     use_container_width=True,hide_index=True)
    else:
        st.info("No matches scheduled yet.")

    st.divider()

    # ── Awards strip ──────────────────────────────────────────
    st.subheader("⭐ Live Tournament Awards")
    a1,a2,a3,a4 = st.columns(4)

    award_card = lambda icon,title,sub,clr: f"""
    <div style="background:#101726;border:1px solid #1e2d45;border-top:3px solid {clr};
    border-radius:12px;padding:12px 14px;text-align:center;margin-bottom:8px">
      <div style="font-size:1.5rem">{icon}</div>
      <div style="font-size:13px;font-weight:700;color:{clr};margin:4px 0">{title}</div>
      <div style="font-size:11px;color:#3a4a6a">{sub}</div>
    </div>"""

    with a1:
        st.markdown(award_card("🏏","Orange Cap","Most Runs","#a855f7"),unsafe_allow_html=True)
        r=run_query("SELECT p.Player_Name,t.Team_Name,SUM(sc.Runs_Scored) AS T FROM Scorecard_Cricket sc JOIN Players p ON sc.Player_ID=p.Player_ID JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sc.Player_ID ORDER BY T DESC LIMIT 1")
        if r: st.metric(r[0]["Player_Name"],f"{r[0]['T']} runs",r[0]["Team_Name"])
        else: st.caption("No data yet")

    with a2:
        st.markdown(award_card("🏏","Purple Cap","Most Wickets","#5b52f5"),unsafe_allow_html=True)
        r=run_query("SELECT p.Player_Name,t.Team_Name,SUM(sc.Wickets_Taken) AS T FROM Scorecard_Cricket sc JOIN Players p ON sc.Player_ID=p.Player_ID JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sc.Player_ID HAVING T>0 ORDER BY T DESC LIMIT 1")
        if r: st.metric(r[0]["Player_Name"],f"{r[0]['T']} wkts",r[0]["Team_Name"])
        else: st.caption("No data yet")

    with a3:
        st.markdown(award_card("⚽","Golden Boot","Most Goals","#22c55e"),unsafe_allow_html=True)
        r=run_query("SELECT p.Player_Name,t.Team_Name,SUM(sf.Goals) AS T FROM Scorecard_Football sf JOIN Players p ON sf.Player_ID=p.Player_ID JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sf.Player_ID ORDER BY T DESC LIMIT 1")
        if r: st.metric(r[0]["Player_Name"],f"{r[0]['T']} goals",r[0]["Team_Name"])
        else: st.caption("No data yet")

    with a4:
        st.markdown(award_card("🏀","MVP","Avg Points","#f97316"),unsafe_allow_html=True)
        r=run_query("SELECT p.Player_Name,t.Team_Name,ROUND(AVG(sb.Points),1) AS T FROM Scorecard_Basketball sb JOIN Players p ON sb.Player_ID=p.Player_ID JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sb.Player_ID ORDER BY T DESC LIMIT 1")
        if r: st.metric(r[0]["Player_Name"],f"{r[0]['T']} avg",r[0]["Team_Name"])
        else: st.caption("No data yet")


# ═══════════ TAB 2 — MATCH RESULTS (admin/manager) ═══════════
if can_edit:
    with tab_results:
        st.subheader("🏆 Update Match Result")
        st.markdown("""
        <div style="padding:10px 16px;border-radius:8px;border-left:3px solid #5b52f5;
        background:rgba(91,82,245,.07);font-size:13px;margin-bottom:20px">
        Calls <strong>UpdateMatchResult</strong> stored procedure — full ACID transaction.
        Trigger <code>trg_match_completed</code> auto-sets Status='Completed'.
        </div>""", unsafe_allow_html=True)

        scheduled = run_query("""
            SELECT m.Match_ID,
              CONCAT(sp.Sport_Name,' | ',ta.Team_Name,' vs ',tb.Team_Name,
                     '  (',m.Match_Date,')  [',m.Stage,']') AS Match_Desc,
              ta.Team_Name AS Team_A, tb.Team_Name AS Team_B,
              ta.Team_ID AS TID_A, tb.Team_ID AS TID_B
            FROM Matches m
            JOIN Sports sp ON m.Sport_ID=sp.Sport_ID
            JOIN Teams ta ON m.Team_A_ID=ta.Team_ID
            JOIN Teams tb ON m.Team_B_ID=tb.Team_ID
            WHERE m.Status='Scheduled' ORDER BY m.Match_Date
        """)
        if scheduled:
            mdict = {r["Match_Desc"]: r for r in scheduled}
            sel   = mdict[st.selectbox("Select match", list(mdict.keys()))]
            winner_label = st.radio("Who won?", [sel["Team_A"], sel["Team_B"]],
                                    horizontal=True, key="wr")
            wid = sel["TID_A"] if winner_label == sel["Team_A"] else sel["TID_B"]
            if st.button("🏆 Confirm & Save Result", use_container_width=True):
                with st.spinner("Running ACID transaction…"):
                    _, err = call_procedure("UpdateMatchResult", (sel["Match_ID"], wid))
                    time.sleep(0.4)
                if err:
                    st.error(f"❌ {err}")
                else:
                    st.success(f"✅ **{winner_label}** wins! Trigger fired → Status='Completed'. Audit logged.")
                    st.balloons(); time.sleep(1.5); st.rerun()
        else:
            st.info("All matches are completed or none are scheduled.")

        st.divider()
        st.subheader("✅ Completed Results")
        done = run_query("""
            SELECT sp.Sport_Name,ta.Team_Name AS Team_A,tb.Team_Name AS Team_B,
                   tw.Team_Name AS Winner, m.Match_Date, m.Stage
            FROM Matches m
            JOIN Sports sp ON m.Sport_ID=sp.Sport_ID
            JOIN Teams ta ON m.Team_A_ID=ta.Team_ID
            JOIN Teams tb ON m.Team_B_ID=tb.Team_ID
            JOIN Teams tw ON m.Winner_Team_ID=tw.Team_ID
            WHERE m.Status='Completed' ORDER BY m.Match_Date DESC
        """)
        if done:
            st.dataframe(pd.DataFrame(done), use_container_width=True, hide_index=True)
        else:
            st.info("No completed matches yet.")


# ═══════════ TAB 3 — TEAMS ═══════════════════════════════════
with tab_teams:
    st.subheader("🏟️ Team Management")
    sports_list = run_query("SELECT Sport_ID,Sport_Name,Icon FROM Sports ORDER BY Sport_Name")
    sport_map   = {f"{s['Icon']} {s['Sport_Name']}": s["Sport_ID"] for s in sports_list} if sports_list else {}

    cf, cl = st.columns([1,1.4])
    with cf:
        st.markdown("**➕ Register a New Team**")
        with st.form("add_team", clear_on_submit=True):
            tname = st.text_input("Team Name *", placeholder="e.g. DTU Warriors")
            uni   = st.text_input("University *", placeholder="e.g. Delhi Tech. University")
            sport = st.selectbox("Sport *", list(sport_map.keys()) if sport_map else ["—"])
            coach = st.text_input("Coach Name *", placeholder="e.g. Rahul Dravid")
            if st.form_submit_button("✅ Add Team", use_container_width=True):
                if not all([tname.strip(), uni.strip(), coach.strip()]):
                    st.error("❌ All fields required.")
                elif not sport_map:
                    st.error("❌ No sports in database.")
                else:
                    rows = run_query(
                        "INSERT INTO Teams (Team_Name,University,Sport_ID,Coach_Name) VALUES (%s,%s,%s,%s)",
                        (tname.strip(), uni.strip(), sport_map[sport], coach.strip()), fetch=False
                    )
                    time.sleep(0.3)
                    if rows:
                        st.balloons(); st.toast(f"'{tname}' added!", icon="✅"); time.sleep(1); st.rerun()
                    else:
                        st.error("❌ Failed — team may already exist for this sport.")

    with cl:
        st.markdown("**📋 All Teams**")
        tdata = run_query("""
            SELECT t.Team_Name, t.University, sp.Sport_Name AS Sport,
                   t.Coach_Name, t.Group_Name AS `Group`,
                   COUNT(p.Player_ID) AS Players
            FROM Teams t
            JOIN Sports sp ON t.Sport_ID=sp.Sport_ID
            LEFT JOIN Players p ON p.Team_ID=t.Team_ID
            GROUP BY t.Team_ID ORDER BY sp.Sport_Name, t.Team_Name
        """)
        if tdata:
            st.dataframe(pd.DataFrame(tdata), use_container_width=True, hide_index=True)


# ═══════════ TAB 4 — PLAYERS ═════════════════════════════════
with tab_players:
    st.subheader("👤 Player Management")
    all_teams = run_query("""
        SELECT t.Team_ID,t.Team_Name,t.University,sp.Sport_Name,sp.Icon
        FROM Teams t JOIN Sports sp ON t.Sport_ID=sp.Sport_ID
        ORDER BY sp.Sport_Name, t.Team_Name
    """)
    team_map = {
        f"{t['Icon']} {t['Team_Name']} ({t['University']})": t["Team_ID"]
        for t in all_teams
    } if all_teams else {}

    pf, pl = st.columns([1,1.4])
    with pf:
        st.markdown("**➕ Register a Player**")
        with st.form("add_player", clear_on_submit=True):
            pname  = st.text_input("Player Name *", placeholder="e.g. Arjun Mehta")
            tsel   = st.selectbox("Team *", list(team_map.keys()) if team_map else ["—"])
            prole  = st.text_input("Role *", placeholder="e.g. Batsman, Striker, Guard")
            jersey = st.number_input("Jersey No *", min_value=1, max_value=99, value=10)
            if st.form_submit_button("✅ Register Player", use_container_width=True):
                if not pname.strip() or not prole.strip():
                    st.error("❌ Name and role required.")
                elif not team_map:
                    st.error("❌ No teams yet.")
                else:
                    _, err = call_procedure(
                        "RegisterPlayer", (pname.strip(), team_map[tsel], prole.strip(), int(jersey))
                    )
                    time.sleep(0.3)
                    if err:
                        if "jersey" in err.lower():
                            st.error(f"❌ Jersey #{jersey} already taken. Pick another.")
                        else:
                            st.error(f"❌ {err}")
                    else:
                        st.toast(f"{pname} registered!", icon="✅"); time.sleep(1); st.rerun()

    with pl:
        st.markdown("**📋 All Players**")
        sf3 = st.selectbox("Sport filter",
                           ["All"]+[s["Sport_Name"] for s in (sports_list or [])],
                           key="plist_sf", label_visibility="collapsed")
        pq = """SELECT p.Player_Name,t.Team_Name,sp.Sport_Name AS Sport,
                       p.Role,p.Jersey_No AS Jersey,p.Form_Status
                FROM Players p JOIN Teams t ON p.Team_ID=t.Team_ID
                JOIN Sports sp ON t.Sport_ID=sp.Sport_ID"""
        if sf3 != "All":
            pq += f" WHERE sp.Sport_Name='{sf3}'"
        pq += " ORDER BY sp.Sport_Name,t.Team_Name,p.Player_Name"
        pdata = run_query(pq)
        if pdata:
            pdf = pd.DataFrame(pdata)
            def color_form(v):
                if v=="In Form":     return "color:#4ade80;font-weight:bold"
                if v=="Out of Form": return "color:#f87171;font-weight:bold"
                return "color:#4a5568"
            st.dataframe(pdf.style.map(color_form,subset=["Form_Status"]),
                         use_container_width=True,hide_index=True)
        else:
            st.info("No players yet.")