# page_football.py — ARENA SNU Football Module v7
# SURGE 2025 · Assigned: Ayush · Reviewed: Mudit
import streamlit as st, time, pandas as pd
import plotly.express as px
from db_connection import run_query

try: st.set_page_config(page_title="Football — ARENA SNU", page_icon="⚽", layout="wide")
except: pass

st.markdown("""<style>
div.stButton>button{background:linear-gradient(135deg,#5b52f5,#9333ea);color:#fff;
font-weight:700;border-radius:10px;border:none;transition:all .25s}
div.stButton>button:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(91,82,245,.5)}
footer{visibility:hidden}</style>""", unsafe_allow_html=True)

st.markdown("""
<h2 style="font-family:'Rajdhani',sans-serif;font-size:2rem;font-weight:700;margin:0">
⚽ <span style="background:linear-gradient(90deg,#22c55e,#5b52f5);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Football Module</span>
</h2>
<p style="color:#4a5568;font-size:.875rem;margin-top:4px">
Score Entry · Golden Boot · Suspension Tracker</p>
""", unsafe_allow_html=True)
st.divider()

role      = st.session_state.get("role","viewer")
CAN_ENTER = role in ("admin","organiser")

def get_matches():
    return run_query("""
        SELECT m.Match_ID,
               CONCAT(ta.Team_Name,' vs ',tb.Team_Name,' | ',m.Stage,
                      ' | ',DATE_FORMAT(m.Match_Date,'%d %b %Y'),' @ ',v.Venue_Name) AS Label,
               m.Team_A_ID, m.Team_B_ID
        FROM Matches m JOIN Sports sp ON m.Sport_ID=sp.Sport_ID
        JOIN Teams ta ON m.Team_A_ID=ta.Team_ID JOIN Teams tb ON m.Team_B_ID=tb.Team_ID
        JOIN Venues v  ON m.Venue_ID=v.Venue_ID
        WHERE sp.Sport_Name='Football' ORDER BY m.Match_Date DESC
    """, fetch=True) or []

def get_players(ta, tb):
    return run_query("""
        SELECT p.Player_ID,
               CONCAT(p.Player_Name,' (',t.Team_Name,' | #',p.Jersey_No,')') AS Label, p.Role
        FROM Players p JOIN Teams t ON p.Team_ID=t.Team_ID
        WHERE p.Team_ID IN (%s,%s) ORDER BY t.Team_Name, p.Player_Name
    """, (ta,tb), fetch=True) or []

# ── SCORE ENTRY ───────────────────────────────────────────────
if CAN_ENTER:
    st.subheader("📋 Enter Match Score")
    matches = get_matches()
    if not matches:
        st.warning("No football matches found.")
    else:
        mdict = {r["Label"]: r for r in matches}
        sel   = mdict[st.selectbox("Select Match", list(mdict.keys()))]
        mid   = sel["Match_ID"]

        players = get_players(sel["Team_A_ID"], sel["Team_B_ID"])
        if not players:
            st.warning("No players for this match.")
        else:
            pdict = {r["Label"]: r for r in players}
            psel  = pdict[st.selectbox("Select Player", list(pdict.keys()))]
            pid   = psel["Player_ID"]

            if psel.get("Role") == "SUSPENDED":
                st.warning("⚠️ Player is SUSPENDED. Verify with referee before entering stats.")

            with st.form("football_score"):
                c1,c2,c3,c4 = st.columns(4)
                with c1: goals   = st.number_input("⚽ Goals",        min_value=0, max_value=20)
                with c2: assists = st.number_input("🎯 Assists",      min_value=0, max_value=20)
                with c3: yc      = st.number_input("🟨 Yellow Cards", min_value=0, max_value=2)
                with c4: rc      = st.number_input("🟥 Red Cards",    min_value=0, max_value=1)

                if st.form_submit_button("✅ Submit Score", type="primary"):
                    ex = run_query("SELECT COUNT(*) AS c FROM Scorecard_Football WHERE Match_ID=%s AND Player_ID=%s",
                                   (mid,pid), fetch=True)
                    if ex and ex[0]["c"] > 0:
                        st.error("🚫 Score already recorded for this player in this match.")
                    else:
                        with st.spinner("Writing to MySQL…"):
                            run_query(
                                "INSERT INTO Scorecard_Football "
                                "(Match_ID,Player_ID,Goals,Assists,Yellow_Cards,Red_Cards) "
                                "VALUES (%s,%s,%s,%s,%s,%s)",
                                (mid,pid,goals,assists,yc,rc), fetch=False
                            )
                            time.sleep(0.4)
                        st.toast("Saved! trg_suspend_player may have fired.", icon="✅")
                        time.sleep(1); st.rerun()
    st.divider()
else:
    st.info("🔒 Score entry restricted to **Organisers**.")
    st.divider()

# ── GOLDEN BOOT ────────────────────────────────────────────────
st.subheader("🏆 Golden Boot — Top Scorers")
gb = run_query("""
    SELECT p.Player_Name AS Player, t.Team_Name AS Team, t.University,
           SUM(sf.Goals) AS Goals, SUM(sf.Assists) AS Assists,
           SUM(sf.Yellow_Cards) AS Yellow_Cards, SUM(sf.Red_Cards) AS Red_Cards,
           COUNT(DISTINCT sf.Match_ID) AS Matches
    FROM Scorecard_Football sf JOIN Players p ON sf.Player_ID=p.Player_ID
    JOIN Teams t ON p.Team_ID=t.Team_ID
    GROUP BY sf.Player_ID HAVING Goals>0 ORDER BY Goals DESC, Assists DESC LIMIT 15
""", fetch=True)
if gb:
    df=pd.DataFrame(gb); df.insert(0,"Rank",range(1,len(df)+1))
    medals={1:"🥇",2:"🥈",3:"🥉"}
    df["Rank"]=df["Rank"].map(lambda r: f"{medals.get(r,str(r))} {r}" if r<=3 else str(r))
    df=df.rename(columns={"Goals":"⚽ Goals","Assists":"🎯 Assists",
                           "Yellow_Cards":"🟨 Yellow","Red_Cards":"🟥 Red","Matches":"Matches"})
    st.dataframe(df, use_container_width=True, hide_index=True)

    # bar chart
    df2 = pd.DataFrame(gb)
    fig = px.bar(df2.head(10), x="Player", y=["Goals","Assists"],
                 barmode="group",
                 color_discrete_sequence=["#22c55e","#5b52f5"],
                 title="Goals & Assists — Top 10")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                      font_color="#e8ecf4",margin=dict(t=36,b=0,l=0,r=0),
                      xaxis=dict(gridcolor="#1e2d45"),yaxis=dict(gridcolor="#1e2d45"))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No goals recorded yet.")

st.divider()

# ── SUSPENSION TRACKER ─────────────────────────────────────────
st.subheader("🚫 Suspension Tracker")
st.markdown("""
<div style="padding:10px 16px;border-radius:8px;border-left:3px solid #f97316;
background:rgba(249,115,22,.07);font-size:13px;margin-bottom:16px">
Powered by <code>trg_suspend_player</code> — auto-suspends when yellow card total ≥ 3.
</div>""", unsafe_allow_html=True)
susp = run_query("""
    SELECT p.Player_Name AS Player, t.Team_Name AS Team, t.University,
           p.Jersey_No AS Jersey,
           SUM(sf.Yellow_Cards) AS Total_Yellows, SUM(sf.Red_Cards) AS Total_Reds
    FROM Players p JOIN Teams t ON p.Team_ID=t.Team_ID
    JOIN Scorecard_Football sf ON sf.Player_ID=p.Player_ID
    WHERE p.Role='SUSPENDED'
    GROUP BY p.Player_ID ORDER BY t.Team_Name
""", fetch=True)
if susp:
    st.dataframe(pd.DataFrame(susp).rename(columns={"Total_Yellows":"🟨 Yellows","Total_Reds":"🟥 Reds","Jersey":"Jersey #"}),
                 use_container_width=True, hide_index=True)
else:
    st.success("✅ No players currently suspended.")

st.divider()

# ── FULL STATS TABLE ──────────────────────────────────────────
with st.expander("📋 All Football Stats"):
    all_stats = run_query("""
        SELECT p.Player_Name,t.Team_Name,SUM(sf.Goals) AS Goals,SUM(sf.Assists) AS Assists,
               SUM(sf.Yellow_Cards) AS Yellows,SUM(sf.Red_Cards) AS Reds,
               COUNT(DISTINCT sf.Match_ID) AS Matches
        FROM Scorecard_Football sf JOIN Players p ON sf.Player_ID=p.Player_ID
        JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sf.Player_ID ORDER BY Goals DESC
    """)
    if all_stats: st.dataframe(pd.DataFrame(all_stats),use_container_width=True,hide_index=True)
    else:         st.info("No data yet.")