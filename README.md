# ARENA SNU v6 — Athletic Resource & Event Navigation Application

> SURGE 2025 Sports Festival · Shiv Nadar University · DBMS Group Project

## Tech Stack
Python 3.10+ · Streamlit · MySQL 8.0 · mysql-connector-python · pandas · plotly · numpy

## Quick Setup
1. Run `arena_setup.sql` in MySQL Workbench, then `advanced_queries.sql`
2. Create `.env` in the project folder:  `DB_PASSWORD=your_mysql_root_password`
3. `pip install streamlit mysql-connector-python pandas plotly python-dotenv numpy`
4. `streamlit run main_app.py`

## File Ownership
| File | Owner | Purpose |
|------|-------|---------|
| `main_app.py` | Mudit | Navigation, login gate, role routing |
| `home_page.py` | Mudit | Dashboard, standings, awards, team/player mgmt |
| `prediction.py` | Mudit | ML linear regression prediction |
| `page_comparison.py` | Mudit | Radar chart comparison (all 6 sports) |
| `page_cricket.py` | Ashank | Cricket T20, Orange/Purple Cap, form tracker |
| `page_football.py` | Ayush | Football stats, Golden Boot, suspensions |
| `page_basketball.py` | Amitog | Basketball stats, MVP leaderboard |
| `page_badminton.py` | Team | Badminton Singles/Doubles leaderboards — NEW v6 |
| `page_tabletennis.py` | Team | Table Tennis Singles/Doubles — NEW v6 |
| `page_volleyball.py` | Team | Volleyball kills/blocks/aces — NEW v6 |
| `page_schedule.py` | Disha | Match scheduling via stored procedure |
| `db_connection.py` | Mudit | Shared MySQL connector |

## Sports Covered — SURGE 2025
🏏 Cricket · ⚽ Football · 🏀 Basketball · 🏸 Badminton · 🏓 Table Tennis · 🏐 Volleyball

## Login Credentials
| Username | Password | Role | Access |
|----------|----------|------|--------|
| admin | arena@admin123 | admin | Everything |
| organiser1 | org@123 | organiser | Score entry, all 6 sports |
| manager1 | manage123 | manager | Scheduling, analytics |
| viewer1 | view123 | viewer | Public pages (no login needed) |

## Novel Features (for Viva)
- **Audit Log** — DB triggers auto-log every INSERT/UPDATE, zero Python
- **ML Prediction** — numpy linear regression on match history with 95% CI
- **Form Tracker** — Trigger auto-updates player Form_Status after every cricket score
- **Suspension System** — Trigger auto-suspends football players at 3 yellow cards
- **Player Comparison** — Radar chart across all 6 sports
- **Public Access** — Viewers browse live data without any login
- **Finals Overview** — Dedicated DB view for all 6 sport finals