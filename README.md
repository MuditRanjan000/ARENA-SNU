# ARENA SNU v7 — Athletic Resource & Event Navigation Application

> SURGE 2025 Sports Festival · Shiv Nadar University · DBMS Group Project

## Tech Stack
Python 3.10+ · Streamlit · MySQL 8.0 · mysql-connector-python · pandas · plotly · numpy · python-dotenv

## Setup — Do This In Order

### 1. Install packages
```bash
pip install streamlit mysql-connector-python pandas plotly numpy python-dotenv scikit-learn
```

### 2. Run SQL files in MySQL Workbench (in this exact order)
```
1. arena_setup.sql      ← creates DB + all tables + dummy data
2. advanced_queries.sql ← triggers + procedures + views + GRANT
3. db_fixes.sql         ← adds organiser role, Icon column, Finals_Overview view
```

### 3. Create .env file in the project folder
```
DB_PASSWORD=your_mysql_root_password
```

### 4. Run the app
```bash
streamlit run main_app.py
```

---

## Login Credentials
| Username | Password | Role | Access |
|----------|----------|------|--------|
| admin | arena@admin123 | admin | Everything + Admin Panel |
| organiser1 | org@123 | organiser | Score entry (Cricket, Football, Basketball) |
| manager1 | manage123 | manager | Scheduling + Analytics |
| viewer1 | view123 | viewer | Public read-only (no login needed) |

---

## File Ownership
| File | Owner | Purpose |
|------|-------|---------|
| `main_app.py` | Mudit | Navigation, login gate, role routing, admin panel |
| `home_page.py` | Mudit | Dashboard, standings, awards, team/player management |
| `prediction.py` | Mudit | ML linear regression prediction with confidence intervals |
| `page_comparison.py` | Mudit | Radar chart player comparison |
| `page_cricket.py` | Ashank | Cricket T20, Orange/Purple Cap, form tracker |
| `page_football.py` | Ayush | Football stats, Golden Boot, suspension tracker |
| `page_basketball.py` | Amitog | Basketball stats, MVP leaderboard |
| `page_schedule.py` | Disha | Match scheduling via stored procedure |
| `db_connection.py` | Mudit | Shared MySQL connector (.env password) |
| `arena_setup.sql` | Mudit | Full DB setup |
| `advanced_queries.sql` | Mudit | Triggers, procedures, views, GRANT/REVOKE |
| `db_fixes.sql` | Mudit | Role fixes, Icon column, Finals_Overview view |

---

## Database: ARENA_SNU
**11 tables:** Sports, Venues, Teams, Players, Matches, Scorecard_Cricket, Scorecard_Football, Scorecard_Basketball, Users, Audit_Log, Predictions

**5 triggers:** trg_match_completed, trg_audit_teams_insert, trg_audit_teams_update, trg_suspend_player, trg_player_form

**3 procedures:** ScheduleMatch, RegisterPlayer, UpdateMatchResult (ACID transaction)

**5 views:** Upcoming_Schedule, Points_Table, Top_Scorers, Audit_View, Finals_Overview

---

## Novel Features (for Viva)
- **Audit Log** — DB triggers auto-log every INSERT/UPDATE, zero Python
- **ML Prediction** — numpy linear regression on match history with 95% CI
- **Form Tracker** — Trigger auto-updates player Form_Status after every cricket score
- **Suspension System** — Trigger auto-suspends football players at 3 yellow cards
- **Player Comparison** — Radar chart head-to-head across any two players
- **Finals Overview** — Dedicated DB view for all 3 sport finals
- **Role-Based Access** — Admin / Organiser / Manager / Viewer with different UI

---

## Role Access Matrix
| Page | Admin | Organiser | Manager | Viewer |
|------|-------|-----------|---------|--------|
| Home Dashboard | ✅ | ✅ | ✅ | ✅ |
| Schedule Match | ✅ | ❌ | ✅ | ❌ |
| Cricket Scores | ✅ | ✅ | ❌ | view only |
| Football Scores | ✅ | ✅ | ❌ | view only |
| Basketball Stats | ✅ | ✅ | ❌ | view only |
| Compare Players | ✅ | ❌ | ✅ | ✅ |
| Predictions | ✅ | ❌ | ✅ | ✅ |
| Admin Panel | ✅ | ❌ | ❌ | ❌ |

---

## Daily Git Workflow
```bash
git pull origin main        # always first
# ... do your work ...
git add .
git commit -m "what you did"
git push origin main        # always last
```

## Common Issues
| Problem | Fix |
|---------|-----|
| `DB_PASSWORD` error | Create `.env` file with `DB_PASSWORD=yourpassword` |
| `plotly` not found | `pip install plotly` |
| `Finals_Overview` missing | Run `db_fixes.sql` in Workbench |
| `organiser` role error | Run `db_fixes.sql` in Workbench |
| `git push` branch error | `git branch -M main && git push origin main` |
