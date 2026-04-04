"""
main_app.py — ARENA SNU v6
SURGE 2025 Sports Festival · Shiv Nadar University
System Architect: Mudit
All 6 sports · Public viewer access · Role-based routing · SURGE visual theme
"""
import streamlit as st
import importlib.util
import os
from db_connection import run_query

st.set_page_config(page_title="ARENA SNU · SURGE 2025", page_icon="🏆", layout="wide",
                   initial_sidebar_state="expanded")

# ── GLOBAL CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Inter:wght@400;500;600&display=swap');

/* Root palette */
:root {
    --bg:       #0d1117;
    --card:     #161b24;
    --border:   #21262d;
    --accent:   #6c63ff;
    --accent2:  #a855f7;
    --gold:     #f5a623;
    --text:     #e8ecf4;
    --muted:    #6b7a99;
}

/* App background */
.stApp { background: var(--bg); }
section[data-testid="stSidebar"] { background: #0d1117 !important; border-right: 1px solid #21262d; }

/* Remove default Streamlit top padding */
.block-container { padding-top: 1.5rem !important; }

/* Buttons */
div.stButton > button {
    background: linear-gradient(135deg, #6c63ff, #a855f7);
    color: white; font-weight: 700; border-radius: 10px;
    border: none; transition: all 0.25s ease;
    font-family: 'Rajdhani', sans-serif; letter-spacing: 0.05em;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(108,99,255,0.5);
}
div.stButton > button:active { transform: translateY(0); }

/* Primary button */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #f5a623, #ef6820);
}

/* Metrics */
[data-testid="stMetric"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 16px 20px;
    border-top: 3px solid var(--accent);
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 13px !important; }
[data-testid="stMetricValue"] { color: var(--text) !important; font-weight: 700 !important; }

/* Tabs */
.stTabs [data-baseweb="tab"] {
    font-weight: 600;
    font-family: 'Rajdhani', sans-serif;
    letter-spacing: 0.04em;
    font-size: 15px;
}
.stTabs [aria-selected="true"] { color: var(--accent) !important; }

/* Dataframe */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }

/* Sidebar nav radio */
.stRadio > div { gap: 4px; }
.stRadio > div > label {
    padding: 8px 12px;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s;
}
.stRadio > div > label:hover { background: rgba(108,99,255,0.08); }

/* Info / warning / error boxes */
div[data-testid="stAlert"] { border-radius: 10px; }

/* Expander */
details summary { font-weight: 600; }

/* Hide default footer */
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── SESSION DEFAULTS ──────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = "Guest"
if "role" not in st.session_state:
    st.session_state.role = "viewer"

# ── PAGE DEFINITIONS ──────────────────────────────────────────
PUBLIC_PAGES = ["🏠 Home Dashboard", "⚔️ Compare Players", "📈 Predictions"]

ALL_PAGES = {
    "🏠 Home Dashboard":   "home_page.py",
    "📅 Schedule Match":   "page_schedule.py",
    "🏏 Cricket":          "page_cricket.py",
    "⚽ Football":         "page_football.py",
    "🏀 Basketball":       "page_basketball.py",
    "🏸 Badminton":        "page_badminton.py",
    "🏓 Table Tennis":     "page_tabletennis.py",
    "🏐 Volleyball":       "page_volleyball.py",
    "⚔️ Compare Players":  "page_comparison.py",
    "📈 Predictions":      "prediction.py",
    "🔐 Admin Panel":      None,
}

ROLE_ACCESS = {
    "admin":     list(ALL_PAGES.keys()),
    "organiser": ["🏠 Home Dashboard", "🏏 Cricket", "⚽ Football", "🏀 Basketball",
                  "🏸 Badminton", "🏓 Table Tennis", "🏐 Volleyball"],
    "manager":   ["🏠 Home Dashboard", "📅 Schedule Match", "⚔️ Compare Players", "📈 Predictions"],
    "viewer":    PUBLIC_PAGES,
}

PAGE_HELP = {
    "🏠 Home Dashboard":  "Live standings, awards, team & player management",
    "📅 Schedule Match":  "Book a match — venue conflict prevention built in",
    "🏏 Cricket":         "T20 scores, Orange/Purple Cap, player form tracker",
    "⚽ Football":        "Match stats, Golden Boot, suspension tracker",
    "🏀 Basketball":      "Stats, MVP leaderboard, team charts",
    "🏸 Badminton":       "Sets & points, Singles/Doubles leaderboards",
    "🏓 Table Tennis":    "Games & points, Singles/Doubles categories",
    "🏐 Volleyball":      "Kills, Blocks, Aces, Digs tracker",
    "⚔️ Compare Players": "Head-to-head radar chart across any two players",
    "📈 Predictions":     "ML linear regression — predict next match score",
    "🔐 Admin Panel":     "Manage users, view DB audit log",
}

OWNERS = {
    "📅 Schedule Match": "Disha",
    "⚽ Football":       "Ayush",
    "🏀 Basketball":     "Amitog",
    "🏏 Cricket":        "Ashank",
    "🏸 Badminton":      "Team",
    "🏓 Table Tennis":   "Team",
    "🏐 Volleyball":     "Team",
}

ROLE_COLORS = {
    "admin":     "#a855f7",
    "organiser": "#f97316",
    "manager":   "#3b82f6",
    "viewer":    "#22c55e",
}

SPORT_SECTIONS = {
    "🏆 MANAGEMENT":    ["🏠 Home Dashboard", "📅 Schedule Match"],
    "⚽ BALL SPORTS":   ["🏏 Cricket", "⚽ Football", "🏀 Basketball", "🏐 Volleyball"],
    "🏸 RACKET SPORTS": ["🏸 Badminton", "🏓 Table Tennis"],
    "🔬 ANALYTICS":     ["⚔️ Compare Players", "📈 Predictions"],
    "🔐 ADMIN":         ["🔐 Admin Panel"],
}


# ── LOGIN PAGE ────────────────────────────────────────────────
def login_page():
    _, mid, _ = st.columns([1, 1.1, 1])
    with mid:
        st.markdown("""
        <div style="text-align:center;padding:36px 0 24px">
          <div style="font-size:4rem;margin-bottom:8px">🏆</div>
          <h1 style="background:linear-gradient(90deg,#6c63ff,#a855f7,#f5a623);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;
             font-size:2.6rem;font-weight:800;margin:0;font-family:'Rajdhani',sans-serif;letter-spacing:-1px">
             ARENA SNU</h1>
          <p style="color:#6b7a99;margin-top:8px;font-size:.9rem;line-height:1.6">
             Athletic Resource &amp; Event Navigation Application<br>
             <strong style="color:#f5a623">SURGE 2025</strong> · Shiv Nadar University</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""<div style="background:#161b24;border:1px solid #21262d;
        border-radius:16px;padding:32px 28px;margin-top:8px">""", unsafe_allow_html=True)

        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Login to ARENA →", use_container_width=True, type="primary"):
            result = run_query("SELECT * FROM Users WHERE Username=%s AND Password=%s",
                               (username, password), fetch=True)
            if result:
                user = result[0]
                st.session_state.logged_in = True
                st.session_state.username  = user["Username"]
                st.session_state.role      = user["Role"]
                st.session_state._show_login = False
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top:20px;padding:16px 18px;background:#161b24;border:1px solid #21262d;
        border-radius:12px;font-size:13px;color:#6b7a99">
        <strong style="color:#e8ecf4">Demo credentials</strong><br><br>
        🔴 <code>admin</code> / <code>arena@admin123</code> — Full access<br>
        🟠 <code>organiser1</code> / <code>org@123</code> — Score entry (all 6 sports)<br>
        🔵 <code>manager1</code> / <code>manage123</code> — Scheduling &amp; analytics<br>
        🟢 <code>viewer1</code> / <code>view123</code> — Read-only (no login needed)
        </div>
        """, unsafe_allow_html=True)

        # SURGE sports strip
        st.markdown("""
        <div style="margin-top:24px;text-align:center;font-size:1.8rem;letter-spacing:6px;
        color:#6b7a99">🏏 ⚽ 🏀 🏸 🏓 🏐</div>
        <div style="text-align:center;font-size:11px;color:#6b7a99;margin-top:6px">
        6 Sports · 38 Teams · SURGE 2025</div>
        """, unsafe_allow_html=True)


# ── SIDEBAR ───────────────────────────────────────────────────
def build_sidebar(role, pages):
    rc = ROLE_COLORS.get(role, "#6b7a99")

    # Header
    st.sidebar.markdown("""
    <div style="padding:16px 0 8px;text-align:center">
      <div style="font-size:1.6rem;font-weight:800;
        background:linear-gradient(90deg,#6c63ff,#a855f7,#f5a623);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        font-family:'Rajdhani',sans-serif;letter-spacing:-0.5px">🏆 ARENA SNU</div>
      <div style="font-size:11px;color:#6b7a99;margin-top:2px;letter-spacing:0.1em">SURGE 2025</div>
    </div>
    """, unsafe_allow_html=True)

    # User badge
    if st.session_state.logged_in:
        st.sidebar.markdown(f"""
        <div style="padding:12px 14px;background:#161b24;border:1px solid #21262d;
        border-radius:10px;margin-bottom:8px">
          <div style="font-size:15px;font-weight:700;color:#e8ecf4">👤 {st.session_state.username}</div>
          <div style="margin-top:5px">
            <span style="background:{rc};color:#fff;font-size:11px;font-weight:700;
            padding:2px 10px;border-radius:20px;text-transform:uppercase;letter-spacing:0.06em">
            {role}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
        <div style="padding:12px 14px;background:#161b24;border:1px solid #21262d;
        border-radius:10px;margin-bottom:8px">
          <div style="font-size:13px;color:#6b7a99">👁️ Browsing as <strong style="color:#e8ecf4">Guest</strong></div>
          <div style="font-size:11px;color:#6b7a99;margin-top:3px">Public pages visible without login</div>
        </div>
        """, unsafe_allow_html=True)

    st.sidebar.divider()

    # Navigation — flat radio (simpler, more reliable)
    st.sidebar.markdown("<div style='font-size:11px;color:#6b7a99;font-weight:600;letter-spacing:.08em;margin-bottom:6px'>NAVIGATION</div>", unsafe_allow_html=True)
    selected = st.sidebar.radio("nav", list(pages.keys()),
                                label_visibility="collapsed")

    # Page help
    help_text = PAGE_HELP.get(selected, "")
    if help_text:
        st.sidebar.markdown(f"""
        <div style="padding:8px 12px;background:#161b24;border-left:3px solid #6c63ff;
        border-radius:0 8px 8px 0;font-size:12px;color:#6b7a99;margin:4px 0 8px 0">
        {help_text}</div>""", unsafe_allow_html=True)

    owner = OWNERS.get(selected)
    if owner:
        st.sidebar.markdown(f"<div style='font-size:11px;color:#6b7a99;padding:0 4px;margin-bottom:6px'>📌 Module by <b style='color:#e8ecf4'>{owner}</b></div>",
                            unsafe_allow_html=True)

    st.sidebar.divider()

    # Scheduled matches counter
    if role in ("admin", "organiser", "manager"):
        matches_cnt = run_query("SELECT COUNT(*) AS c FROM Matches WHERE Status='Scheduled'")
        n = matches_cnt[0]["c"] if matches_cnt else 0
        if n > 0:
            st.sidebar.markdown(f"""
            <div style="padding:8px 12px;background:#161b24;border-radius:8px;
            font-size:12px;margin-bottom:8px;border:1px solid #21262d">
              📅 <strong style="color:#facc15">{n}</strong> match{'es' if n!=1 else ''} still scheduled
            </div>""", unsafe_allow_html=True)

    # Finals upcoming
    finals_cnt = run_query("SELECT COUNT(*) AS c FROM Matches WHERE Stage='Final' AND Status='Scheduled'")
    fn = finals_cnt[0]["c"] if finals_cnt else 0
    if fn > 0:
        st.sidebar.markdown(f"""
        <div style="padding:8px 12px;background:rgba(245,166,35,.1);border-radius:8px;
        font-size:12px;margin-bottom:8px;border:1px solid rgba(245,166,35,.3)">
          🏆 <strong style="color:#f5a623">{fn}</strong> Final{'s' if fn!=1 else ''} remaining!
        </div>""", unsafe_allow_html=True)

    # Auth button
    if st.session_state.logged_in:
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username  = "Guest"
            st.session_state.role      = "viewer"
            st.session_state._show_login = False
            st.rerun()
    else:
        if st.sidebar.button("🔑 Login", use_container_width=True, type="primary"):
            st.session_state._show_login = True
            st.rerun()

    # Footer
    st.sidebar.markdown("""
    <div style="padding:12px 4px 4px;font-size:11px;color:#6b7a99;text-align:center;
    border-top:1px solid #21262d;margin-top:8px">
    ARENA SNU v6 · SURGE 2025<br>Shiv Nadar University<br>
    <span style="font-size:10px">🏏 ⚽ 🏀 🏸 🏓 🏐</span>
    </div>""", unsafe_allow_html=True)

    return selected


# ── ADMIN PANEL ───────────────────────────────────────────────
def admin_panel():
    st.markdown("""
    <h2 style="background:linear-gradient(90deg,#a855f7,#6c63ff);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    font-size:2rem;font-weight:800;margin:0">🔐 Admin Panel</h2>
    <p style="color:#6b7a99;font-size:.875rem;margin-top:4px">
    User management, audit trail, database monitoring</p>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("""
    <div style="padding:10px 16px;border-radius:8px;border-left:3px solid #a855f7;
    background:rgba(168,85,247,.07);font-size:13px;margin-bottom:20px">
    Visible to <strong>admin</strong> users only. Manage users, view full audit trail of all DB changes.
    </div>""", unsafe_allow_html=True)

    tab_users, tab_add, tab_audit, tab_stats = st.tabs(["👥 Users", "➕ Add User", "📋 Audit Log", "📊 DB Stats"])

    with tab_users:
        users = run_query("SELECT Username, Role, Created_At FROM Users ORDER BY Role, Username", fetch=True)
        if users:
            import pandas as pd
            df = pd.DataFrame(users)
            role_colors = {"admin": "🔴", "organiser": "🟠", "manager": "🔵", "viewer": "🟢"}
            df["Role"] = df["Role"].map(lambda r: f"{role_colors.get(r,'')} {r}")
            st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption("Passwords are hidden for security.")

    with tab_add:
        st.subheader("Create New User")
        st.info("Create **manager** and **organiser** accounts. Admins are created directly in the DB.")

        with st.form("add_user_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                new_username = st.text_input("👤 Username", placeholder="e.g. ayush_organiser")
                new_role     = st.selectbox("🎭 Role", ["organiser", "manager"],
                                            help="Organiser = score entry for all 6 sports | Manager = scheduling")
            with col2:
                new_password  = st.text_input("🔑 Password", type="password")
                new_password2 = st.text_input("🔑 Confirm Password", type="password")

            if st.form_submit_button("✅ Create User", use_container_width=True):
                if not new_username or not new_password:
                    st.error("❌ Username and password are required.")
                elif new_password != new_password2:
                    st.error("❌ Passwords do not match.")
                elif len(new_password) < 6:
                    st.error("❌ Password must be at least 6 characters.")
                else:
                    existing = run_query("SELECT COUNT(*) AS c FROM Users WHERE Username=%s",
                                         (new_username,), fetch=True)
                    if existing and existing[0]["c"] > 0:
                        st.error(f"❌ Username '{new_username}' already exists.")
                    else:
                        run_query("INSERT INTO Users (Username, Password, Role) VALUES (%s, %s, %s)",
                                  (new_username, new_password, new_role), fetch=False)
                        st.success(f"✅ User **{new_username}** created as **{new_role}**.")
                        st.rerun()

        st.divider()
        st.subheader("Delete User")
        st.warning("⚠️ This permanently removes the user's login access.")
        del_users = run_query(
            "SELECT Username, Role FROM Users WHERE Role NOT IN ('admin') ORDER BY Role, Username", fetch=True)
        if del_users:
            del_map = {f"{u['Username']} ({u['Role']})": u['Username'] for u in del_users}
            del_choice = st.selectbox("Select user to delete", list(del_map.keys()))
            if st.button("🗑️ Delete User", type="secondary"):
                run_query("DELETE FROM Users WHERE Username=%s", (del_map[del_choice],), fetch=False)
                st.success(f"✅ User **{del_map[del_choice]}** deleted.")
                st.rerun()

    with tab_audit:
        st.caption("Every INSERT/UPDATE to Teams and Matches is auto-recorded by DB triggers. Zero Python code for logging.")
        audit = run_query("SELECT * FROM Audit_Log ORDER BY Changed_At DESC LIMIT 100", fetch=True)
        if audit:
            import pandas as pd
            st.dataframe(pd.DataFrame(audit), use_container_width=True, hide_index=True)
        else:
            st.info("No audit entries yet. Add teams or schedule matches to see entries.")

    with tab_stats:
        st.subheader("📊 Database Statistics")
        import pandas as pd

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        stats = [
            ("Teams",   "SELECT COUNT(*) AS n FROM Teams"),
            ("Players", "SELECT COUNT(*) AS n FROM Players"),
            ("Matches", "SELECT COUNT(*) AS n FROM Matches"),
            ("Scored",  "SELECT COUNT(*) AS n FROM (SELECT Match_ID FROM Scorecard_Cricket UNION SELECT Match_ID FROM Scorecard_Football UNION SELECT Match_ID FROM Scorecard_Basketball) AS scored"),
            ("Sports",  "SELECT COUNT(*) AS n FROM Sports"),
            ("Venues",  "SELECT COUNT(*) AS n FROM Venues"),
        ]
        for col, (label, q) in zip([col1,col2,col3,col4,col5,col6], stats):
            res = run_query(q)
            col.metric(label, res[0]["n"] if res else 0)

        st.divider()
        teams_by_sport = run_query("""
            SELECT sp.Sport_Name, COUNT(t.Team_ID) AS Teams,
                   COUNT(p.Player_ID) AS Players
            FROM Sports sp
            LEFT JOIN Teams t ON sp.Sport_ID=t.Sport_ID
            LEFT JOIN Players p ON p.Team_ID=t.Team_ID
            GROUP BY sp.Sport_ID
        """)
        if teams_by_sport:
            st.dataframe(pd.DataFrame(teams_by_sport), use_container_width=True, hide_index=True)


# ── MAIN ROUTING ──────────────────────────────────────────────
if st.session_state.get("_show_login") and not st.session_state.logged_in:
    login_page()
    st.stop()

role  = st.session_state.role
pages = {k: ALL_PAGES[k] for k in ROLE_ACCESS.get(role, PUBLIC_PAGES) if k in ALL_PAGES}

if not st.session_state.logged_in:
    pages = {k: ALL_PAGES[k] for k in PUBLIC_PAGES}

selected = build_sidebar(role, pages)

if st.session_state.get("_show_login") and not st.session_state.logged_in:
    login_page()
    st.stop()

# ── RENDER SELECTED PAGE ──────────────────────────────────────
if selected == "🔐 Admin Panel" and role == "admin":
    admin_panel()

elif pages.get(selected):
    fname = pages[selected]
    if os.path.exists(fname):
        spec = importlib.util.spec_from_file_location("page", fname)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    else:
        st.error(f"❌ File '{fname}' not found. Make sure all .py files are in the same folder as main_app.py")
        st.markdown("""
        **Expected file structure:**
        ```
        ARENA_SNU/
        ├── main_app.py
        ├── home_page.py
        ├── prediction.py
        ├── page_cricket.py
        ├── page_football.py
        ├── page_basketball.py
        ├── page_badminton.py       ← NEW in v6
        ├── page_tabletennis.py     ← NEW in v6
        ├── page_volleyball.py      ← NEW in v6
        ├── page_schedule.py
        ├── page_comparison.py
        ├── db_connection.py
        └── .env
        ```
        """)