"""
main_app.py — ARENA SNU v7
SURGE 2025 · Cricket · Football · Basketball
System Architect: Mudit
"""
import streamlit as st
import importlib.util
import os
from db_connection import run_query

st.set_page_config(
    page_title="ARENA SNU · SURGE 2025",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── GLOBAL CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=DM+Sans:wght@400;500;600&display=swap');

/* ── base ── */
.stApp { background: #080c14; }
.block-container { padding-top: 1.4rem !important; max-width: 1400px; }

/* ── sidebar ── */
section[data-testid="stSidebar"] {
    background: #0a0f1a !important;
    border-right: 1px solid #1a2235;
}

/* ── buttons ── */
div.stButton > button {
    background: linear-gradient(135deg, #5b52f5 0%, #9333ea 100%);
    color: #fff; font-family: 'Rajdhani', sans-serif;
    font-weight: 700; font-size: 15px; letter-spacing: .04em;
    border: none; border-radius: 10px;
    transition: transform .2s ease, box-shadow .2s ease;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(91,82,245,.5);
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #f5a623 0%, #ef4444 100%);
}
div.stButton > button[kind="primary"]:hover {
    box-shadow: 0 8px 28px rgba(245,166,35,.45);
}

/* ── metrics ── */
[data-testid="stMetric"] {
    background: #101726;
    border: 1px solid #1e2d45;
    border-top: 3px solid #5b52f5;
    border-radius: 14px;
    padding: 16px 20px;
}
[data-testid="stMetricLabel"] { color: #6b7a99 !important; font-size: 12px !important; }
[data-testid="stMetricValue"] { color: #e8ecf4 !important; font-weight: 800 !important; }

/* ── tabs ── */
.stTabs [data-baseweb="tab"] {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600; font-size: 15px; letter-spacing: .03em;
}
.stTabs [aria-selected="true"] { color: #7c6cf7 !important; }

/* ── alerts ── */
div[data-testid="stAlert"] { border-radius: 10px; }

/* ── radio nav (sidebar) ── */
.stRadio label {
    padding: 7px 12px;
    border-radius: 8px;
    cursor: pointer;
    transition: background .18s;
    font-family: 'DM Sans', sans-serif;
}
.stRadio label:hover { background: rgba(91,82,245,.1); }

/* ── dataframe ── */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }

/* ── expander ── */
details summary { font-weight: 600; }

footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── SESSION DEFAULTS ──────────────────────────────────────────
for key, val in [("logged_in", False), ("username", "Guest"),
                 ("role", "viewer"), ("_show_login", False)]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── PAGE REGISTRY ─────────────────────────────────────────────
PUBLIC_PAGES = ["🏠 Home Dashboard", "⚔️ Compare Players", "📈 Predictions"]

ALL_PAGES = {
    "🏠 Home Dashboard":  "home_page.py",
    "📅 Schedule Match":  "page_schedule.py",
    "🏏 Cricket":         "page_cricket.py",
    "⚽ Football":        "page_football.py",
    "🏀 Basketball":      "page_basketball.py",
    "⚔️ Compare Players": "page_comparison.py",
    "📈 Predictions":     "prediction.py",
    "🔐 Admin Panel":     None,
}

ROLE_ACCESS = {
    "admin":     list(ALL_PAGES.keys()),
    "organiser": ["🏠 Home Dashboard","🏏 Cricket","⚽ Football","🏀 Basketball"],
    "manager":   ["🏠 Home Dashboard","📅 Schedule Match","⚔️ Compare Players","📈 Predictions"],
    "viewer":    PUBLIC_PAGES,
}

PAGE_HELP = {
    "🏠 Home Dashboard":  "Live standings, awards, team & player management",
    "📅 Schedule Match":  "Book a match — venue conflict prevention built in",
    "🏏 Cricket":         "T20 scores, Orange Cap, Purple Cap, form tracker",
    "⚽ Football":        "Match stats, Golden Boot, suspension tracker",
    "🏀 Basketball":      "Stats entry, MVP leaderboard, team charts",
    "⚔️ Compare Players": "Head-to-head radar chart across any two players",
    "📈 Predictions":     "ML linear regression — predict next match score",
    "🔐 Admin Panel":     "User management, audit trail, DB stats",
}

OWNERS = {
    "📅 Schedule Match": "Disha",
    "⚽ Football":       "Ayush",
    "🏀 Basketball":     "Amitog",
    "🏏 Cricket":        "Ashank",
}

ROLE_PILL = {
    "admin":     ("#a855f7", "ADMIN"),
    "organiser": ("#f97316", "ORGANISER"),
    "manager":   ("#3b82f6", "MANAGER"),
    "viewer":    ("#22c55e", "VIEWER"),
}

# ── LOGIN PAGE ────────────────────────────────────────────────
def login_page():
    _, mid, _ = st.columns([1, 1.05, 1])
    with mid:
        st.markdown("""
        <div style="text-align:center;padding:40px 0 28px">
          <div style="font-size:4.5rem;line-height:1">🏆</div>
          <h1 style="
            background:linear-gradient(100deg,#5b52f5,#a855f7,#f5a623);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            font-family:'Rajdhani',sans-serif;font-size:3rem;font-weight:700;
            margin:10px 0 4px;letter-spacing:-1px">ARENA SNU</h1>
          <p style="color:#4a5568;font-size:.9rem;margin:0">
            Athletic Resource &amp; Event Navigation Application<br>
            <strong style="color:#f5a623">SURGE 2025</strong> · Shiv Nadar University
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""<div style="background:#101726;border:1px solid #1e2d45;
        border-radius:16px;padding:32px 28px">""", unsafe_allow_html=True)

        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Login to ARENA →", use_container_width=True, type="primary"):
            result = run_query(
                "SELECT * FROM Users WHERE Username=%s AND Password=%s",
                (username, password), fetch=True
            )
            if result:
                u = result[0]
                st.session_state.logged_in   = True
                st.session_state.username    = u["Username"]
                st.session_state.role        = u["Role"]
                st.session_state._show_login = False
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top:18px;padding:16px 18px;background:#101726;border:1px solid #1e2d45;
        border-radius:12px;font-size:13px;color:#4a5568">
          <strong style="color:#e8ecf4">Demo credentials</strong><br><br>
          🔴 <code>admin</code> / <code>arena@admin123</code> — Full access<br>
          🟠 <code>organiser1</code> / <code>org@123</code> — Score entry<br>
          🔵 <code>manager1</code> / <code>manage123</code> — Scheduling<br>
          🟢 <code>viewer1</code> / <code>view123</code> — Read-only (no login needed)
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""<div style="text-align:center;font-size:1.7rem;
        letter-spacing:8px;color:#1e2d45;margin-top:22px">🏏 ⚽ 🏀</div>""",
        unsafe_allow_html=True)


# ── SIDEBAR ───────────────────────────────────────────────────
def build_sidebar(role, pages):
    color, label = ROLE_PILL.get(role, ("#22c55e", "VIEWER"))

    # Brand
    st.sidebar.markdown("""
    <div style="padding:18px 4px 10px;text-align:center">
      <div style="font-family:'Rajdhani',sans-serif;font-size:1.7rem;font-weight:700;
        background:linear-gradient(100deg,#5b52f5,#a855f7,#f5a623);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent">
        🏆 ARENA SNU
      </div>
      <div style="font-size:11px;color:#3a4a6a;letter-spacing:.12em;margin-top:2px">
        SURGE 2025 · 3 Sports
      </div>
    </div>
    """, unsafe_allow_html=True)

    # User badge
    if st.session_state.logged_in:
        st.sidebar.markdown(f"""
        <div style="padding:12px 14px;background:#101726;border:1px solid #1e2d45;
        border-radius:10px;margin-bottom:8px">
          <div style="font-weight:700;color:#e8ecf4;font-size:15px">
            👤 {st.session_state.username}
          </div>
          <div style="margin-top:5px">
            <span style="background:{color};color:#fff;font-size:11px;font-weight:700;
            padding:2px 10px;border-radius:20px;letter-spacing:.06em">{label}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
        <div style="padding:12px 14px;background:#101726;border:1px solid #1e2d45;
        border-radius:10px;margin-bottom:8px">
          <div style="color:#3a4a6a;font-size:13px">
            👁️ Guest · <em style="color:#4a5568">public pages only</em>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.sidebar.divider()
    st.sidebar.markdown(
        "<div style='font-size:10px;color:#3a4a6a;font-weight:600;"
        "letter-spacing:.1em;margin-bottom:6px'>NAVIGATION</div>",
        unsafe_allow_html=True,
    )

    selected = st.sidebar.radio("nav", list(pages.keys()), label_visibility="collapsed")

    help_txt = PAGE_HELP.get(selected, "")
    if help_txt:
        st.sidebar.markdown(f"""
        <div style="padding:8px 12px;background:#101726;border-left:3px solid #5b52f5;
        border-radius:0 8px 8px 0;font-size:12px;color:#4a5568;margin:4px 0 8px">
        {help_txt}</div>""", unsafe_allow_html=True)

    owner = OWNERS.get(selected)
    if owner:
        st.sidebar.markdown(
            f"<div style='font-size:11px;color:#3a4a6a;margin-bottom:6px'>"
            f"📌 Module by <b style='color:#e8ecf4'>{owner}</b></div>",
            unsafe_allow_html=True,
        )

    st.sidebar.divider()

    # Counters
    if role in ("admin", "organiser", "manager"):
        row = run_query("SELECT COUNT(*) AS c FROM Matches WHERE Status='Scheduled'")
        n = row[0]["c"] if row else 0
        if n:
            st.sidebar.markdown(f"""
            <div style="padding:8px 12px;background:#101726;border:1px solid #1e2d45;
            border-radius:8px;font-size:12px;margin-bottom:8px">
            📅 <strong style="color:#facc15">{n}</strong> match{'es' if n!=1 else ''} scheduled
            </div>""", unsafe_allow_html=True)

    row2 = run_query(
        "SELECT COUNT(*) AS c FROM Matches WHERE Stage='Final' AND Status='Scheduled'"
    )
    fn = row2[0]["c"] if row2 else 0
    if fn:
        st.sidebar.markdown(f"""
        <div style="padding:8px 12px;background:rgba(245,166,35,.08);
        border:1px solid rgba(245,166,35,.25);border-radius:8px;
        font-size:12px;margin-bottom:8px">
        🏆 <strong style="color:#f5a623">{fn}</strong> Final{'s' if fn!=1 else ''} upcoming!
        </div>""", unsafe_allow_html=True)

    # Auth button
    if st.session_state.logged_in:
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            for k, v in [("logged_in", False), ("username", "Guest"),
                         ("role", "viewer"), ("_show_login", False)]:
                st.session_state[k] = v
            st.rerun()
    else:
        if st.sidebar.button("🔑 Login", use_container_width=True, type="primary"):
            st.session_state._show_login = True
            st.rerun()

    st.sidebar.markdown("""
    <div style="padding:12px 4px 4px;font-size:11px;color:#2a3a52;
    text-align:center;border-top:1px solid #1a2235;margin-top:8px">
    ARENA SNU v7 · SURGE 2025<br>Shiv Nadar University
    </div>""", unsafe_allow_html=True)

    return selected


# ── ADMIN PANEL ───────────────────────────────────────────────
def admin_panel():
    import pandas as pd, time

    st.markdown("""
    <h2 style="background:linear-gradient(90deg,#a855f7,#5b52f5);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    font-family:'Rajdhani',sans-serif;font-size:2rem;font-weight:700;margin:0">
    🔐 Admin Panel</h2>
    <p style="color:#4a5568;font-size:.875rem;margin-top:4px">
    User management · Audit trail · Database statistics</p>
    """, unsafe_allow_html=True)
    st.divider()

    tab_users, tab_add, tab_audit, tab_stats = st.tabs(
        ["👥 Users", "➕ Add User", "📋 Audit Log", "📊 DB Stats"]
    )

    with tab_users:
        rows = run_query(
            "SELECT Username, Role, Created_At FROM Users ORDER BY Role, Username",
            fetch=True,
        )
        if rows:
            df = pd.DataFrame(rows)
            icons = {"admin":"🔴","organiser":"🟠","manager":"🔵","viewer":"🟢"}
            df["Role"] = df["Role"].map(lambda r: f"{icons.get(r,'')} {r}")
            st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption("Passwords hidden for security.")

    with tab_add:
        st.subheader("Create New User")
        with st.form("add_user_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                new_user = st.text_input("👤 Username")
                new_role = st.selectbox("🎭 Role", ["organiser","manager"])
            with c2:
                pw1 = st.text_input("🔑 Password",         type="password")
                pw2 = st.text_input("🔑 Confirm Password", type="password")
            if st.form_submit_button("✅ Create User", use_container_width=True):
                if not new_user or not pw1:
                    st.error("❌ Username and password required.")
                elif pw1 != pw2:
                    st.error("❌ Passwords do not match.")
                elif len(pw1) < 6:
                    st.error("❌ Password must be ≥ 6 characters.")
                else:
                    ex = run_query(
                        "SELECT COUNT(*) AS c FROM Users WHERE Username=%s",
                        (new_user,), fetch=True,
                    )
                    if ex and ex[0]["c"] > 0:
                        st.error(f"❌ Username '{new_user}' already exists.")
                    else:
                        run_query(
                            "INSERT INTO Users (Username,Password,Role) VALUES (%s,%s,%s)",
                            (new_user, pw1, new_role), fetch=False,
                        )
                        st.success(f"✅ **{new_user}** created as **{new_role}**.")
                        st.rerun()

        st.divider()
        st.subheader("Delete User")
        del_rows = run_query(
            "SELECT Username, Role FROM Users WHERE Role NOT IN ('admin') ORDER BY Role, Username",
            fetch=True,
        )
        if del_rows:
            del_map = {f"{u['Username']} ({u['Role']})": u["Username"] for u in del_rows}
            choice  = st.selectbox("Select user to delete", list(del_map.keys()))
            if st.button("🗑️ Delete User", type="secondary"):
                run_query("DELETE FROM Users WHERE Username=%s", (del_map[choice],), fetch=False)
                st.success(f"✅ **{del_map[choice]}** deleted.")
                st.rerun()

    with tab_audit:
        st.caption("Every INSERT/UPDATE to Teams and Matches is auto-recorded by DB triggers.")
        audit = run_query("SELECT * FROM Audit_Log ORDER BY Changed_At DESC LIMIT 100", fetch=True)
        if audit:
            st.dataframe(pd.DataFrame(audit), use_container_width=True, hide_index=True)
        else:
            st.info("No audit entries yet.")

    with tab_stats:
        st.subheader("Database Statistics")
        qs = [
            ("Teams",      "SELECT COUNT(*) AS n FROM Teams"),
            ("Players",    "SELECT COUNT(*) AS n FROM Players"),
            ("Matches",    "SELECT COUNT(*) AS n FROM Matches"),
            ("Completed",  "SELECT COUNT(*) AS n FROM Matches WHERE Status='Completed'"),
            ("Cricket Rows","SELECT COUNT(*) AS n FROM Scorecard_Cricket"),
            ("Football Rows","SELECT COUNT(*) AS n FROM Scorecard_Football"),
        ]
        cols = st.columns(len(qs))
        for col, (label, q) in zip(cols, qs):
            res = run_query(q)
            col.metric(label, res[0]["n"] if res else 0)

        st.divider()
        sport_stats = run_query("""
            SELECT sp.Sport_Name, COUNT(DISTINCT t.Team_ID) AS Teams,
                   COUNT(DISTINCT p.Player_ID) AS Players,
                   COUNT(DISTINCT m.Match_ID)  AS Matches
            FROM Sports sp
            LEFT JOIN Teams   t ON sp.Sport_ID = t.Sport_ID
            LEFT JOIN Players p ON p.Team_ID   = t.Team_ID
            LEFT JOIN Matches  m ON sp.Sport_ID = m.Sport_ID
            GROUP BY sp.Sport_ID
        """)
        if sport_stats:
            st.dataframe(pd.DataFrame(sport_stats), use_container_width=True, hide_index=True)


# ── ROUTING ───────────────────────────────────────────────────
if st.session_state._show_login and not st.session_state.logged_in:
    login_page()
    st.stop()

role  = st.session_state.role
pages = {k: ALL_PAGES[k] for k in ROLE_ACCESS.get(role, PUBLIC_PAGES) if k in ALL_PAGES}
if not st.session_state.logged_in:
    pages = {k: ALL_PAGES[k] for k in PUBLIC_PAGES}

selected = build_sidebar(role, pages)

if st.session_state._show_login and not st.session_state.logged_in:
    login_page()
    st.stop()

# ── RENDER PAGE ───────────────────────────────────────────────
if selected == "🔐 Admin Panel" and role == "admin":
    admin_panel()

elif pages.get(selected):
    fname = pages[selected]
    if os.path.exists(fname):
        spec = importlib.util.spec_from_file_location("page", fname)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    else:
        st.error(f"❌ File '{fname}' not found. Ensure all .py files are in the same folder.")
        st.code("""
ARENA_SNU/
├── main_app.py          ← run this
├── home_page.py
├── page_cricket.py
├── page_football.py
├── page_basketball.py
├── page_schedule.py
├── page_comparison.py
├── prediction.py
├── db_connection.py
└── .env                 ← DB_PASSWORD=yourpassword
        """)