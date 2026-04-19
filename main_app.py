"""
main_app.py — ARENA SNU v7
SURGE 2025 · Cricket · Football · Basketball
System Architect: Mudit
"""
import streamlit as st
import importlib.util
import os
import base64
import pandas as pd
from db_connection import run_query

# ─────────────────────────────
# CONFIG
# ─────────────────────────────
st.set_page_config(
    page_title="ARENA SNU · SURGE 2025",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────
# BASE64 IMAGE LOADER
# ─────────────────────────────
def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

football   = get_base64("football.jpg")
cricket    = get_base64("cricket.jpg")
basketball = get_base64("basketball.jpg")
login_bg   = get_base64("login.jpg")

# ─────────────────────────────
# SESSION STATE
# ─────────────────────────────
for key, val in [
    ("app_state",   "landing"),
    ("logged_in",   False),
    ("username",    "Guest"),
    ("role",        "viewer"),
    ("_show_login", False),
]:
    if key not in st.session_state:
        st.session_state[key] = val

# ─────────────────────────────
# GLOBAL CSS
# ─────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@700;800&family=DM+Sans:wght@400;500&display=swap');

.stApp { background:#080c14; color:white; }

footer, #MainMenu { visibility:hidden; }

/* Button styling */
div.stButton > button {
    background: rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.3);
    color:white;
    border-radius:40px;
    padding:14px 40px;
    font-weight:600;
    letter-spacing:2px;
    transition: all 0.25s ease;
}

div.stButton > button:hover {
    background: rgba(255,255,255,0.15);
    border-color:white;
    transform: translateY(-2px);
    box-shadow:0 8px 30px rgba(255,255,255,0.2);
}
</style>
""", unsafe_allow_html=True)

UNIFIED_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
/* Base */ html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background: #080c14 !important; font-family: 'DM Sans', sans-serif; color: #b0bac8; } [data-testid="stSidebar"] { background: rgba(8,12,20,0.95) !important; border-right: 1px solid rgba(255,255,255,0.06); } [data-testid="stHeader"] { background: transparent !important; } section[data-testid="stMain"] > div { background: transparent !important; } p, label, div { color: #b0bac8; font-family: 'DM Sans', sans-serif; }
/* Dividers */ hr { border: none; border-top: 1px solid rgba(255,255,255,0.07) !important; margin: 2rem 0 !important; }
/* Buttons */ div.stButton > button { background: transparent !important; color: #fff !important; font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; font-size: 0.875rem !important; border-radius: 40px !important; border: 1px solid rgba(255,255,255,0.3) !important; padding: 0.55rem 1.6rem !important; letter-spacing: 0.03em !important; transition: all 0.25s ease !important; backdrop-filter: blur(8px) !important; } div.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 32px rgba(168,85,247,0.25) !important; border-color: rgba(168,85,247,0.5) !important; } div.stButton > button[kind="primary"], div.stFormSubmitButton > button { background: linear-gradient(135deg, rgba(168,85,247,0.6), rgba(91,82,245,0.5)) !important; color: #fff !important; font-weight: 700 !important; border-radius: 50px !important; border: 1px solid rgba(168,85,247,0.4) !important; padding: 12px 32px !important; font-family: 'Rajdhani', sans-serif !important; font-size: 1rem !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; transition: all 0.3s ease !important; width: 100% !important; } div.stButton > button[kind="primary"]:hover, div.stFormSubmitButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 12px 40px rgba(168,85,247,0.5) !important; }
/* Inputs */ div[data-baseweb="select"] > div, div[data-baseweb="input"] > div input, div[data-testid="stNumberInput"] input, [data-testid="stTimeInput"] input, [data-testid="stDateInput"] input { background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 10px !important; color: #e8ecf4 !important; font-family: 'DM Sans', sans-serif !important; } div[data-baseweb="select"] svg { color: #7a8499 !important; } div[data-baseweb="popover"] { background: #0f1623 !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 12px !important; } div[data-baseweb="menu"] { background: #0f1623 !important; } div[data-baseweb="menu"] li { color: #b0bac8 !important; } div[data-baseweb="menu"] li:hover { background: rgba(255,255,255,0.07) !important; } label[data-testid="stWidgetLabel"] p, div[data-testid="stSelectbox"] label p { color: rgba(255,255,255,0.4) !important; font-size: 0.7rem !important; letter-spacing: 4px !important; text-transform: uppercase !important; font-family: 'DM Sans', sans-serif !important; font-weight: 500 !important; margin-bottom: 6px !important; }
/* Number inputs */ div[data-testid="stNumberInput"] button { background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(255,255,255,0.1) !important; color: #b0bac8 !important; border-radius: 6px !important; }
/* Form & Containers */ div[data-testid="stForm"] { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 20px !important; padding: 1.5rem !important; } div[data-testid="stDataFrame"] { background: rgba(255,255,255,0.03) !important; border-radius: 16px !important; overflow: hidden !important; border: 1px solid rgba(255,255,255,0.08) !important; } iframe[data-testid="stDataFrameResizable"] { background: transparent !important; } div[data-testid="stAlert"] { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 12px !important; color: #b0bac8 !important; font-family: 'DM Sans', sans-serif !important; } details summary { color: #b0bac8 !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.875rem !important; } details { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 14px !important; padding: 0.25rem 1rem !important; } div[data-testid="stSpinner"] p { color: #7a8499 !important; } div[data-testid="stToast"] { background: rgba(15,22,35,0.95) !important; border: 1px solid rgba(34,197,94,0.3) !important; border-radius: 14px !important; color: #e8ecf4 !important; backdrop-filter: blur(18px) !important; } .js-plotly-plot .plotly { background: transparent !important; }
/* Tabs */ [data-testid="stTabs"] [data-baseweb="tab-list"] { background: rgba(255,255,255,0.03); border-radius: 50px; padding: 4px; border: 1px solid rgba(255,255,255,0.08); gap: 4px; } [data-testid="stTabs"] [data-baseweb="tab"] { background: transparent; border-radius: 50px; color: rgba(255,255,255,0.45); font-family: 'DM Sans', sans-serif; font-weight: 500; font-size: 0.875rem; padding: 8px 20px; border: none; transition: all 0.25s; } [data-testid="stTabs"] [aria-selected="true"] { background: rgba(255,255,255,0.1) !important; color: #fff !important; border: 1px solid rgba(255,255,255,0.2) !important; } [data-testid="stTabs"] [data-baseweb="tab-highlight"], [data-testid="stTabs"] [data-baseweb="tab-border"] { background: transparent !important; }
/* Metrics */ div[data-testid="stMetric"] { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 16px !important; padding: 20px 22px !important; backdrop-filter: blur(18px) !important; } div[data-testid="stMetric"] label { color: rgba(255,255,255,0.35) !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.65rem !important; letter-spacing: 4px !important; text-transform: uppercase !important; } div[data-testid="stMetricValue"] { font-family: 'Rajdhani', sans-serif !important; font-size: 2rem !important; font-weight: 700 !important; color: #e8ecf4 !important; } div[data-testid="stMetricDelta"] { display: none !important; } footer { visibility: hidden; }
</style>
"""

# ─────────────────────────────
# PAGE REGISTRY
# ─────────────────────────────
PUBLIC_PAGES = ["🏠 Home Dashboard", "🏏 Cricket", "⚽ Football", "🏀 Basketball", "⚔️ Compare Players", "📈 Predictions"]

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
    "organiser": ["🏠 Home Dashboard", "📅 Schedule Match", "🏏 Cricket", "⚽ Football", "🏀 Basketball"],
    "manager":   ["🏠 Home Dashboard", "🏏 Cricket", "⚽ Football", "🏀 Basketball", "⚔️ Compare Players", "📈 Predictions"],
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
    "🏀 Basketball":     "Amitoj",
    "🏏 Cricket":        "Ashank",
}

ROLE_PILL = {
    "admin":     ("#a855f7", "ADMIN"),
    "organiser": ("#f97316", "ORGANISER"),
    "manager":   ("#3b82f6", "MANAGER"),
    "viewer":    ("#22c55e", "VIEWER"),
}

# ─────────────────────────────
# LANDING PAGE
# ─────────────────────────────
def landing_page():

    st.markdown(f"""
    <style>
    .block-container {{
        padding:0 !important;
        max-width:100% !important;
    }}

    /* ── THREE-PANEL BACKGROUND ── */
    .bg {{
        position:fixed;
        top:0; left:0;
        width:100%; height:100%;
        display:flex;
        z-index:0;
    }}

    .col {{
        flex:1;
        background-size:cover;
        background-position:center;
        position:relative;
    }}

    .f {{ background-image:url("data:image/jpeg;base64,{football}"); }}
    .c {{ background-image:url("data:image/jpeg;base64,{cricket}"); }}
    .b {{ background-image:url("data:image/jpeg;base64,{basketball}"); }}

    /* Per-panel darkening */
    .f::after {{
        content:'';
        position:absolute; inset:0;
        background: linear-gradient(to right,
            rgba(5,8,18,0.80) 0%,
            rgba(5,8,18,0.45) 70%,
            rgba(5,8,18,0.10) 100%
        );
    }}
    .c::after {{
        content:'';
        position:absolute; inset:0;
        background: radial-gradient(ellipse 80% 60% at 50% 50%,
            rgba(5,8,18,0.28) 0%,
            rgba(5,8,18,0.55) 100%
        );
    }}
    .b::after {{
        content:'';
        position:absolute; inset:0;
        background: linear-gradient(to left,
            rgba(5,8,18,0.80) 0%,
            rgba(5,8,18,0.45) 70%,
            rgba(5,8,18,0.10) 100%
        );
    }}

    /* Thin gradient seams between panels */
    .seam {{
        position:fixed;
        top:0;
        width:80px;
        height:100%;
        background: linear-gradient(to right, rgba(5,8,18,0.5), transparent);
        z-index:1;
        pointer-events:none;
    }}
    .seam-left  {{ left:33.33%; transform:translateX(-50%); }}
    .seam-right {{ left:66.66%; transform:translateX(-50%) scaleX(-1); }}

    /* Sport labels on outer panels */
    .sport-label {{
        position:fixed;
        bottom:15vh;
        font-family:'Rajdhani',sans-serif;
        font-size:0.72rem;
        letter-spacing:5px;
        color:rgba(255,255,255,0.35);
        text-transform:uppercase;
        z-index:2;
        pointer-events:none;
    }}
    .sl-left  {{ left:10vw; }}
    .sl-right {{ right:9vw; }}

    /* ── CENTER CONTENT ── */
    .center {{
        position:relative;
        z-index:3;
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
        height:100vh;
        text-align:center;
        padding:0 1rem;
    }}

    .eyebrow {{
        font-size:0.72rem;
        letter-spacing:6px;
        color:rgba(255,255,255,0.45);
        text-transform:uppercase;
        margin-bottom:1.2rem;
    }}

    .title {{
        font-family:'Rajdhani',sans-serif;
        font-size:clamp(5rem, 11vw, 11rem);
        font-weight:800;
        letter-spacing:22px;
        margin:0;
        line-height:1;
        text-shadow: 0 4px 40px rgba(0,0,0,0.6);
    }}

    .quote {{
        margin-top:18px;
        font-size:1.0rem;
        color:rgba(255,255,255,0.55);
        letter-spacing:1px;
        font-style:italic;
    }}

    /* Button wrapper — z-index above overlay */
    .btn-wrap {{
        position:relative;
        z-index:10;
        margin-top:40px;
    }}

    /* Override Streamlit button for landing */
    .btn-wrap div.stButton > button {{
        background: rgba(255,255,255,0.08) !important;
        border: 1.5px solid rgba(255,255,255,0.65) !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 16px 52px !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        letter-spacing: 4px !important;
        transition: all 0.25s ease !important;
        backdrop-filter: blur(8px) !important;
    }}

    .btn-wrap div.stButton > button:hover {{
        background: rgba(255,255,255,0.18) !important;
        border-color: white !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 36px rgba(255,255,255,0.18) !important;
    }}

    </style>

    <div class="bg">
        <div class="col f"></div>
        <div class="col c"></div>
        <div class="col b"></div>
    </div>
    <div class="seam seam-left"></div>
    <div class="seam seam-right"></div>
    <div class="sport-label sl-left">⚽ Football</div>
    <div class="sport-label sl-right">🏀 Basketball</div>

    <div class="center">
        <div class="eyebrow">SURGE 2025 · SNU</div>
        <div class="title">ARENA</div>
        <div class="quote">"Champions keep playing until they get it right."</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="btn-wrap">', unsafe_allow_html=True)
    _, col, _ = st.columns([3, 2, 3])
    with col:
        if st.button("ENTER THE ARENA", use_container_width=True):
            st.session_state.app_state = "login"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────
# LOGIN PAGE
# ─────────────────────────────
def login_page():

    st.markdown(f"""
    <style>
    .block-container {{
        padding: 2rem 2rem 2rem 2rem !important;
        max-width: 100% !important;
    }}

    /* BACKGROUND */
    .login-bg {{
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        background-image: url("data:image/jpeg;base64,{login_bg}");
        background-size: cover;
        background-position: center;
        z-index: 0;
    }}
    .login-bg::after {{
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(
            to right,
            rgba(5,8,18,0.90) 0%,
            rgba(5,8,18,0.78) 50%,
            rgba(5,8,18,0.85) 100%
        );
    }}

    /* ── LEFT PANEL ── */
    .lp-left {{
        padding: 3rem 3rem 3rem 2rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 90vh;
    }}

    .lp-eyebrow {{
        font-size: 0.78rem;
        letter-spacing: 4px;
        color: #a0a8c0;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }}

    .lp-title {{
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(3rem, 5.5vw, 5.5rem);
        font-weight: 800;
        line-height: 1.0;
        color: #ffffff;
        margin: 0;
    }}

    .lp-title span {{
        color: transparent;
        -webkit-text-stroke: 1.5px rgba(255,255,255,0.45);
    }}

    .lp-divider {{
        width: 56px;
        height: 3px;
        background: linear-gradient(90deg,#ffffff,transparent);
        margin: 1.6rem 0;
        border-radius: 2px;
    }}

    .lp-desc {{
        font-size: 1.05rem;
        color: #b0bac8;
        line-height: 1.7;
        max-width: 460px;
    }}

    .lp-stats {{
        display: flex;
        gap: 2.5rem;
        margin-top: 2.8rem;
    }}

    .lp-stat {{
        display: flex;
        flex-direction: column;
    }}

    .lp-stat-num {{
        font-family: 'Rajdhani', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: #fff;
        line-height: 1;
    }}

    .lp-stat-label {{
        font-size: 0.72rem;
        letter-spacing: 2px;
        color: #7a8499;
        text-transform: uppercase;
        margin-top: 4px;
    }}

    .lp-sports {{
        display: flex;
        gap: 0.6rem;
        margin-top: 2.4rem;
        flex-wrap: wrap;
    }}

    .lp-badge {{
        padding: 5px 14px;
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 20px;
        font-size: 0.78rem;
        color: #c0c8d8;
        letter-spacing: 1px;
        background: rgba(255,255,255,0.05);
    }}

    /* ── RIGHT PANEL — style the Streamlit column as the card ── */
    [data-testid="column"]:nth-child(2) > div > div[data-testid="stVerticalBlock"] {{
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 20px;
        padding: 2.2rem 1.8rem !important;
        margin-top: 7.5rem;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
    }}

    .lp-card-title {{
        font-family: 'Rajdhani', sans-serif;
        font-size: 2.6rem;
        font-weight: 800;
        color: #fff;
        margin-bottom: 0.2rem;
        line-height: 1;
    }}

    .lp-card-sub {{
        font-size: 0.85rem;
        color: #7a8499;
        margin-bottom: 1.8rem;
    }}

    /* Input overrides */
    .stTextInput label {{
        font-size: 0.82rem !important;
        letter-spacing: 1px !important;
        color: #8a94a6 !important;
        text-transform: uppercase !important;
    }}

    .stTextInput input {{
        background: rgba(255,255,255,0.07) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
    }}

    .stTextInput input:focus {{
        border-color: rgba(255,255,255,0.5) !important;
        background: rgba(255,255,255,0.10) !important;
    }}

    </style>

    <div class="login-bg"></div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([6, 4], gap="large")

    # ── LEFT: Branding & Info ──
    with col_left:
        st.markdown("""
        <div class="lp-left">
            <div class="lp-eyebrow">ARENA SNU · SURGE 2025</div>
            <div class="lp-title">Welcome<br>Back to the<br><span>Arena.</span></div>
            <div class="lp-divider"></div>
            <div class="lp-desc">
                Your central hub for live scores, player analytics, match schedules,
                and performance predictions across all sports at SNU.
            </div>
            <div class="lp-stats">
                <div class="lp-stat">
                    <div class="lp-stat-num">3+</div>
                    <div class="lp-stat-label">Sports</div>
                </div>
                <div class="lp-stat">
                    <div class="lp-stat-num">Live</div>
                    <div class="lp-stat-label">Scores</div>
                </div>
                <div class="lp-stat">
                    <div class="lp-stat-num">AI</div>
                    <div class="lp-stat-label">Predictions</div>
                </div>
            </div>
            <div class="lp-sports">
                <span class="lp-badge">🏏 Cricket</span>
                <span class="lp-badge">⚽ Football</span>
                <span class="lp-badge">🏀 Basketball</span>
                <span class="lp-badge">⚔️ Compare Players</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── RIGHT: Login Card ──
    with col_right:
        st.markdown("""
        <div class="lp-card-title">Login</div>
        <div class="lp-card-sub">Enter your credentials to continue</div>
        """, unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Your username")
        password = st.text_input("Password", type="password", placeholder="••••••••")

        st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)

        if st.button("LOGIN", use_container_width=True):
            result = run_query(
                "SELECT * FROM Users WHERE Username=%s AND Password=%s",
                (username, password),
                fetch=True
            )
            if result:
                u = result[0]
                st.session_state.logged_in   = True
                st.session_state.username    = u["Username"]
                st.session_state.role        = u["Role"]
                st.session_state.app_state   = "app"
                st.session_state._show_login = False
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")

        st.markdown(
            "<div style='margin-top:12px; border-top:1px solid rgba(255,255,255,0.08); padding-top:12px'></div>",
            unsafe_allow_html=True,
        )

        if st.button("← Back to Homepage", key="back_btn", use_container_width=True):
            st.session_state.app_state = "landing"
            st.rerun()


# ─────────────────────────────
# SIDEBAR
# ─────────────────────────────
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
            📅 <strong style="color:#facc15">{n}</strong> match{'es' if n != 1 else ''} scheduled
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
        🏆 <strong style="color:#f5a623">{fn}</strong> Final{'s' if fn != 1 else ''} upcoming!
        </div>""", unsafe_allow_html=True)

    # Auth button
    if st.session_state.logged_in:
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            for k, v in [("logged_in", False), ("username", "Guest"),
                         ("role", "viewer"), ("_show_login", False),
                         ("app_state", "landing")]:
                st.session_state[k] = v
            st.rerun()
    else:
        if st.sidebar.button("🔑 Login", use_container_width=True, type="primary"):
            st.session_state.app_state   = "login"
            st.session_state._show_login = True
            st.rerun()

    st.sidebar.markdown("""
    <div style="padding:12px 4px 4px;font-size:11px;color:#2a3a52;
    text-align:center;border-top:1px solid #1a2235;margin-top:8px">
    ARENA SNU v7 · SURGE 2025<br>Shiv Nadar University
    </div>""", unsafe_allow_html=True)

    return selected


# ─────────────────────────────
# ADMIN PANEL
# ─────────────────────────────
def admin_panel():
    import time
    st.markdown(UNIFIED_CSS, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding: 2.5rem 0 1rem; position: relative;">
        <div style="display: inline-block; background: rgba(168,85,247,0.1); border: 1px solid rgba(168,85,247,0.22);
            border-radius: 20px; padding: 4px 14px; margin-bottom: 18px;">
            <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
                color:rgba(255,255,255,0.45); text-transform:uppercase; font-weight:500;">
                SYSTEM MANAGEMENT
            </span>
        </div>
        <h1 style="font-family:'Rajdhani',sans-serif; font-size:3rem; font-weight:800; margin:0;
            line-height:1.0; color:#fff; letter-spacing:-0.01em;">
            🔐 Admin <span style="background:linear-gradient(90deg,#a855f7,#5b52f5);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Panel</span>
        </h1>
        <div style="width:52px; height:3px; background:linear-gradient(90deg,#a855f7,transparent);
            border-radius:2px; margin:14px 0 12px 0;"></div>
        <p style="font-family:'DM Sans',sans-serif; color:#7a8499; font-size:0.95rem;
            margin:0; line-height:1.7;">
            User management · Audit trail · Database statistics
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    tab_users, tab_add, tab_audit, tab_stats = st.tabs(
        ["👥 Users", "➕ Add User", "📋 Audit Log", "📊 DB Stats"]
    )

    with tab_users:
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        rows = run_query(
            "SELECT Username, Role, Created_At FROM Users ORDER BY Role, Username",
            fetch=True,
        )
        if rows:
            df = pd.DataFrame(rows)
            icons = {"admin": "🔴", "organiser": "🟠", "manager": "🔵", "viewer": "🟢"}
            df["Role"] = df["Role"].map(lambda r: f"{icons.get(r, '')} {r}")
            st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption("Passwords hidden for security.")

    with tab_add:
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="margin-bottom:12px;">
            <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:4px;
                color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                Create New User
            </span>
        </div>
        """, unsafe_allow_html=True)
        with st.form("add_user_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                new_user = st.text_input("👤 Username")
                new_role = st.selectbox("🎭 Role", ["organiser", "manager"])
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
        st.markdown("""
        <div style="margin-bottom:12px;">
            <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:4px;
                color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                Delete User
            </span>
        </div>
        """, unsafe_allow_html=True)
        del_rows = run_query(
            "SELECT Username, Role FROM Users WHERE Role NOT IN ('admin') ORDER BY Role, Username",
            fetch=True,
        )
        if del_rows:
            del_map = {f"{u['Username']} ({u['Role']})": u["Username"] for u in del_rows}
            choice  = st.selectbox("Select user to delete", list(del_map.keys()))
            if st.button("🗑️ Delete User"):
                run_query("DELETE FROM Users WHERE Username=%s", (del_map[choice],), fetch=False)
                st.success(f"✅ **{del_map[choice]}** deleted.")
                st.rerun()

    with tab_audit:
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        st.caption("Every INSERT/UPDATE to Teams and Matches is auto-recorded by DB triggers.")
        audit = run_query("SELECT * FROM Audit_Log ORDER BY Changed_At DESC LIMIT 100", fetch=True)
        if audit:
            df_audit = pd.DataFrame(audit)
            st.dataframe(df_audit, use_container_width=True, hide_index=True)

            st.divider()
            csv = df_audit.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Audit Log as CSV",
                data=csv,
                file_name="arena_audit_log.csv",
                mime="text/csv",
                type="primary",
            )
        else:
            st.info("No audit entries yet.")

    with tab_stats:
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="margin-bottom:20px;">
            <span style="font-family:'DM Sans',sans-serif; font-size:0.72rem; letter-spacing:5px;
                color:rgba(255,255,255,0.35); text-transform:uppercase; font-weight:500;">
                DATABASE HEALTH
            </span>
            <h3 style="font-family:'Rajdhani',sans-serif; font-size:1.6rem; font-weight:700;
                color:#fff; margin:6px 0 0 0; line-height:1.1;">
                📊 Global Statistics
            </h3>
            <div style="width:48px; height:3px; background:linear-gradient(90deg,#a855f7,transparent);
                border-radius:2px; margin-top:10px;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        qs = [
            ("Teams",         "SELECT COUNT(*) AS n FROM Teams"),
            ("Players",       "SELECT COUNT(*) AS n FROM Players"),
            ("Matches",       "SELECT COUNT(*) AS n FROM Matches"),
            ("Completed",     "SELECT COUNT(*) AS n FROM Matches WHERE Status='Completed'"),
            ("Cricket Rows",  "SELECT COUNT(*) AS n FROM Scorecard_Cricket"),
            ("Football Rows", "SELECT COUNT(*) AS n FROM Scorecard_Football"),
        ]
        cols = st.columns(len(qs))
        for col, (lbl, q) in zip(cols, qs):
            res = run_query(q)
            col.metric(lbl, res[0]["n"] if res else 0)

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


# ─────────────────────────────
# ROUTING
# ─────────────────────────────
if st.session_state.app_state == "landing":
    landing_page()

elif st.session_state.app_state == "login":
    login_page()

elif st.session_state.app_state == "app" and st.session_state.logged_in:

    role  = st.session_state.role
    pages = {k: ALL_PAGES[k] for k in ROLE_ACCESS.get(role, PUBLIC_PAGES) if k in ALL_PAGES}

    selected = build_sidebar(role, pages)

    # ── RENDER PAGE ──
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