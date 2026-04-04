# page_volleyball.py — ARENA SNU Volleyball Module v6
# SURGE 2025 · Shiv Nadar University
import streamlit as st
import time
import pandas as pd
import plotly.express as px
from db_connection import run_query

try:
    st.set_page_config(page_title="Volleyball — ARENA SNU", page_icon="🏐", layout="wide")
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
<h2 style="background:linear-gradient(90deg,#f59e0b,#6c63ff);
   -webkit-background-clip:text;-webkit-text-fill-color:transparent;
   font-size:2rem;font-weight:800;margin:0">🏐 Volleyball Module</h2>
<p style="color:#6b7a99;font-size:.875rem;margin-top:4px">Score Entry · Kills · Blocks · Aces · Digs</p>
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
            WHERE m.Sport_ID=(SELECT Sport_ID FROM Sports WHERE Sport_Name='Volleyball')
            ORDER BY m.Match_Date DESC
        """)
        if not matches:
            st.warning("⚠️ No volleyball matches found. Schedule a match first.")
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

                with st.form("vb_stats", clear_on_submit=True):
                    c1, c2 = st.columns(2)
                    with c1:
                        kills  = st.number_input("Kills",  min_value=0, max_value=50)
                        blocks = st.number_input("Blocks", min_value=0, max_value=30)
                    with c2:
                        aces = st.number_input("Aces", min_value=0, max_value=30)
                        digs = st.number_input("Digs", min_value=0, max_value=50)

                    if st.form_submit_button("🏐 Submit Stats", use_container_width=True):
                        with st.spinner("Recording to MySQL…"):
                            run_query(
                                "INSERT INTO Scorecard_Volleyball (Match_ID,Player_ID,Kills,Blocks,Aces,Digs) "
                                "VALUES (%s,%s,%s,%s,%s,%s)",
                                (match_id, player_id, kills, blocks, aces, digs), fetch=False
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
        SELECT p.Player_Name, t.Team_Name, p.Role,
               SUM(sv.Kills)   AS Total_Kills,
               SUM(sv.Blocks)  AS Total_Blocks,
               SUM(sv.Aces)    AS Total_Aces,
               SUM(sv.Digs)    AS Total_Digs,
               COUNT(DISTINCT sv.Match_ID) AS Matches
        FROM Scorecard_Volleyball sv
        JOIN Players p ON sv.Player_ID=p.Player_ID
        JOIN Teams t ON p.Team_ID=t.Team_ID
        GROUP BY sv.Player_ID ORDER BY Total_Kills DESC
    """)

    if not data:
        st.info("No volleyball data yet. Enter match scores using the organiser account.")
        scheduled = run_query("""
            SELECT CONCAT(ta.Team_Name,' vs ',tb.Team_Name) AS Match,
                   m.Match_Date, m.Stage
            FROM Matches m
            JOIN Teams ta ON m.Team_A_ID=ta.Team_ID
            JOIN Teams tb ON m.Team_B_ID=tb.Team_ID
            JOIN Sports sp ON m.Sport_ID=sp.Sport_ID
            WHERE sp.Sport_Name='Volleyball' AND m.Status='Scheduled'
        """)
        if scheduled:
            st.markdown("**Upcoming Volleyball Fixtures:**")
            st.dataframe(pd.DataFrame(scheduled), use_container_width=True, hide_index=True)
    else:
        df = pd.DataFrame(data)
        df.insert(0, "Rank", range(1, len(df)+1))

        # Top performer highlight
        top = df.iloc[0]
        st.markdown(f"""<div style="padding:12px 18px;border-radius:10px;border-left:4px solid #f59e0b;
        background:rgba(245,158,11,.08);margin-bottom:16px;font-size:14px">
        🏐 <strong>Top Killer:</strong> {top['Player_Name']} <span style="color:#6b7a99">({top['Team_Name']})</span> —
        <strong style="color:#fcd34d">{top['Total_Kills']} kills · {top['Total_Aces']} aces</strong></div>""",
        unsafe_allow_html=True)

        st.dataframe(df, use_container_width=True, hide_index=True)

        st.divider()
        fig = px.bar(df.head(10), x="Player_Name",
                     y=["Total_Kills","Total_Blocks","Total_Aces","Total_Digs"],
                     barmode="group",
                     color_discrete_sequence=["#f59e0b","#6c63ff","#a855f7","#22c55e"],
                     labels={"Player_Name":"Player","value":"Count","variable":"Stat"},
                     title="Top Players — All Stats")
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          font_color="#e8ecf4", xaxis=dict(gridcolor="#252c3d"),
                          yaxis=dict(gridcolor="#252c3d"), margin=dict(t=36,b=0,l=0,r=0),
                          legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("📋 Volleyball Match Results")
results = run_query("""
    SELECT ta.Team_Name AS Team_A, tb.Team_Name AS Team_B,
           IFNULL(tw.Team_Name,'TBD') AS Winner, m.Stage, m.Match_Date, m.Status
    FROM Matches m
    JOIN Teams ta ON m.Team_A_ID=ta.Team_ID
    JOIN Teams tb ON m.Team_B_ID=tb.Team_ID
    LEFT JOIN Teams tw ON m.Winner_Team_ID=tw.Team_ID
    JOIN Sports sp ON m.Sport_ID=sp.Sport_ID
    WHERE sp.Sport_Name='Volleyball'
    ORDER BY m.Match_Date
""")
if results:
    rdf = pd.DataFrame(results)
    def style_status(val):
        if val == "Completed": return "color:#10b981;font-weight:bold"
        if val == "Scheduled": return "color:#8b85ff;font-weight:bold"
        return ""
    st.dataframe(rdf.style.map(style_status, subset=["Status"]), use_container_width=True, hide_index=True)