-- ============================================================
--  ARENA SNU — Advanced SQL: Triggers, Procedures, Views,
--  GRANT/REVOKE, Constraints, 15 Complex Queries
--  Run AFTER arena_setup.sql
-- ============================================================

USE ARENA_SNU;

-- ═══════════════════════ TRIGGERS ═══════════════════════════

DROP TRIGGER IF EXISTS trg_match_completed;
DELIMITER $$
CREATE TRIGGER trg_match_completed
BEFORE UPDATE ON Matches FOR EACH ROW
BEGIN
    IF NEW.Winner_Team_ID IS NOT NULL AND OLD.Winner_Team_ID IS NULL THEN
        SET NEW.Status = 'Completed';
    END IF;
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_audit_teams_insert;
DELIMITER $$
CREATE TRIGGER trg_audit_teams_insert
AFTER INSERT ON Teams FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log (Table_Name, Operation, Record_ID, New_Value)
    VALUES ('Teams','INSERT',NEW.Team_ID,
            CONCAT('Team: ',NEW.Team_Name,' | Uni: ',NEW.University,' | Sport_ID: ',NEW.Sport_ID));
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_audit_teams_update;
DELIMITER $$
CREATE TRIGGER trg_audit_teams_update
AFTER UPDATE ON Teams FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log (Table_Name, Operation, Record_ID, Old_Value, New_Value)
    VALUES ('Teams','UPDATE',NEW.Team_ID,
            CONCAT('Team: ',OLD.Team_Name,' | Coach: ',IFNULL(OLD.Coach_Name,'N/A')),
            CONCAT('Team: ',NEW.Team_Name,' | Coach: ',IFNULL(NEW.Coach_Name,'N/A')));
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_suspend_player;
DELIMITER $$
CREATE TRIGGER trg_suspend_player
AFTER INSERT ON Scorecard_Football FOR EACH ROW
BEGIN
    DECLARE total_yellows INT;
    SELECT SUM(Yellow_Cards) INTO total_yellows
    FROM Scorecard_Football WHERE Player_ID = NEW.Player_ID;
    IF total_yellows >= 3 THEN
        UPDATE Players SET Role = 'SUSPENDED' WHERE Player_ID = NEW.Player_ID;
    END IF;
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_player_form;
DELIMITER $$
CREATE TRIGGER trg_player_form
AFTER INSERT ON Scorecard_Cricket FOR EACH ROW
BEGIN
    DECLARE recent_avg DECIMAL(10,2);
    DECLARE overall_avg DECIMAL(10,2);
    SELECT AVG(Runs_Scored) INTO recent_avg FROM (
        SELECT Runs_Scored FROM Scorecard_Cricket
        WHERE Player_ID = NEW.Player_ID ORDER BY Stat_ID DESC LIMIT 5
    ) AS last5;
    SELECT AVG(Runs_Scored) INTO overall_avg
    FROM Scorecard_Cricket WHERE Player_ID = NEW.Player_ID;
    IF recent_avg IS NOT NULL AND overall_avg IS NOT NULL THEN
        IF recent_avg >= overall_avg * 1.2 THEN
            UPDATE Players SET Form_Status = 'In Form' WHERE Player_ID = NEW.Player_ID;
        ELSEIF recent_avg <= overall_avg * 0.8 THEN
            UPDATE Players SET Form_Status = 'Out of Form' WHERE Player_ID = NEW.Player_ID;
        ELSE
            UPDATE Players SET Form_Status = 'Neutral' WHERE Player_ID = NEW.Player_ID;
        END IF;
    END IF;
END$$
DELIMITER ;

-- ═══════════════════ STORED PROCEDURES ══════════════════════

DROP PROCEDURE IF EXISTS ScheduleMatch;
DELIMITER $$
CREATE PROCEDURE ScheduleMatch(
    IN p_sport_id INT, IN p_team_a INT, IN p_team_b INT,
    IN p_date DATE, IN p_time TIME, IN p_venue_id INT, IN p_stage VARCHAR(50)
)
BEGIN
    DECLARE conflict INT;
    SELECT COUNT(*) INTO conflict FROM Matches
    WHERE Venue_ID=p_venue_id AND Match_Date=p_date AND Match_Time=p_time;
    IF conflict > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Venue already booked at this date and time!';
    ELSEIF p_team_a = p_team_b THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Team A and Team B cannot be the same!';
    ELSE
        INSERT INTO Matches (Sport_ID,Team_A_ID,Team_B_ID,Match_Date,Match_Time,Venue_ID,Stage,Status)
        VALUES (p_sport_id,p_team_a,p_team_b,p_date,p_time,p_venue_id,p_stage,'Scheduled');
        SELECT LAST_INSERT_ID() AS New_Match_ID, 'Match scheduled successfully!' AS Message;
    END IF;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS RegisterPlayer;
DELIMITER $$
CREATE PROCEDURE RegisterPlayer(
    IN p_name VARCHAR(100), IN p_team_id INT, IN p_role VARCHAR(50), IN p_jersey INT
)
BEGIN
    DECLARE jersey_taken INT;
    SELECT COUNT(*) INTO jersey_taken FROM Players
    WHERE Team_ID=p_team_id AND Jersey_No=p_jersey;
    IF jersey_taken > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Jersey number already taken in this team!';
    ELSE
        INSERT INTO Players (Player_Name,Team_ID,Role,Jersey_No,Form_Status)
        VALUES (p_name,p_team_id,p_role,p_jersey,'Neutral');
        SELECT LAST_INSERT_ID() AS New_Player_ID, 'Player registered successfully!' AS Message;
    END IF;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS UpdateMatchResult;
DELIMITER $$
CREATE PROCEDURE UpdateMatchResult(IN p_match_id INT, IN p_winner_id INT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; SELECT 'ERROR: Transaction rolled back!' AS Message; END;
    START TRANSACTION;
    IF NOT EXISTS (SELECT 1 FROM Matches WHERE Match_ID=p_match_id AND Status='Scheduled') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Match not found or already completed!';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM Matches WHERE Match_ID=p_match_id AND (Team_A_ID=p_winner_id OR Team_B_ID=p_winner_id)) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Winner must be one of the two teams in this match!';
    END IF;
    UPDATE Matches SET Winner_Team_ID=p_winner_id WHERE Match_ID=p_match_id;
    INSERT INTO Audit_Log (Table_Name,Operation,Record_ID,New_Value)
    VALUES ('Matches','UPDATE',p_match_id,CONCAT('Winner set: Team_ID=',p_winner_id));
    COMMIT;
    SELECT 'Match result updated successfully!' AS Message;
END$$
DELIMITER ;

-- ════════════════════════ VIEWS ═════════════════════════════

CREATE OR REPLACE VIEW Upcoming_Schedule AS
SELECT m.Match_ID, sp.Sport_Name,
    ta.Team_Name AS Team_A, ta.University AS Uni_A,
    tb.Team_Name AS Team_B, tb.University AS Uni_B,
    m.Match_Date, m.Match_Time, v.Venue_Name, m.Stage, m.Status,
    IFNULL(tw.Team_Name,'TBD') AS Winner
FROM Matches m
JOIN Sports sp ON m.Sport_ID=sp.Sport_ID
JOIN Teams ta ON m.Team_A_ID=ta.Team_ID
JOIN Teams tb ON m.Team_B_ID=tb.Team_ID
JOIN Venues v ON m.Venue_ID=v.Venue_ID
LEFT JOIN Teams tw ON m.Winner_Team_ID=tw.Team_ID
ORDER BY m.Match_Date, m.Match_Time;

CREATE OR REPLACE VIEW Points_Table AS
SELECT t.Team_Name, t.University, sp.Sport_Name,
    COUNT(m.Match_ID) AS Matches_Played,
    SUM(CASE WHEN m.Winner_Team_ID=t.Team_ID THEN 1 ELSE 0 END) AS Wins,
    SUM(CASE WHEN m.Winner_Team_ID!=t.Team_ID AND m.Winner_Team_ID IS NOT NULL THEN 1 ELSE 0 END) AS Losses,
    SUM(CASE WHEN m.Winner_Team_ID=t.Team_ID THEN 3 ELSE 0 END) AS Points
FROM Teams t
JOIN Sports sp ON t.Sport_ID=sp.Sport_ID
LEFT JOIN Matches m ON (m.Team_A_ID=t.Team_ID OR m.Team_B_ID=t.Team_ID) AND m.Status='Completed'
GROUP BY t.Team_ID ORDER BY sp.Sport_Name, Points DESC;

CREATE OR REPLACE VIEW Top_Scorers AS
SELECT p.Player_Name, t.Team_Name, t.University, 'Cricket' AS Sport, 'Runs' AS Metric, SUM(sc.Runs_Scored) AS Total
FROM Scorecard_Cricket sc JOIN Players p ON sc.Player_ID=p.Player_ID JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sc.Player_ID
UNION ALL
SELECT p.Player_Name, t.Team_Name, t.University, 'Football', 'Goals', SUM(sf.Goals)
FROM Scorecard_Football sf JOIN Players p ON sf.Player_ID=p.Player_ID JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sf.Player_ID
UNION ALL
SELECT p.Player_Name, t.Team_Name, t.University, 'Basketball', 'Avg Points', AVG(sb.Points)
FROM Scorecard_Basketball sb JOIN Players p ON sb.Player_ID=p.Player_ID JOIN Teams t ON p.Team_ID=t.Team_ID GROUP BY sb.Player_ID
ORDER BY Sport, Total DESC;

CREATE OR REPLACE VIEW Audit_View AS
SELECT Log_ID, Table_Name, Operation, Record_ID, Changed_At,
    IFNULL(Old_Value,'N/A') AS Old_Value, IFNULL(New_Value,'N/A') AS New_Value
FROM Audit_Log ORDER BY Changed_At DESC;

-- ════════════════════ GRANT / REVOKE ════════════════════════

CREATE USER IF NOT EXISTS 'arena_admin'@'localhost'   IDENTIFIED BY 'admin123';
CREATE USER IF NOT EXISTS 'arena_manager'@'localhost' IDENTIFIED BY 'manager123';
CREATE USER IF NOT EXISTS 'arena_viewer'@'localhost'  IDENTIFIED BY 'viewer123';

GRANT ALL PRIVILEGES ON ARENA_SNU.* TO 'arena_admin'@'localhost';

GRANT SELECT ON ARENA_SNU.* TO 'arena_manager'@'localhost';
GRANT INSERT, UPDATE ON ARENA_SNU.Scorecard_Cricket    TO 'arena_manager'@'localhost';
GRANT INSERT, UPDATE ON ARENA_SNU.Scorecard_Football   TO 'arena_manager'@'localhost';
GRANT INSERT, UPDATE ON ARENA_SNU.Scorecard_Basketball TO 'arena_manager'@'localhost';
GRANT INSERT ON ARENA_SNU.Matches TO 'arena_manager'@'localhost';

GRANT SELECT ON ARENA_SNU.Sports           TO 'arena_viewer'@'localhost';
GRANT SELECT ON ARENA_SNU.Teams            TO 'arena_viewer'@'localhost';
GRANT SELECT ON ARENA_SNU.Players          TO 'arena_viewer'@'localhost';
GRANT SELECT ON ARENA_SNU.Matches          TO 'arena_viewer'@'localhost';
GRANT SELECT ON ARENA_SNU.Venues           TO 'arena_viewer'@'localhost';
GRANT SELECT ON ARENA_SNU.Scorecard_Cricket    TO 'arena_viewer'@'localhost';
GRANT SELECT ON ARENA_SNU.Scorecard_Football   TO 'arena_viewer'@'localhost';
GRANT SELECT ON ARENA_SNU.Scorecard_Basketball TO 'arena_viewer'@'localhost';
GRANT SELECT ON ARENA_SNU.Upcoming_Schedule    TO 'arena_viewer'@'localhost';
GRANT SELECT ON ARENA_SNU.Points_Table         TO 'arena_viewer'@'localhost';
GRANT SELECT ON ARENA_SNU.Top_Scorers          TO 'arena_viewer'@'localhost';
FLUSH PRIVILEGES;

-- ═══════════════════ 15 COMPLEX QUERIES ═════════════════════

-- Q1: INNER JOIN — full schedule with names
SELECT m.Match_ID, sp.Sport_Name, ta.Team_Name AS Team_A, tb.Team_Name AS Team_B, v.Venue_Name, m.Match_Date, m.Status
FROM Matches m INNER JOIN Sports sp ON m.Sport_ID=sp.Sport_ID INNER JOIN Teams ta ON m.Team_A_ID=ta.Team_ID
INNER JOIN Teams tb ON m.Team_B_ID=tb.Team_ID INNER JOIN Venues v ON m.Venue_ID=v.Venue_ID;

-- Q2: LEFT JOIN — all teams including zero matches
SELECT t.Team_Name, t.University, sp.Sport_Name, COUNT(m.Match_ID) AS Total_Matches
FROM Teams t LEFT JOIN Matches m ON (m.Team_A_ID=t.Team_ID OR m.Team_B_ID=t.Team_ID)
JOIN Sports sp ON t.Sport_ID=sp.Sport_ID GROUP BY t.Team_ID ORDER BY Total_Matches DESC;

-- Q3: GROUP BY + HAVING — universities with 2+ teams
SELECT University, COUNT(*) AS Total_Teams FROM Teams GROUP BY University HAVING COUNT(*) >= 2 ORDER BY Total_Teams DESC;

-- Q4: Orange Cap — highest runs
SELECT p.Player_Name, t.Team_Name, t.University, SUM(sc.Runs_Scored) AS Total_Runs, SUM(sc.Wickets_Taken) AS Total_Wickets
FROM Scorecard_Cricket sc JOIN Players p ON sc.Player_ID=p.Player_ID JOIN Teams t ON p.Team_ID=t.Team_ID
GROUP BY sc.Player_ID ORDER BY Total_Runs DESC LIMIT 1;

-- Q5: Golden Boot — highest goals
SELECT p.Player_Name, t.Team_Name, t.University, SUM(sf.Goals) AS Total_Goals, SUM(sf.Assists) AS Total_Assists
FROM Scorecard_Football sf JOIN Players p ON sf.Player_ID=p.Player_ID JOIN Teams t ON p.Team_ID=t.Team_ID
GROUP BY sf.Player_ID ORDER BY Total_Goals DESC LIMIT 1;

-- Q6: MVP — highest avg points (AVG + HAVING)
SELECT p.Player_Name, t.Team_Name, t.University, AVG(sb.Points) AS Avg_Points, COUNT(sb.Match_ID) AS Games_Played
FROM Scorecard_Basketball sb JOIN Players p ON sb.Player_ID=p.Player_ID JOIN Teams t ON p.Team_ID=t.Team_ID
GROUP BY sb.Player_ID HAVING COUNT(sb.Match_ID) >= 1 ORDER BY Avg_Points DESC LIMIT 1;

-- Q7: Subquery — teams with at least 1 win
SELECT Team_Name, University FROM Teams WHERE Team_ID IN (
    SELECT DISTINCT Winner_Team_ID FROM Matches WHERE Winner_Team_ID IS NOT NULL);

-- Q8: Correlated subquery — players above team avg runs
SELECT p.Player_Name, t.Team_Name, sc.Runs_Scored FROM Scorecard_Cricket sc
JOIN Players p ON sc.Player_ID=p.Player_ID JOIN Teams t ON p.Team_ID=t.Team_ID
WHERE sc.Runs_Scored > (SELECT AVG(sc2.Runs_Scored) FROM Scorecard_Cricket sc2
    JOIN Players p2 ON sc2.Player_ID=p2.Player_ID WHERE p2.Team_ID=t.Team_ID);

-- Q9: UNION — all scorers across 3 sports
SELECT p.Player_Name,'Cricket' AS Sport FROM Scorecard_Cricket sc JOIN Players p ON sc.Player_ID=p.Player_ID
UNION SELECT p.Player_Name,'Football' FROM Scorecard_Football sf JOIN Players p ON sf.Player_ID=p.Player_ID
UNION SELECT p.Player_Name,'Basketball' FROM Scorecard_Basketball sb JOIN Players p ON sb.Player_ID=p.Player_ID;

-- Q10: CASE WHEN — points table
SELECT t.Team_Name, sp.Sport_Name,
    SUM(CASE WHEN m.Winner_Team_ID=t.Team_ID THEN 1 ELSE 0 END) AS Wins,
    SUM(CASE WHEN m.Winner_Team_ID=t.Team_ID THEN 3 ELSE 0 END) AS Points
FROM Teams t JOIN Sports sp ON t.Sport_ID=sp.Sport_ID
LEFT JOIN Matches m ON (m.Team_A_ID=t.Team_ID OR m.Team_B_ID=t.Team_ID)
GROUP BY t.Team_ID ORDER BY Points DESC;

-- Q11: Nested subquery — busiest sport
SELECT Sport_Name, Total FROM (
    SELECT sp.Sport_Name, COUNT(*) AS Total FROM Matches m JOIN Sports sp ON m.Sport_ID=sp.Sport_ID GROUP BY sp.Sport_ID
) AS counts ORDER BY Total DESC LIMIT 1;

-- Q12: Full player profile — 3-table JOIN
SELECT p.Player_Name, p.Role, p.Jersey_No, p.Form_Status, t.Team_Name, t.University, sp.Sport_Name
FROM Players p JOIN Teams t ON p.Team_ID=t.Team_ID JOIN Sports sp ON t.Sport_ID=sp.Sport_ID
ORDER BY sp.Sport_Name, t.Team_Name;

-- Q13: Audit log recent changes
SELECT Table_Name, Operation, Record_ID, Changed_At, Old_Value, New_Value FROM Audit_View LIMIT 20;

-- Q14: Transaction demo
START TRANSACTION;
INSERT INTO Scorecard_Cricket (Match_ID,Player_ID,Runs_Scored,Wickets_Taken,Overs_Bowled) VALUES (1,1,75,2,4.0);
COMMIT;

-- Q15: Suspended players
SELECT p.Player_Name, t.Team_Name, t.University, SUM(sf.Yellow_Cards) AS Total_Yellows
FROM Scorecard_Football sf JOIN Players p ON sf.Player_ID=p.Player_ID JOIN Teams t ON p.Team_ID=t.Team_ID
WHERE p.Role='SUSPENDED' GROUP BY sf.Player_ID;

SELECT 'ARENA_SNU Advanced SQL setup complete!' AS Status;
