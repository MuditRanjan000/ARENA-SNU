import streamlit as st
import importlib.util
import os
from db_connection import run_query

# ── CONFIG ─────────────────────────────
st.set_page_config(page_title="ARENA SNU", page_icon="🏆", layout="wide")

# ── SESSION INIT ───────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ── LOGIN FUNCTION ─────────────────────
def login_page():
    st.markdown("<h1 style='text-align:center;'>🔐 ARENA SNU Login</h1>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        query = "SELECT * FROM Users WHERE Username=%s AND Password=%s"
        result = run_query(query, (username, password), fetch=True)

        if result:
            user = result[0]
            st.session_state.logged_in = True
            st.session_state.username = user["Username"]
            st.session_state.role = user["Role"]
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ── LOGIN GATE ─────────────────────────
if not st.session_state.logged_in:
    login_page()
    st.stop()

# ── ROLE BASED ACCESS ──────────────────
role = st.session_state.role

if role == "admin":
    pages = {
        "🏠 Home": "home_page.py",
        "📅 Schedule": "page_schedule.py",
        "🏏 Cricket": "page_cricket.py",
        "⚽ Football": "page_football.py",
        "⚔️ Comparison": "page_comparison.py",
        "📈 Predictions": "prediction.py",
        "🏀 Basketball": "page_basketball.py",
        "🔐 Admin Panel": None,
    }

elif role == "manager":
    pages = {
        "🏠 Home": "home_page.py",
        "🏏 Cricket": "page_cricket.py",
        "⚽ Football": "page_football.py",
        "🏀 Basketball": "page_basketball.py",
    }

else:
    pages = {
        "🏠 Home": "home_page.py",
        "⚔️ Comparison": "page_comparison.py",
        "📈 Predictions": "prediction.py",
    }

# ── OWNER TAGS ─────────────────────────
OWNERS = {
    "📅 Schedule": "Disha",
    "⚽ Football": "Ayush",
    "🏀 Basketball": "Amitog",
}

# ── SIDEBAR UI ─────────────────────────
st.sidebar.markdown(f"""
<div style="padding:10px">
<b>👤 {st.session_state.username}</b><br>
<small>Role: {role}</small>
</div>
""", unsafe_allow_html=True)

st.sidebar.divider()

# Show pages with status + owner
for label, fname in pages.items():
    if fname is None:
        st.sidebar.markdown(f"🔐 {label}")
    else:
        status = "✅" if os.path.exists(fname) else "⏳"
        owner = OWNERS.get(label, "")
        owner_tag = f" ({owner})" if owner else ""
        st.sidebar.markdown(f"{status} {label}{owner_tag}")

st.sidebar.divider()

# Navigation
selected = st.sidebar.radio("Navigate", list(pages.keys()), label_visibility="collapsed")

st.sidebar.divider()

# Logout
if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

# ── ADMIN PANEL ────────────────────────
if selected == "🔐 Admin Panel" and role == "admin":
    st.title("🔐 Admin Panel")

    st.subheader("Audit Log")
    audit = run_query(
        "SELECT * FROM audit_log ORDER BY created_at DESC LIMIT 20",
        fetch=True
    )
    st.write(audit)

    st.subheader("Users")
    users = run_query("SELECT Username, Role FROM Users", fetch=True)
    st.write(users)

# ── PAGE LOADER ────────────────────────
elif pages[selected]:
    fname = pages[selected]

    if os.path.exists(fname):
        spec = importlib.util.spec_from_file_location("page", fname)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        # ✅ ADD THIS LINE ONLY
        if hasattr(mod, "show"):
            mod.show()

    else:
        st.error(f"❌ File '{fname}' not found.")