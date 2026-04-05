# page_cricket.py — ARENA SNU Cricket Module v7
# SURGE 2025 · Assigned: Ashank · Reviewed: Mudit
import streamlit as st, time, pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db_connection import run_query

try: st.set_page_config(page_title="Cricket — ARENA SNU", page_icon="🏏", layout="wide")
except: pass

st.markdown("""<style>
div.stButton>button{background:linear-gradient(135deg,#5b52f5,#9333ea);color:#fff;
font-weight:700;border-radius:10px;border:none;transition:all .25s}
div.stButton>button:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(91,82,245,.5)}
footer{visibility:hidden}</style>""", unsafe_allow_html=True)

st.markdown("""
<h2 style="background:linear-gradient(90deg,#a855f7,#5b52f5);-webkit-background-clip:text;
-webkit-text-fill-color:transparent;font-family:'Rajdhani',sans-serif;
font-size:2rem;font-weight:700;margin:0">🏏 Cricket Module</h2>
<p style="color:#4a5568;font-size:.875rem;margin-top:4px">
T20 Format · Score Entry · Orange/Purple Cap · Player Form</p>
""", unsafe_allow_html=True)
st.divider()

role      = st.session_state.get("role","viewer")
CAN_ENTER = role in ("admin","organiser")
tabs      = st.tabs(["📝 Enter Score","📊 Leaderboards","🔥 Player Form"] if CAN_ENTER
                    else ["📊 Leaderboards","🔥 Player Form"])
tab_entry  = tabs[0] if CAN_ENTER else None
tab_boards = tabs[1] if CAN_ENTER else tabs[0]
tab_form   = tabs[2] if CAN_ENTER else tabs[1]

# ── ENTRY ─────────────────────────────────────────────────────
if CAN_ENTER:
    with tab_entry:
        matches = run_query("""
            SELECT m.Match_ID,
                   CONCAT(ta.Team_Name,' vs ',tb.Team_Name,' (',m.Match_Date,') [',m.Stage,']') AS Match_Desc,
                   m.Team_A_ID, m.Team_B_ID
            FROM Matches m
            JOIN Teams ta ON m.Team_A_ID=ta.Team_ID JOIN Teams tb ON m.Team_B_ID=tb.Team_ID
            WHERE m.Sport_ID=1 AND m.Status='Scheduled' ORDER BY m.Match_Date
        """)
        if not matches:
            st.warning("⚠️ No scheduled cricket matches found. Schedule one first.")
        else:
            md = {r["Match_Desc"]: r for r in matches}
            sel = md[st.selectbox("Select Match", list(md.keys()))]
            mid = sel["Match_ID"]

            players = run_query("""
                SELECT p.Player_ID,
                       CONCAT(p.Player_Name,'  (',t.Team_Name,')  — ',p.Role) AS PDesc
                FROM Players p JOIN Teams t ON p.Team_ID=t.Team_ID
                WHERE p.Team_ID IN (%s,%s) ORDER BY t.Team_Name, p.Player_Name
            """, (sel["Team_A_ID"], sel["Team_B_ID"]))
            if not players:
                st.warning("⚠️ No players for these teams.")
            else:
                pd2 = {r["PDesc"]: r["Player_ID"] for r in players}
                pid = pd2[st.selectbox("Select Player", list(pd2.keys()))]

                ex = run_query("SELECT Runs_Scored,Wickets_Taken,Overs_Bowled,Catches "
                               "FROM Scorecard_Cricket WHERE Match_ID=%s AND Player_ID=%s",
                               (mid, pid))
                if ex:
                    e=ex[0]
                    st.info(f"⚠️ Existing entry — Runs: {e['Runs_Scored']} | Wkts: {e['Wickets_Taken']} "
                            f"| Overs: {e['Overs_Bowled']} | Catches: {e['Catches']}")

                with st.form("cricket_form", clear_on_submit=True):
                    c1,c2 = st.columns(2)
                    with c1:
                        runs    = st.number_input("Runs Scored",   min_value=0, max_value=200)
                        wickets = st.number_input("Wickets Taken", min_value=0, max_value=10)
                    with c2:
                        overs   = st.number_input("Overs Bowled",  min_value=0.0, max_value=20.0, step=0.1)
                        catches = st.number_input("Catches",        min_value=0, max_value=10)
                    sub = st.form_submit_button("🏏 Submit Score", use_container_width=True)

                if sub:
                    if round(overs % 1, 1) > 0.5:
                        st.error("❌ Invalid overs — decimal must be 0–5 (e.g. 3.4, not 3.7)")
                    else:
                        with st.spinner("Writing to MySQL…"):
                            run_query(
                                "INSERT INTO Scorecard_Cricket "
                                "(Match_ID,Player_ID,Runs_Scored,Wickets_Taken,Overs_Bowled,Catches) "
                                "VALUES (%s,%s,%s,%s,%s,%s)",
                                (mid,pid,runs,wickets,overs,catches), fetch=False
                            )
                            time.sleep(0.4)
                        st.toast("Score recorded! trg_player_form fired.", icon="✅")
                        time.sleep(1); st.rerun()

# ── LEADERBOARDS ──────────────────────────────────────────────
with tab_boards:
    if not CAN_ENTER:
        st.info("🔒 Score entry restricted to Organisers.")
    left, right = st.columns(2)

    with left:
        st.subheader("🏅 Orange Cap — Top Runs")
        oc = run_query("""
            SELECT p.Player_Name,t.Team_Name,t.University,
                   SUM(sc.Runs_Scored) AS Runs, COUNT(DISTINCT sc.Match_ID) AS Innings
            FROM Scorecard_Cricket sc JOIN Players p ON sc.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sc.Player_ID ORDER BY Runs DESC
        """)
        if oc:
            df=pd.DataFrame(oc); df.insert(0,"Rank",range(1,len(df)+1))
            def hl(r): return ["background:rgba(168,85,247,.12)"]*len(r) if r["Rank"]==1 else [""]*len(r)
            st.dataframe(df.style.apply(hl,axis=1),use_container_width=True,hide_index=True)
            fig=px.bar(df.head(8),x="Player_Name",y="Runs",color="Team_Name",
                       color_discrete_sequence=px.colors.qualitative.Vivid,
                       title="Top Run Scorers")
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                              font_color="#e8ecf4",showlegend=False,
                              margin=dict(t=36,b=0,l=0,r=0),
                              xaxis=dict(gridcolor="#1e2d45"),yaxis=dict(gridcolor="#1e2d45"))
            st.plotly_chart(fig,use_container_width=True)
        else:
            st.info("No batting data yet.")

    with right:
        st.subheader("💜 Purple Cap — Top Wickets")
        pc = run_query("""
            SELECT p.Player_Name,t.Team_Name,SUM(sc.Wickets_Taken) AS Wickets,
                   ROUND(SUM(sc.Overs_Bowled),1) AS Overs
            FROM Scorecard_Cricket sc JOIN Players p ON sc.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID
            GROUP BY sc.Player_ID HAVING Wickets>0 ORDER BY Wickets DESC
        """)
        if pc:
            df2=pd.DataFrame(pc); df2.insert(0,"Rank",range(1,len(df2)+1))
            def hl2(r): return ["background:rgba(91,82,245,.12)"]*len(r) if r["Rank"]==1 else [""]*len(r)
            st.dataframe(df2.style.apply(hl2,axis=1),use_container_width=True,hide_index=True)
            fig2=px.bar(df2.head(8),x="Player_Name",y="Wickets",
                        color_discrete_sequence=["#a855f7"],title="Top Wicket Takers")
            fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                               font_color="#e8ecf4",showlegend=False,
                               margin=dict(t=36,b=0,l=0,r=0),
                               xaxis=dict(gridcolor="#1e2d45"),yaxis=dict(gridcolor="#1e2d45"))
            st.plotly_chart(fig2,use_container_width=True)
        else:
            st.info("No bowling data yet.")

    st.divider()
    with st.expander("📋 Full Scorecard — All Players"):
        full = run_query("""
            SELECT p.Player_Name,t.Team_Name,SUM(sc.Runs_Scored) AS Runs,
                   SUM(sc.Wickets_Taken) AS Wickets,ROUND(SUM(sc.Overs_Bowled),1) AS Overs,
                   SUM(sc.Catches) AS Catches,COUNT(DISTINCT sc.Match_ID) AS Matches
            FROM Scorecard_Cricket sc JOIN Players p ON sc.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sc.Player_ID ORDER BY Runs DESC
        """)
        if full: st.dataframe(pd.DataFrame(full),use_container_width=True,hide_index=True)
        else:    st.info("No data yet.")

# ── FORM TRACKER ──────────────────────────────────────────────
with tab_form:
    st.subheader("🔥 Player Form Tracker")
    st.markdown("""
    <div style="padding:10px 16px;border-radius:8px;border-left:3px solid #5b52f5;
    background:rgba(91,82,245,.07);font-size:13px;margin-bottom:16px">
    Form auto-updated by <code>trg_player_form</code> after every score entry.
    🟢 In Form = last-5 avg ≥ 120% of overall · 🔴 Out of Form = ≤ 80%
    </div>""", unsafe_allow_html=True)
    fdata = run_query("""
        SELECT p.Player_Name,t.Team_Name,p.Form_Status,
               ROUND(IFNULL(AVG(sc.Runs_Scored),0),1) AS Avg_Runs,
               IFNULL(SUM(sc.Wickets_Taken),0) AS Wickets
        FROM Players p JOIN Teams t ON p.Team_ID=t.Team_ID
        LEFT JOIN Scorecard_Cricket sc ON sc.Player_ID=p.Player_ID
        WHERE t.Sport_ID=1
        GROUP BY p.Player_ID
        ORDER BY CASE p.Form_Status WHEN 'In Form' THEN 1 WHEN 'Neutral' THEN 2 ELSE 3 END, Avg_Runs DESC
    """)
    if fdata:
        fdf=pd.DataFrame(fdata)
        fdf["Status"]=fdf["Form_Status"].map({"In Form":"🔥 In Form","Out of Form":"❄️ Out of Form","Neutral":"➖ Neutral"}).fillna("➖ Neutral")
        def cf(v):
            if "In Form" in str(v):     return "color:#4ade80;font-weight:bold"
            if "Out of Form" in str(v): return "color:#f87171;font-weight:bold"
            return "color:#4a5568"
        st.dataframe(fdf[["Player_Name","Team_Name","Status","Avg_Runs","Wickets"]].style.map(cf,subset=["Status"]),
                     use_container_width=True,hide_index=True)
    else:
        st.info("No player data available.")