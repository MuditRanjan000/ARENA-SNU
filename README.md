# 🏆 ARENA SNU — Athletic Resource & Event Navigation Application

> **SURGE 2025** · Shiv Nadar University · Greater Noida  
> DBMS Group Project — Python + Streamlit + MySQL 8.0

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Tech Stack](#-tech-stack)
3. [Team Members](#-team-members)
4. [Database Schema](#-database-schema)
5. [Setup Instructions](#-setup-instructions)
6. [Running the App](#-running-the-app)
7. [Login Credentials](#-login-credentials)
8. [Features](#-features)
9. [Project Structure](#-project-structure)
10. [Git Workflow](#-git-workflow)

---

## 🎯 Project Overview

ARENA SNU is a full-stack database-driven web application built to digitalise **SURGE** — Shiv Nadar University's annual inter-university sports festival. It replaces manual spreadsheet management with a real-time system covering:

- Team registration and player management
- Match scheduling with venue conflict prevention
- Live scorecard entry for Cricket, Football, and Basketball
- Real-time analytics dashboard, points table, and standings
- Machine learning performance predictions (NumPy linear regression)
- Role-based access control for admins, organisers, managers, and viewers
- Automatic audit logging, form tracking, and player suspension via database triggers

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Database | MySQL 8.0 |
| Backend | Python 3.10+ |
| Frontend | Streamlit |
| Charts | Plotly Express + Plotly Graph Objects |
| ML | NumPy (linear regression — no sklearn needed) |
| DB Connector | mysql-connector-python |
| Config | python-dotenv |

---

## 👥 Team Members

| Name | Role | Files |
|---|---|---|
| Mudit | System Architect | `main_app.py`, `home_page.py`, `db_connection.py`, `prediction.py`, `page_comparison.py`, `*.sql` |
| Disha | Match Operations | `page_schedule.py` |
| Ashank | Cricket Lead | `page_cricket.py` |
| Aayush | Football Lead | `page_football.py` |
| Amitoj | Basketball / Admin | `page_basketball.py` |

---

## 🗄 Database Schema

**Database name:** `ARENA_SNU`  
**Tables:** 11 · **Views:** 5 · **Triggers:** 6 · **Procedures:** 4 · **Normal Form:** 3NF

### Tables

| Table | Purpose |
|---|---|
| `Sports` | Cricket, Football, Basketball metadata |
| `Venues` | 5 SNU campus venue records |
| `Teams` | 18 university teams (6 per sport) |
| `Players` | 174 players across all teams |
| `Matches` | All scheduled and completed matches, tracks overall scores |
| `Scorecard_Cricket` | Per-player cricket stats |
| `Scorecard_Football` | Per-player football stats |
| `Scorecard_Basketball` | Per-player basketball stats |
| `Users` | App login accounts with role-based access |
| `Audit_Log` | Auto-populated by triggers only |
| `Predictions` | ML prediction results saved from the UI |

### Views

| View | Description |
|---|---|
| `Upcoming_Schedule` | Full match schedule with sport icon, teams, venue, and winner |
| `Points_Table` | Live standings — wins, losses, points per team |
| `Top_Scorers` | Orange Cap · Golden Boot · MVP across all 3 sports |
| `Audit_View` | All DB changes with timestamps (admin only) |
| `Finals_Overview` | Final-stage matches with champion name |

### Triggers

| Trigger | Event | What it does |
|---|---|---|
| `trg_match_completed` | BEFORE UPDATE on Matches | Auto-sets `Status='Completed'` when a winner is recorded |
| `trg_audit_teams_insert` | AFTER INSERT on Teams | Logs every new team to `Audit_Log` |
| `trg_audit_teams_update` | AFTER UPDATE on Teams | Logs old vs new team values to `Audit_Log` |
| `trg_audit_matches_insert` | AFTER INSERT on Matches | Logs every new match scheduling action |
| `trg_suspend_player` | AFTER INSERT on Scorecard_Football | Sets `Role='SUSPENDED'` if cumulative yellow cards ≥ 3 |
| `trg_player_form` | AFTER INSERT on Scorecard_Cricket | Updates `Form_Status` based on last-5 vs career batting average |

### Stored Procedures

| Procedure | Description |
|---|---|
| `ScheduleMatch` | Inserts a match after checking for venue conflicts via `SIGNAL` |
| `RegisterPlayer` | Registers a player after checking jersey uniqueness via `SIGNAL` |
| `UpdateMatchResult` | ACID transaction to set the winner and trigger status update |
| `GenerateSportReport` | Cursor-based procedure returning aggregated stats per sport |

---

## ⚙️ Setup Instructions

### Prerequisites

- MySQL 8.0 installed and running
- Python 3.10+
- Git

### 1. Clone the repository

```bash
git clone https://github.com/MuditRanjan000/ARENA-SNU.git
cd ARENA-SNU
```

### 2. Install Python dependencies

```bash
pip install streamlit mysql-connector-python pandas plotly numpy python-dotenv
```

### 3. Create the `.env` file

Create a file named `.env` in the project root folder (same level as `main_app.py`):

```
DB_PASSWORD=your_mysql_root_password
```

> ⚠️ Never commit this file to GitHub. It is already in `.gitignore`.

### 4. Run the SQL files in order

Open **MySQL Workbench** (or any MySQL client) and run the following files **in this exact order**:

```
1. arena_setup.sql       ← Creates DB, all tables, inserts all dummy data
2. advanced_queries.sql  ← Creates triggers, procedures, views, GRANT/REVOKE
3. db_fixes.sql          ← Adds organiser role, icons, group names, rebuilds views
```

In MySQL Workbench:
- `File → Open SQL Script → select file → click the lightning bolt (Execute) icon`
- Wait for "X row(s) affected" and no red errors before running the next file

---

## ▶️ Running the App

```bash
streamlit run main_app.py
```

The app opens at `http://localhost:8501` in your browser.

---

## 🔐 Login Credentials

| Username | Password | Role | Access |
|---|---|---|---|
| `admin` | `arena@admin123` | Admin | Full access + Admin Panel |
| `organiser1` | `org@123` | Organiser | Score entry, Match scheduling + Match Result Entry |
| `manager1` | `manage123` | Manager | Team/Player management + Analytics + Predictions |
| `viewer1` | `view123` | Viewer | Public read-only pages (now includes sports leaderboards) |

---

## ✨ Features

### Home Dashboard
Live KPIs, Finals strip, Points table, Standings chart, and upcoming schedule — all fetched live from MySQL.

### Match Scheduling
`ScheduleMatch` stored procedure prevents double-booking at the database level. Accessible to admin and organiser.

### Score & Match Result Entry
Separate tabbed pages for Cricket, Football, and Basketball. Duplicate-entry guard before each player stats INSERT. Organisers can also declare match winners and input explicit overall scores directly from these pages or the home dashboard. All triggers fire automatically on save.

### ML Prediction
Fetches the last 10 scorecard entries for a player from MySQL, runs `numpy.polyfit` (degree 1) linear regression, plots the trend line with a 95% confidence band, and optionally saves the result to the `Predictions` table.

### Player Comparison
Head-to-head radar chart with stats normalised to 0–100 for fair cross-sport comparison. Edge winner per stat highlighted in the comparison table.

### Audit Log
6 database triggers auto-write every INSERT/UPDATE on Teams and Matches to `Audit_Log`. Visible to admin only. No Python code involved.

### Suspension System
`trg_suspend_player` automatically sets `Role='SUSPENDED'` when a football player's cumulative yellow cards across all matches reaches 3.

### Form Tracker
`trg_player_form` fires after every cricket score insert and updates `Form_Status` to **In Form**, **Out of Form**, or **Neutral** based on a comparison of the player's last-5-match average vs their career average.

---

## 📁 Project Structure

```
ARENA-SNU/
│
├── main_app.py          # Navigation hub, login, sidebar, session state
├── home_page.py         # Dashboard: KPIs, finals, points table, schedule
├── db_connection.py     # MySQL connection pool, run_query(), call_procedure()
├── page_schedule.py     # Match scheduling form (calls ScheduleMatch procedure)
├── page_cricket.py      # Cricket score entry + Orange Cap leaderboard
├── page_football.py     # Football score entry + Golden Boot + suspension tracker
├── page_basketball.py   # Basketball stats entry + MVP leaderboard + charts
├── page_comparison.py   # Radar chart player comparison (all 3 sports)
├── prediction.py        # ML prediction using numpy linear regression
│
├── arena_setup.sql      # DB creation, all tables, all dummy data (RUN FIRST)
├── advanced_queries.sql # Triggers, procedures, views, GRANTs, 15 queries (RUN SECOND)
├── db_fixes.sql         # ENUM fixes, icon columns, group names, view updates (RUN THIRD)
│
├── .env                 # DB_PASSWORD=yourpassword  ← CREATE THIS YOURSELF
├── .gitignore           # Excludes .env and __pycache__
└── README.md
```

---

## 🔧 Common Issues & Fixes

| Problem | Fix |
|---|---|
| `DB_PASSWORD` error / connection fails | Create `.env` file in project root: `DB_PASSWORD=yourpassword` |
| `plotly` not found | `pip install plotly` |
| `Finals_Overview` view missing | Run `db_fixes.sql` in MySQL Workbench |
| `organiser` role login fails | Run `db_fixes.sql` — adds organiser to Users ENUM |
| Icon column error in Sports | Run `db_fixes.sql` — adds Icon column safely |
| Form status not updating | Check `trg_player_form` exists — run `advanced_queries.sql` |
| `set_page_config` error | Each page wraps it in `try/except` — called once by `main_app.py` |
| Scorecard duplicate entry warning | Expected behaviour — app checks for existing entry before INSERT |

---

## 📦 Git Workflow

### Initial setup (one time)

```bash
git clone https://github.com/MuditRanjan000/ARENA-SNU.git
cd ARENA-SNU
git config user.name "Your Name"
git config user.email "your@email.com"
```

### Daily workflow

```bash
# 1. Always pull latest changes before you start working
git pull origin main

# 2. Make your changes to your assigned files

# 3. Stage your changes
git add .
# OR stage specific files only:
git add page_cricket.py page_football.py

# 4. Commit with a clear message
git commit -m "feat: add orange cap leaderboard to cricket page"

# 5. Push to GitHub
git push origin main
```

### If push is rejected (someone else pushed first)

```bash
git pull origin main   # pull their changes first
git push origin main   # now push yours
```

### Useful commands

```bash
git status                    # see what files changed
git log --oneline -10         # see last 10 commits
git diff filename.py          # see exactly what changed in a file
git checkout -- filename.py   # discard local changes to a file (CAREFUL)
git branch                    # check current branch
git branch -M main            # rename current branch to main
```

### Good commit message format

```
feat: short description of what you added
fix: short description of what you fixed
docs: updated README or comments
style: formatting changes only
```

**Examples:**
```
feat: add player suspension tracker to football page
fix: correct basketball player IDs in dummy data
docs: add setup instructions to README
feat: implement numpy confidence band in prediction page
```

---

## 📚 References

1. MySQL 8.0 Reference Manual — dev.mysql.com/doc/refman/8.0/en/
2. Streamlit Documentation — docs.streamlit.io
3. Plotly Python Documentation — plotly.com/python/
4. NumPy Documentation — numpy.org/doc/
5. mysql-connector-python — dev.mysql.com/doc/connector-python/en/
6. python-dotenv — pypi.org/project/python-dotenv/
7. Database System Concepts, 7th Ed — Silberschatz, Korth, Sudarshan

---

*ARENA SNU · Shiv Nadar University · SURGE 2025 · DBMS Group Project*  
*System Architect: Mudit (MuditRanjan000)*