-- ============================================================
--  ARENA SNU — DB Fixes (run AFTER arena_setup.sql +
--  advanced_queries.sql)
-- ============================================================
USE ARENA_SNU;

-- ── 1. Add organiser role to Users ENUM ─────────────────────
ALTER TABLE Users
    MODIFY Role ENUM('admin','organiser','manager','viewer') DEFAULT 'viewer';

-- ── 2. Add Icon column to Sports ────────────────────────────
DROP PROCEDURE IF EXISTS _AddIconColumn;
DELIMITER $$
CREATE PROCEDURE _AddIconColumn()
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM   information_schema.COLUMNS
        WHERE  TABLE_SCHEMA = 'ARENA_SNU'
          AND  TABLE_NAME   = 'Sports'
          AND  COLUMN_NAME  = 'Icon'
    ) THEN
        ALTER TABLE Sports ADD COLUMN Icon VARCHAR(10) DEFAULT '🏅';
    END IF;
END$$
DELIMITER ;
CALL _AddIconColumn();
DROP PROCEDURE IF EXISTS _AddIconColumn;

UPDATE Sports SET Icon='🏏' WHERE Sport_Name='Cricket';
UPDATE Sports SET Icon='⚽' WHERE Sport_Name='Football';
UPDATE Sports SET Icon='🏀' WHERE Sport_Name='Basketball';
UPDATE Sports SET Icon='🏸' WHERE Sport_Name='Badminton';
UPDATE Sports SET Icon='🏐' WHERE Sport_Name='Volleyball';
UPDATE Sports SET Icon='🏓' WHERE Sport_Name='Table Tennis';

-- ── 3. Add Group_Name column to Teams ───────────────────────
DROP PROCEDURE IF EXISTS _AddGroupNameColumn;
DELIMITER $$
CREATE PROCEDURE _AddGroupNameColumn()
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM   information_schema.COLUMNS
        WHERE  TABLE_SCHEMA = 'ARENA_SNU'
          AND  TABLE_NAME   = 'Teams'
          AND  COLUMN_NAME  = 'Group_Name'
    ) THEN
        ALTER TABLE Teams ADD COLUMN Group_Name VARCHAR(10) DEFAULT 'A';
    END IF;
END$$
DELIMITER ;
CALL _AddGroupNameColumn();
DROP PROCEDURE IF EXISTS _AddGroupNameColumn;

-- ── 3.1 Add Score Columns to Matches ────────────────────────
DROP PROCEDURE IF EXISTS _AddMatchScoreColumns;
DELIMITER $$
CREATE PROCEDURE _AddMatchScoreColumns()
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = 'ARENA_SNU' AND TABLE_NAME = 'Matches' AND COLUMN_NAME = 'Team_A_Score'
    ) THEN
        ALTER TABLE Matches ADD COLUMN Team_A_Score VARCHAR(20) DEFAULT NULL;
    END IF;
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = 'ARENA_SNU' AND TABLE_NAME = 'Matches' AND COLUMN_NAME = 'Team_B_Score'
    ) THEN
        ALTER TABLE Matches ADD COLUMN Team_B_Score VARCHAR(20) DEFAULT NULL;
    END IF;
END$$
DELIMITER ;
CALL _AddMatchScoreColumns();
DROP PROCEDURE IF EXISTS _AddMatchScoreColumns;

-- Assign groups for cricket teams
UPDATE Teams SET Group_Name='A' WHERE Team_ID IN (1,2) AND Sport_ID=1;
UPDATE Teams SET Group_Name='B' WHERE Team_ID IN (3,4) AND Sport_ID=1;
-- Football
UPDATE Teams SET Group_Name='A' WHERE Team_ID IN (5,6) AND Sport_ID=2;
UPDATE Teams SET Group_Name='B' WHERE Team_ID IN (7,8) AND Sport_ID=2;
-- Basketball
UPDATE Teams SET Group_Name='A' WHERE Team_ID IN (9,10) AND Sport_ID=3;
UPDATE Teams SET Group_Name='B' WHERE Team_ID IN (11) AND Sport_ID=3;

-- ── 4. Insert organiser user ─────────────────────────────────
INSERT IGNORE INTO Users (Username, Password, Role)
VALUES ('organiser1','org@123','organiser');

-- ── 5. Rebuild Upcoming_Schedule view with Sport_Icon ────────
CREATE OR REPLACE VIEW Upcoming_Schedule AS
SELECT
    sp.Icon       AS Sport_Icon,
    sp.Sport_Name,
    ta.Team_Name  AS Team_A,
    ta.University AS Uni_A,
    tb.Team_Name  AS Team_B,
    tb.University AS Uni_B,
    m.Match_Date,
    m.Match_Time,
    v.Venue_Name,
    m.Stage,
    m.Status,
    IFNULL(tw.Team_Name, 'TBD') AS Winner
FROM Matches m
JOIN Sports  sp ON m.Sport_ID  = sp.Sport_ID
JOIN Teams   ta ON m.Team_A_ID = ta.Team_ID
JOIN Teams   tb ON m.Team_B_ID = tb.Team_ID
JOIN Venues  v  ON m.Venue_ID  = v.Venue_ID
LEFT JOIN Teams tw ON m.Winner_Team_ID = tw.Team_ID
ORDER BY m.Match_Date, m.Match_Time;

-- ── 6. Create Finals_Overview view ──────────────────────────
CREATE OR REPLACE VIEW Finals_Overview AS
SELECT
    sp.Icon        AS Icon,
    sp.Sport_Name,
    ta.Team_Name   AS Team_A,
    tb.Team_Name   AS Team_B,
    m.Match_Date,
    m.Match_Time,
    v.Venue_Name,
    IFNULL(tw.Team_Name, 'TBD') AS Champion,
    m.Status
FROM Matches m
JOIN Sports sp  ON m.Sport_ID  = sp.Sport_ID
JOIN Teams  ta  ON m.Team_A_ID = ta.Team_ID
JOIN Teams  tb  ON m.Team_B_ID = tb.Team_ID
JOIN Venues v   ON m.Venue_ID  = v.Venue_ID
LEFT JOIN Teams tw ON m.Winner_Team_ID = tw.Team_ID
WHERE m.Stage = 'Final'
ORDER BY sp.Sport_Name;

-- ── 7. Create or refresh Points_Table view ───────────────────
CREATE OR REPLACE VIEW Points_Table AS
SELECT t.Team_Name, t.University, sp.Sport_Name, sp.Icon,
       COUNT(m.Match_ID) AS Matches_Played,
       SUM(CASE WHEN m.Winner_Team_ID = t.Team_ID THEN 1 ELSE 0 END)                             AS Wins,
       SUM(CASE WHEN m.Winner_Team_ID != t.Team_ID AND m.Winner_Team_ID IS NOT NULL THEN 1 ELSE 0 END) AS Losses,
       SUM(CASE WHEN m.Winner_Team_ID = t.Team_ID THEN 3 ELSE 0 END)                             AS Points
FROM   Teams   t
JOIN   Sports  sp ON t.Sport_ID = sp.Sport_ID
LEFT JOIN Matches m
       ON (m.Team_A_ID = t.Team_ID OR m.Team_B_ID = t.Team_ID)
      AND m.Status = 'Completed'
GROUP BY t.Team_ID, t.Team_Name, t.University, sp.Sport_Name, sp.Icon
ORDER BY sp.Sport_Name, Points DESC;

-- ── 8. Verify ────────────────────────────────────────────────
SELECT Username, Role FROM Users ORDER BY Role;
SELECT * FROM Finals_Overview;
SELECT * FROM Upcoming_Schedule LIMIT 5;
SELECT * FROM Points_Table LIMIT 5;

SELECT 'db_fixes.sql complete!' AS Status;