# main_app.py — ARENA SNU Navigation Hub (v2)
# Run: streamlit run main_app.py
import streamlit as st
import importlib.util
import os

try:
    st.set_page_config(page_title="ARENA SNU", page_icon="🏆", layout="wide")
except Exception:
    pass

pages = {
    "🏠 Home Dashboard":      "home_page.py",
    "📅 Schedule Match":      "page_schedule.py",
    "🏏 Cricket Scores":      "page_cricket.py",
    "⚽ Football Scores":     "page_football.py",
    "🏀 Basketball / Admin":  "page_login.py",
    "⚔️ Player Comparison":   "page_comparison.py",
    "📈 Predictions":         "prediction.py",
}

# Owners for pages not yet built
OWNERS = {
    "📅 Schedule Match":     "Disha",
    "⚽ Football Scores":    "Ayush",
    "🏀 Basketball / Admin": "Amitog",
}

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.markdown("""
<div style="padding:16px 0 8px">
  <h2 style="background:linear-gradient(90deg,#6c63ff,#a855f7);
     -webkit-background-clip:text;-webkit-text-fill-color:transparent;
     font-size:1.5rem;font-weight:800;margin:0">🏆 ARENA SNU</h2>
  <p style="color:#6b7a99;font-size:.75rem;margin-top:2px">SURGE Sports Festival</p>
</div>
""", unsafe_allow_html=True)
st.sidebar.divider()

for label, fname in pages.items():
    status = "✅" if os.path.exists(fname) else "⏳"
    owner  = OWNERS.get(label, "")
    owner_tag = f" *({owner})*" if owner and not os.path.exists(fname) else ""
    st.sidebar.markdown(f"{status} {label}{owner_tag}")

st.sidebar.divider()
selected = st.sidebar.radio("Navigate to:", list(pages.keys()), label_visibility="collapsed")
st.sidebar.divider()
st.sidebar.caption("System Architect: Mudit · SNU DBMS Project")

# ── Page Loader ───────────────────────────────────────────────
fname = pages[selected]
if os.path.exists(fname):
    spec = importlib.util.spec_from_file_location("page", fname)
    mod  = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except SystemExit:
        pass
    except Exception as e:
        st.error(f"❌ Error loading page: {e}")
        st.info("Check the terminal for the full traceback.")
else:
    st.title(selected)
    owner = OWNERS.get(selected, "a teammate")
    st.markdown(f"""
    <div style="padding:20px 24px;border-radius:12px;border-left:4px solid #f59e0b;
    background:rgba(245,158,11,.07);margin-top:16px">
        <strong>⏳ Page not built yet</strong><br>
        <span style="color:#6b7a99;font-size:14px">
        Waiting for <strong>{owner}</strong> to push <code>{fname}</code> to GitHub.<br>
        Once the file is pushed, this page loads automatically — no code changes needed.
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.info("💡 Tip: Use `git pull origin main` to fetch the latest files from your teammates.")