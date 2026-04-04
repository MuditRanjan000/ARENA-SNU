import streamlit as st
import importlib.util
import os
from db_connection import run_query

st.set_page_config(page_title="ARENA SNU", page_icon="🏆", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ── LOGIN PAGE ────────────────────────────────────────────────
def login_page():
    # Centre everything
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown("""
        <div style="text-align:center;padding:40px 0 20px">
          <h1 style="background:linear-gradient(90deg,#6c63ff,#a855f7);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;
             font-size:2.8rem;font-weight:800;margin:0">🏆 ARENA SNU</h1>
          <p style="color:#6b7a99;margin-top:8px;font-size:.95rem">
             Athletic Resource &amp; Event Navigation Application<br>
             SURGE Sports Festival · Shiv Nadar University</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#1c2030;border:1px solid #252c3d;border-radius:16px;padding:32px 28px;margin-top:8px">
        """, unsafe_allow_html=True)

        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Login →", use_container_width=True, type="primary"):
            result = run_query("SELECT * FROM Users WHERE Username=%s AND Password=%s",
                               (username, password), fetch=True)
            if result:
                user = result[0]
                st.session_state.logged_in  = True
                st.session_state.username   = user["Username"]
                st.session_state.role       = user["Role"]
                st.rerun()
            else:
                st.error("❌ Invalid username or password. Try again.")

        st.markdown("</div>", unsafe_allow_html=True)

        # Demo credentials hint
        st.markdown("""
        <div style="margin-top:20px;padding:14px 18px;background:#1c2030;border:1px solid #252c3d;
        border-radius:12px;font-size:13px;color:#6b7a99">
        <strong style="color:#e8ecf4">Demo credentials</strong><br><br>
        🔴 <code>admin</code> / <code>arena@admin123</code> — Full access<br>
        🟡 <code>manager1</code> / <code>manage123</code> — Score entry<br>
        🟢 <code>viewer1</code> / <code>view123</code> — Read-only view
        </div>
        """, unsafe_allow_html=True)

if not st.session_state.logged_in:
    login_page()
    st.stop()

role = st.session_state.role

# ── PAGE DEFINITIONS ──────────────────────────────────────────
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
    "admin":   list(ALL_PAGES.keys()),
    "manager": ["🏠 Home Dashboard", "📅 Schedule Match", "🏏 Cricket", "⚽ Football", "🏀 Basketball"],
    "viewer":  ["🏠 Home Dashboard", "⚔️ Compare Players", "📈 Predictions"],
}

pages = {k: ALL_PAGES[k] for k in ROLE_ACCESS[role]}

PAGE_HELP = {
    "🏠 Home Dashboard":  "Live stats, standings, awards, team & player management",
    "📅 Schedule Match":  "Book a new match — checks for venue conflicts automatically",
    "🏏 Cricket":         "Enter T20 scores, view Orange/Purple Cap leaderboards, track form",
    "⚽ Football":        "Enter match stats, view Golden Boot, check suspensions",
    "🏀 Basketball":      "Enter stats, view MVP leaderboard and team charts",
    "⚔️ Compare Players": "Head-to-head radar chart comparison across any two players",
    "📈 Predictions":     "ML linear regression — predict a player's next match score",
    "🔐 Admin Panel":     "Audit log of all DB changes, user management",
}

OWNERS = {
    "📅 Schedule Match": "Disha",
    "⚽ Football":       "Ayush",
    "🏀 Basketball":     "Amitog",
    "🏏 Cricket":        "Ashank",
}

ROLE_COLORS = {"admin": "#a855f7", "manager": "#f97316", "viewer": "#22c55e"}
rc = ROLE_COLORS.get(role, "#6b7a99")

# ── SIDEBAR ───────────────────────────────────────────────────
st.sidebar.markdown(f"""
<div style="padding:14px 12px;background:#1c2030;border-radius:10px;margin-bottom:4px">
  <div style="font-size:1rem;font-weight:700;color:#e8ecf4">👤 {st.session_state.username}</div>
  <div style="margin-top:4px">
    <span style="background:{rc};color:#fff;font-size:11px;font-weight:700;
    padding:2px 10px;border-radius:20px;text-transform:uppercase">{role}</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.markdown("<div style='font-size:11px;color:#6b7a99;font-weight:600;letter-spacing:.08em;margin-bottom:6px'>NAVIGATION</div>", unsafe_allow_html=True)

selected = st.sidebar.radio(
    "nav", list(pages.keys()),
    label_visibility="collapsed",
    format_func=lambda x: x
)

# Show helper text for selected page
help_text = PAGE_HELP.get(selected, "")
if help_text:
    st.sidebar.markdown(f"""
    <div style="padding:8px 12px;background:#1c2030;border-left:3px solid #6c63ff;
    border-radius:0 8px 8px 0;font-size:12px;color:#6b7a99;margin:4px 0 8px 0">
    {help_text}</div>""", unsafe_allow_html=True)

owner = OWNERS.get(selected)
if owner:
    st.sidebar.markdown(f"<div style='font-size:11px;color:#6b7a99;padding:0 4px'>👤 Module by <b style='color:#e8ecf4'>{owner}</b></div>", unsafe_allow_html=True)

st.sidebar.divider()

# Quick stats in sidebar
if role in ("admin", "manager"):
    matches_cnt = run_query("SELECT COUNT(*) AS c FROM Matches WHERE Status='Scheduled'")
    n = matches_cnt[0]["c"] if matches_cnt else 0
    if n > 0:
        st.sidebar.markdown(f"""
        <div style="padding:8px 12px;background:#1c2030;border-radius:8px;font-size:12px;margin-bottom:8px">
          📅 <strong style="color:#facc15">{n}</strong> match{'' if n==1 else 'es'} scheduled
        </div>""", unsafe_allow_html=True)

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.clear()
    st.rerun()

st.sidebar.markdown("""
<div style="padding:8px 4px;font-size:11px;color:#6b7a99;text-align:center;margin-top:8px">
ARENA SNU · SURGE 2025<br>Shiv Nadar University
</div>""", unsafe_allow_html=True)

# ── ADMIN PANEL ───────────────────────────────────────────────
if selected == "🔐 Admin Panel" and role == "admin":
    st.title("🔐 Admin Panel")
    st.markdown("""
    <div style="padding:10px 16px;border-radius:8px;border-left:3px solid #a855f7;
    background:rgba(168,85,247,.07);font-size:13px;margin-bottom:20px">
    This panel is only visible to <strong>admin</strong> users. The Audit Log is auto-filled by
    MySQL triggers — no Python code writes to it.
    </div>""", unsafe_allow_html=True)

    tab_audit, tab_users = st.tabs(["📋 Audit Log", "👥 Users"])

    with tab_audit:
        st.caption("Every INSERT/UPDATE to Teams and Matches is automatically recorded here by DB triggers.")
        audit = run_query("SELECT * FROM Audit_Log ORDER BY Changed_At DESC LIMIT 30", fetch=True)
        if audit:
            st.dataframe(audit, use_container_width=True, hide_index=True)
        else:
            st.info("No audit entries yet. Make a change (add team, update match result) to see it logged.")

    with tab_users:
        users = run_query("SELECT Username, Role, Created_At FROM Users ORDER BY Role", fetch=True)
        if users:
            st.dataframe(users, use_container_width=True, hide_index=True)

# ── LOAD PAGE MODULE ──────────────────────────────────────────
elif pages.get(selected):
    fname = pages[selected]
    if os.path.exists(fname):
        spec = importlib.util.spec_from_file_location("page", fname)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    else:
        st.error(f"❌ File '{fname}' not found. Make sure all .py files are in the same folder as main_app.py")
        st.info("Expected folder structure:\n```\nARENAَSNU/\n├── main_app.py\n├── home_page.py\n├── prediction.py\n├── page_cricket.py\n├── page_football.py\n├── page_basketball.py\n├── page_schedule.py\n├── page_comparison.py\n├── db_connection.py\n└── .env\n```")