# page_basketball.py — ARENA SNU Basketball Module v5
# Assigned: Amitog | Integrated by: Mudit
import streamlit as st
import time
import pandas as pd
import plotly.express as px
from db_connection import run_query

try:
    st.set_page_config(page_title="Basketball — ARENA SNU", page_icon="🏀", layout="wide")
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
<h2 style="background:linear-gradient(90deg,#f97316,#6c63ff);
   -webkit-background-clip:text;-webkit-text-fill-color:transparent;
   font-size:2rem;font-weight:800;margin:0">🏀 Basketball Module</h2>
<p style="color:#6b7a99;font-size:.875rem;margin-top:4px">Score Entry · MVP Leaderboard · Team Stats</p>
""", unsafe_allow_html=True)
st.divider()

user_role = st.session_state.get("role", "viewer")
CAN_ENTER = user_role in ("admin", "organiser")

tabs     = ["📝 Enter Stats", "📊 Leaderboards"] if CAN_ENTER else ["📊 Leaderboards"]
tab_list = st.tabs(tabs)
tab1     = tab_list[0] if CAN_ENTER else None
tab2     = tab_list[1] if CAN_ENTER else tab_list[0]

# ── SCORE ENTRY ──────────────────────────────────────────────
if CAN_ENTER:
    with tab1:
        matches = run_query("""
            SELECT m.Match_ID,
                   CONCAT(ta.Team_Name,' vs ',tb.Team_Name,'  (',m.Match_Date,')  [',m.Stage,']') AS Match_Desc,
                   m.Team_A_ID, m.Team_B_ID
            FROM Matches m
            JOIN Teams ta ON m.Team_A_ID=ta.Team_ID
            JOIN Teams tb ON m.Team_B_ID=tb.Team_ID
            WHERE m.Sport_ID=(SELECT Sport_ID FROM Sports WHERE Sport_Name='Basketball')
            ORDER BY m.Match_Date DESC
        """)
        if not matches:
            st.warning("⚠️ No basketball matches found. Schedule a match first.")
        else:
            match_dict = {r["Match_Desc"]: r for r in matches}
            sel_match  = match_dict[st.selectbox("Select Match", list(match_dict.keys()))]
            match_id   = sel_match["Match_ID"]

            players = run_query("""
                SELECT p.Player_ID,
                       CONCAT(p.Player_Name,'  (',t.Team_Name,')  — ',p.Role) AS Player_Desc
                FROM Players p JOIN Teams t ON p.Team_ID=t.Team_ID
                WHERE p.Team_ID IN (%s,%s)
                ORDER BY t.Team_Name, p.Player_Name
            """, (sel_match["Team_A_ID"], sel_match["Team_B_ID"]))

            if not players:
                st.warning("⚠️ No players found for these teams.")
            else:
                player_dict = {r["Player_Desc"]: r["Player_ID"] for r in players}
                player_id   = player_dict[st.selectbox("Select Player", list(player_dict.keys()))]

                existing = run_query("SELECT COUNT(*) AS cnt FROM Scorecard_Basketball WHERE Match_ID=%s AND Player_ID=%s",
                                     (match_id, player_id))
                if existing and existing[0]["cnt"] > 0:
                    st.markdown("""<div style="padding:10px 16px;border-radius:8px;border-left:3px solid #f59e0b;
                    background:rgba(245,158,11,.07);font-size:13px;margin-bottom:8px">
                    ⚠️ Entry already exists. Submitting adds another record.</div>""", unsafe_allow_html=True)

                with st.form("bball_stats", clear_on_submit=True):
                    c1, c2 = st.columns(2)
                    with c1:
                        points   = st.number_input("Points",   min_value=0, max_value=100)
                        rebounds = st.number_input("Rebounds", min_value=0, max_value=50)
                    with c2:
                        assists  = st.number_input("Assists",  min_value=0, max_value=30)
                        steals   = st.number_input("Steals",   min_value=0, max_value=20)

                    if st.form_submit_button("🏀 Submit Stats", use_container_width=True):
                        with st.spinner("Recording to MySQL…"):
                            run_query(
                                "INSERT INTO Scorecard_Basketball (Match_ID,Player_ID,Points,Rebounds,Assists,Steals) "
                                "VALUES (%s,%s,%s,%s,%s,%s)",
                                (match_id, player_id, points, rebounds, assists, steals), fetch=False
                            )
                            time.sleep(0.4)
                        st.toast("Stats recorded!", icon="✅")
                        time.sleep(1)
                        st.rerun()

# ── LEADERBOARDS ─────────────────────────────────────────────
with tab2:
    if not CAN_ENTER:
        st.info("🔒 Score entry is restricted to **Organisers**.")

    data = run_query("""
        SELECT p.Player_Name, t.Team_Name,
               SUM(sb.Points) AS Total_Points, SUM(sb.Rebounds) AS Total_Rebounds,
               SUM(sb.Assists) AS Total_Assists, SUM(sb.Steals) AS Total_Steals,
               ROUND(AVG(sb.Points),1) AS Avg_Points,
               COUNT(DISTINCT sb.Match_ID) AS Games
        FROM Scorecard_Basketball sb
        JOIN Players p ON sb.Player_ID=p.Player_ID
        JOIN Teams t ON p.Team_ID=t.Team_ID
        GROUP BY sb.Player_ID ORDER BY Total_Points DESC
    """)
    if not data:
        st.info("No basketball data yet.")
    else:
        df = pd.DataFrame(data)
        df.insert(0, "Rank", range(1, len(df)+1))
        mvp = df.iloc[0]
        st.markdown(f"""<div style="padding:12px 18px;border-radius:10px;border-left:4px solid #f97316;
        background:rgba(249,115,22,.08);margin-bottom:16px;font-size:14px">
        🏀 <strong>MVP:</strong> {mvp['Player_Name']} <span style="color:#6b7a99">({mvp['Team_Name']})</span> —
        <strong style="color:#fdba74">{mvp['Total_Points']} pts · {mvp['Avg_Points']} avg</strong></div>""",
        unsafe_allow_html=True)

        def hl(row): return ["background-color:rgba(249,115,22,.1)"]*len(row) if row["Rank"]==1 else [""]*len(row)
        st.dataframe(df.style.apply(hl, axis=1), use_container_width=True, hide_index=True)

        st.divider()
        fig = px.bar(df.head(10), x="Player_Name",
                     y=["Total_Points","Total_Rebounds","Total_Assists","Total_Steals"],
                     barmode="group",
                     color_discrete_sequence=["#f97316","#6c63ff","#a855f7","#22c55e"],
                     labels={"Player_Name":"Player","value":"Count","variable":"Stat"},
                     title="Top Players — All Stats")
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          font_color="#e8ecf4", xaxis=dict(gridcolor="#252c3d"),
                          yaxis=dict(gridcolor="#252c3d"), margin=dict(t=36,b=0,l=0,r=0),
                          legend=dict(orientation="h",y=1.1))
        st.plotly_chart(fig, use_container_width=True)