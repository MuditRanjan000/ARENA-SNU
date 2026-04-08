# page_basketball.py — ARENA SNU Basketball Module v7
# SURGE 2025 · Assigned: Amitog · Reviewed: Mudit
import streamlit as st, time, pandas as pd
import plotly.express as px
from db_connection import run_query

try: st.set_page_config(page_title="Basketball — ARENA SNU", page_icon="🏀", layout="wide")
except: pass

st.markdown("""<style>
div.stButton>button{background:linear-gradient(135deg,#5b52f5,#9333ea);color:#fff;
font-weight:700;border-radius:10px;border:none;transition:all .25s}
div.stButton>button:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(91,82,245,.5)}
footer{visibility:hidden}</style>""", unsafe_allow_html=True)

st.markdown("""
<h2 style="background:linear-gradient(90deg,#f97316,#5b52f5);-webkit-background-clip:text;
-webkit-text-fill-color:transparent;font-family:'Rajdhani',sans-serif;
font-size:2rem;font-weight:700;margin:0">🏀 Basketball Module</h2>
<p style="color:#4a5568;font-size:.875rem;margin-top:4px">
Score Entry · MVP Leaderboard · Team Stats</p>
""", unsafe_allow_html=True)
st.divider()

role      = st.session_state.get("role","viewer")
CAN_ENTER = role in ("admin","organiser")
tabs      = st.tabs(["📝 Enter Stats","📊 Leaderboard","📈 Team Charts"] if CAN_ENTER
                    else ["📊 Leaderboard","📈 Team Charts"])
tab_entry = tabs[0] if CAN_ENTER else None
tab_lb    = tabs[1] if CAN_ENTER else tabs[0]
tab_chart = tabs[2] if CAN_ENTER else tabs[1]

# ── ENTRY ─────────────────────────────────────────────────────
if CAN_ENTER:
    with tab_entry:
        matches = run_query("""
            SELECT m.Match_ID,
                   CONCAT(ta.Team_Name,' vs ',tb.Team_Name,'  (',m.Match_Date,')  [',m.Stage,']') AS Match_Desc,
                   m.Team_A_ID, m.Team_B_ID
            FROM Matches m JOIN Teams ta ON m.Team_A_ID=ta.Team_ID JOIN Teams tb ON m.Team_B_ID=tb.Team_ID
            WHERE m.Sport_ID=3 ORDER BY m.Match_Date DESC
        """)
        if not matches:
            st.warning("⚠️ No basketball matches found.")
        else:
            md = {r["Match_Desc"]: r for r in matches}
            sel = md[st.selectbox("Select Match", list(md.keys()))]
            mid = sel["Match_ID"]
            players = run_query("""
                SELECT p.Player_ID,CONCAT(p.Player_Name,'  (',t.Team_Name,')  — ',p.Role) AS PDesc
                FROM Players p JOIN Teams t ON p.Team_ID=t.Team_ID
                WHERE p.Team_ID IN (%s,%s) ORDER BY t.Team_Name, p.Player_Name
            """, (sel["Team_A_ID"], sel["Team_B_ID"]))
            if not players:
                st.warning("⚠️ No players found.")
            else:
                pd2 = {r["PDesc"]: r["Player_ID"] for r in players}
                pid = pd2[st.selectbox("Select Player", list(pd2.keys()))]

                ex = run_query("SELECT COUNT(*) AS c FROM Scorecard_Basketball WHERE Match_ID=%s AND Player_ID=%s",
                               (mid,pid))
                if ex and ex[0]["c"] > 0:
                    st.warning("⚠️ Entry exists for this player/match. Submitting adds another record.")

                with st.form("bball_form", clear_on_submit=True):
                    c1,c2 = st.columns(2)
                    with c1:
                        pts = st.number_input("Points",   min_value=0, max_value=100)
                        reb = st.number_input("Rebounds", min_value=0, max_value=50)
                    with c2:
                        ast = st.number_input("Assists",  min_value=0, max_value=30)
                        stl = st.number_input("Steals",   min_value=0, max_value=20)
                    if st.form_submit_button("🏀 Submit Stats", use_container_width=True):
                        with st.spinner("Writing to MySQL…"):
                            run_query(
                                "INSERT INTO Scorecard_Basketball "
                                "(Match_ID,Player_ID,Points,Rebounds,Assists,Steals) "
                                "VALUES (%s,%s,%s,%s,%s,%s)",
                                (mid,pid,pts,reb,ast,stl), fetch=False
                            )
                            time.sleep(0.4)
                        st.toast("Stats recorded!", icon="✅"); time.sleep(1); st.rerun()

# ── LEADERBOARD ────────────────────────────────────────────────
with tab_lb:
    if not CAN_ENTER:
        st.info("🔒 Score entry restricted to Organisers.")
    data = run_query("""
        SELECT p.Player_Name, t.Team_Name,
               SUM(sb.Points) AS Total_Points, SUM(sb.Rebounds) AS Total_Rebounds,
               SUM(sb.Assists) AS Total_Assists, SUM(sb.Steals) AS Total_Steals,
               ROUND(AVG(sb.Points),1) AS Avg_Points, COUNT(DISTINCT sb.Match_ID) AS Games
        FROM Scorecard_Basketball sb JOIN Players p ON sb.Player_ID=p.Player_ID
        JOIN Teams t ON p.Team_ID=t.Team_ID
        GROUP BY sb.Player_ID ORDER BY Total_Points DESC
    """)
    if not data:
        st.info("No basketball data yet.")
    else:
        df=pd.DataFrame(data); df.insert(0,"Rank",range(1,len(df)+1))
        mvp=df.iloc[0]
        st.markdown(f"""
        <div style="padding:12px 18px;border-radius:10px;border-left:4px solid #f97316;
        background:rgba(249,115,22,.08);margin-bottom:16px;font-size:14px">
        🏀 <strong>MVP:</strong> {mvp['Player_Name']} <span style="color:#4a5568">({mvp['Team_Name']})</span> —
        <strong style="color:#fdba74">{mvp['Total_Points']} pts · {mvp['Avg_Points']} avg</strong>
        </div>""", unsafe_allow_html=True)
        def hl(r): return ["background:rgba(249,115,22,.1)"]*len(r) if r["Rank"]==1 else [""]*len(r)
        st.dataframe(df.style.apply(hl,axis=1),use_container_width=True,hide_index=True)

# ── TEAM CHARTS ───────────────────────────────────────────────
with tab_chart:
    data2 = run_query("""
        SELECT p.Player_Name, t.Team_Name,
               SUM(sb.Points) AS Points, SUM(sb.Rebounds) AS Rebounds,
               SUM(sb.Assists) AS Assists, SUM(sb.Steals) AS Steals
        FROM Scorecard_Basketball sb JOIN Players p ON sb.Player_ID=p.Player_ID
        JOIN Teams t ON p.Team_ID=t.Team_ID
        GROUP BY sb.Player_ID ORDER BY Points DESC
    """)
    if data2:
        df3=pd.DataFrame(data2)
        fig=px.bar(df3.head(12), x="Player_Name",
                   y=["Points","Rebounds","Assists","Steals"],
                   barmode="group",
                   color_discrete_sequence=["#f97316","#5b52f5","#a855f7","#22c55e"],
                   labels={"Player_Name":"Player","value":"Count","variable":"Stat"},
                   title="Top Players — All Stats")
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                          font_color="#e8ecf4",margin=dict(t=36,b=0,l=0,r=0),
                          xaxis=dict(gridcolor="#1e2d45"),yaxis=dict(gridcolor="#1e2d45"),
                          legend=dict(orientation="h",y=1.1))
        st.plotly_chart(fig,use_container_width=True)

        # Team totals
        team_totals = run_query("""
            SELECT t.Team_Name,SUM(sb.Points) AS Points,SUM(sb.Rebounds) AS Rebounds,
                   SUM(sb.Assists) AS Assists
            FROM Scorecard_Basketball sb JOIN Players p ON sb.Player_ID=p.Player_ID
            JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY p.Team_ID ORDER BY Points DESC
        """)
        if team_totals:
            st.divider()
            st.subheader("Team Totals")
            fig2=px.bar(pd.DataFrame(team_totals), x="Team_Name",
                        y=["Points","Rebounds","Assists"], barmode="group",
                        color_discrete_sequence=["#f97316","#5b52f5","#a855f7"],
                        title="Team Comparison")
            fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                               font_color="#e8ecf4",margin=dict(t=36,b=0,l=0,r=0),
                               xaxis=dict(gridcolor="#1e2d45"),yaxis=dict(gridcolor="#1e2d45"))
            st.plotly_chart(fig2,use_container_width=True)
    else:
        st.info("No basketball data yet.")