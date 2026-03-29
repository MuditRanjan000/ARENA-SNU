# main_app.py — ARENA SNU Navigation Hub
# Run: streamlit run main_app.py
import streamlit as st
import importlib.util, os

st.set_page_config(page_title="ARENA SNU", page_icon="🏆", layout="wide")

pages = {
    "🏠 Home Dashboard":      "home_page.py",
    "📅 Schedule Match":      "page_schedule.py",
    "🏏 Cricket Scores":      "page_cricket.py",
    "⚽ Football Scores":     "page_football.py",
    "🔐 Login & Admin":       "page_login.py",
    "📈 Predictions":         "prediction.py",
}

st.sidebar.markdown("## 🏆 ARENA SNU")
st.sidebar.markdown("*SURGE Sports Festival*")
st.sidebar.divider()

for label, fname in pages.items():
    status = "✅" if os.path.exists(fname) else "⏳"
    st.sidebar.markdown(f"{status} {label}")

st.sidebar.divider()
selected = st.sidebar.radio("Navigate to:", list(pages.keys()))

fname = pages[selected]
if os.path.exists(fname):
    spec = importlib.util.spec_from_file_location("page", fname)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
else:
    st.title(selected)
    owners = {
        "📅 Schedule Match":"Disha","🏏 Cricket Scores":"Ashank",
        "⚽ Football Scores":"Ayush","🔐 Login & Admin":"Amitog","📈 Predictions":"Mudit"
    }
    st.warning(f"⏳ Page not built yet — waiting for **{owners.get(selected,'teammate')}** to push `{fname}`")
    st.info("Once the file is pushed to GitHub, this page loads automatically.")

st.sidebar.divider()
st.sidebar.caption("System Architect: Mudit")
