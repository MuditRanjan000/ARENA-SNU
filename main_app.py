import streamlit as st
import importlib.util
import os
from db_connection import run_query

# Configure the main Streamlit page settings
st.set_page_config(page_title="ARENA SNU", page_icon="🏆", layout="wide")

# Initialize session state for user authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.markdown("<h1 style='text-align:center;'>🔐 ARENA SNU Login</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):
            # Verify credentials against the Users table
            query = "SELECT * FROM Users WHERE Username=%s AND Password=%s"
            result = run_query(query, (username, password), fetch=True)

            if result:
                user = result[0]
                st.session_state.logged_in = True
                st.session_state.username = user["Username"]
                st.session_state.role = user["Role"]
                st.rerun() # Refresh app to load role-specific views
            else:
                st.error("Invalid credentials")

# Block access to the rest of the app if not authenticated
if not st.session_state.logged_in:
    login_page()
    st.stop()

role = st.session_state.role

# Define available pages based on user role (Access Control)
if role == "admin":
    pages = {
        "🏠 Home": "home_page.py",
        "📅 Schedule": "page_schedule.py",
        "🏏 Cricket": "page_cricket.py",
        "⚽ Football": "page_football.py",
        "🏀 Basketball": "page_basketball.py",
        "⚔️ Comparison": "page_comparison.py",
        "📈 Predictions": "prediction.py",
        "🔐 Admin Panel": None, # None indicates an internal section rendered below, not an external file
    }
elif role == "manager":
    pages = {
        "🏠 Home": "home_page.py",
        "🏏 Cricket": "page_cricket.py",
        "⚽ Football": "page_football.py",
        "🏀 Basketball": "page_basketball.py",
    }
else: # viewer role
    pages = {
        "🏠 Home": "home_page.py",
        "⚔️ Comparison": "page_comparison.py",
        "📈 Predictions": "prediction.py",
    }

OWNERS = {
    "📅 Schedule": "Disha",
    "⚽ Football": "Ayush",
    "🏀 Basketball": "Amitog",
}

# Build sidebar UI displaying user details
st.sidebar.markdown(f"""
<div style="padding:10px">
<b>👤 {st.session_state.username}</b><br>
<small>Role: {role.capitalize()}</small>
</div>
""", unsafe_allow_html=True)
st.sidebar.divider()

# Render navigation menu and indicate file existence status
for label, fname in pages.items():
    if fname is None:
        st.sidebar.markdown(f"🔐 {label}")
    else:
        status = "✅" if os.path.exists(fname) else "⏳"
        owner = OWNERS.get(label, "")
        owner_tag = f" ({owner})" if owner else ""
        st.sidebar.markdown(f"{status} {label}{owner_tag}")

st.sidebar.divider()
selected = st.sidebar.radio("Navigate", list(pages.keys()), label_visibility="collapsed")
st.sidebar.divider()

if st.sidebar.button("Logout", use_container_width=True):
    st.session_state.clear()
    st.rerun()

# Render internal Admin Panel
if selected == "🔐 Admin Panel" and role == "admin":
    st.title("🔐 Admin Panel")
    
    st.subheader("Audit Log")
    # Fetch recent system changes automatically logged by database triggers
    audit = run_query("SELECT * FROM Audit_Log ORDER BY Changed_At DESC LIMIT 20", fetch=True)
    if audit:
        st.dataframe(audit, use_container_width=True, hide_index=True)
    
    st.subheader("Users")
    users = run_query("SELECT Username, Role FROM Users", fetch=True)
    if users:
        st.dataframe(users, use_container_width=True, hide_index=True)

# Dynamically load and execute selected external Streamlit module
elif pages[selected]:
    fname = pages[selected]
    if os.path.exists(fname):
        spec = importlib.util.spec_from_file_location("page", fname)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    else:
        st.error(f"❌ File '{fname}' not found.")