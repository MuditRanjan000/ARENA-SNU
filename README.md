# ARENA SNU — Athletic Resource & Event Navigation Application

> SURGE Sports Festival · Shiv Nadar University · DBMS Group Project

## Tech Stack
Python 3.10+ · Streamlit · MySQL 8.0 · mysql-connector-python · pandas · plotly · numpy

## Setup
1. Run `arena_setup.sql` then `advanced_queries.sql` in MySQL Workbench
2. Create a `.env` file in the project folder:  `DB_PASSWORD=your_mysql_root_password`
3. Install dependencies: `pip install streamlit mysql-connector-python pandas plotly python-dotenv`
4. Run: `streamlit run main_app.py`

## Files
| File | Owner | Purpose |
|------|-------|---------|
| `main_app.py` | Mudit | Navigation hub, login gate, role-based routing |
| `home_page.py` | Mudit | Dashboard, standings, awards, team/player management |
| `prediction.py` | Mudit | ML prediction (linear regression → MySQL) |
| `page_comparison.py` | Mudit | Player comparison radar chart |
| `page_cricket.py` | Ashank | Cricket scores, Orange/Purple Cap, form tracker |
| `page_football.py` | Ayush | Football scores, Golden Boot, suspension tracker |
| `page_basketball.py` | Amitog | Basketball scores, MVP leaderboard |
| `page_schedule.py` | Disha | Match scheduling via stored procedure |
| `db_connection.py` | Mudit | Shared MySQL connector |

## Login Credentials
| Username | Password | Role |
|----------|----------|------|
| admin | arena@admin123 | admin |
| mudit | mudit123 | admin |
| manager1 | manage123 | manager |
| viewer1 | view123 | viewer |

## Novel Features
- **Audit Log** — DB triggers auto-record every INSERT/UPDATE to `Audit_Log`
- **ML Prediction** — Python linear regression on MySQL match history, saves back to DB
- **Form Tracker** — Trigger auto-updates `Form_Status` after every cricket score
- **Player Comparison** — Radar chart head-to-head across all 3 sports