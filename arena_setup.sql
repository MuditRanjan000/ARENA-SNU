-- ============================================================
--  ARENA SNU — Complete Database Setup
--  Athletic Resource & Event Navigation Application
--  System Architect: Mudit | Run this FIRST
-- ============================================================

DROP DATABASE IF EXISTS ARENA_SNU;
CREATE DATABASE ARENA_SNU;
USE ARENA_SNU;

-- ── TABLE 1: Sports ─────────────────────────────────────────
CREATE TABLE Sports (
    Sport_ID   INT AUTO_INCREMENT PRIMARY KEY,
    Sport_Name VARCHAR(50) NOT NULL UNIQUE,
    Team_Size  INT NOT NULL,
    Format     VARCHAR(100),
    CONSTRAINT chk_team_size CHECK (Team_Size BETWEEN 1 AND 15)
);
INSERT INTO Sports (Sport_Name, Team_Size, Format) VALUES
('Cricket',11,'T20 format, knockout rounds'),
('Football',11,'90 min matches, group + knockout'),
('Basketball',5,'40 min matches, group + knockout'),
('Badminton',1,'Singles and Doubles categories'),
('Volleyball',6,'Best of 3 sets format'),
('Table Tennis',1,'Singles, round robin');

-- ── TABLE 2: Venues ─────────────────────────────────────────
CREATE TABLE Venues (
    Venue_ID   INT AUTO_INCREMENT PRIMARY KEY,
    Venue_Name VARCHAR(100) NOT NULL UNIQUE,
    Location   VARCHAR(100) NOT NULL,
    Capacity   INT,
    CONSTRAINT chk_capacity CHECK (Capacity > 0)
);
INSERT INTO Venues (Venue_Name, Location, Capacity) VALUES
('SNU Indoor Sports Complex','Shiv Nadar University, Greater Noida',500),
('SNU Football Ground','Shiv Nadar University, Greater Noida',1000),
('SNU Basketball Court','Shiv Nadar University, Greater Noida',300),
('SNU Cricket Ground','Shiv Nadar University, Greater Noida',800),
('SNU Badminton Hall','Shiv Nadar University, Greater Noida',200),
('SNU Table Tennis Arena','Shiv Nadar University, Greater Noida',150);

-- ── TABLE 3: Teams ─────────────────────────────────────────
CREATE TABLE Teams (
    Team_ID    INT AUTO_INCREMENT PRIMARY KEY,
    Team_Name  VARCHAR(100) NOT NULL,
    University VARCHAR(100) NOT NULL,
    Sport_ID   INT NOT NULL,
    Coach_Name VARCHAR(100),
    FOREIGN KEY (Sport_ID) REFERENCES Sports(Sport_ID),
    CONSTRAINT uq_team_sport UNIQUE (Team_Name, Sport_ID)
);
INSERT INTO Teams (Team_Name, University, Sport_ID, Coach_Name) VALUES
('SNU Strikers','Shiv Nadar University',1,'Rajiv Sharma'),
('DTU Thunder','Delhi Technological University',1,'Anil Kapoor'),
('NSUT Blaze','NSUT Delhi',1,'Suresh Nair'),
('Amity Aces','Amity University',1,'Vikas Gupta'),
('SNU FC','Shiv Nadar University',2,'Carlos Mendes'),
('DTU United','Delhi Technological University',2,'Rohit Verma'),
('Jamia Eleven','Jamia Millia Islamia',2,'Farhan Sheikh'),
('Bennett FC','Bennett University',2,'Priya Nair'),
('SNU Hoops','Shiv Nadar University',3,'Mike Johnson'),
('NSUT Ballers','NSUT Delhi',3,'Deepak Singh'),
('Amity Dunkers','Amity University',3,'Neha Kapoor'),
('SNU Smashers','Shiv Nadar University',4,'Prakash Nath'),
('DTU Shuttlers','Delhi Technological University',4,'Saina Mehta'),
('SNU Spikes','Shiv Nadar University',5,'Arjun Das'),
('Jamia Spikers','Jamia Millia Islamia',5,'Kabir Khan'),
('SNU Spinners','Shiv Nadar University',6,'Liu Wei');

-- ── TABLE 4: Players ──────────────────────────────────────
CREATE TABLE Players (
    Player_ID   INT AUTO_INCREMENT PRIMARY KEY,
    Player_Name VARCHAR(100) NOT NULL,
    Team_ID     INT NOT NULL,
    Role        VARCHAR(50),
    Jersey_No   INT,
    Form_Status VARCHAR(20) DEFAULT 'Neutral',
    FOREIGN KEY (Team_ID) REFERENCES Teams(Team_ID),
    CONSTRAINT chk_jersey CHECK (Jersey_No BETWEEN 1 AND 99),
    CONSTRAINT uq_jersey_team UNIQUE (Jersey_No, Team_ID)
);
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Arjun Mehta',1,'Batsman',7),('Rohan Tiwari',1,'Bowler',10),('Sahil Gupta',1,'All-Rounder',4),
('Karan Sharma',2,'Batsman',18),('Prateek Singh',2,'Bowler',22),('Harsh Verma',2,'Wicketkeeper',3),
('Vikram Nair',5,'Striker',9),('Aditya Roy',5,'Midfielder',8),('Ankit Joshi',5,'Goalkeeper',1),
('Rahul Das',6,'Striker',11),('Deepak Yadav',6,'Defender',5),
('Nikhil Bose',9,'Point Guard',23),('Rishabh Jain',9,'Center',33),('Arnav Singh',9,'Shooting Guard',3),
('Tarun Gupta',10,'Point Guard',12),('Vivek Kumar',10,'Forward',7),
('Akash Rathi',12,'Singles',1),('Saurabh Negi',13,'Singles',1),
('Manish Patel',14,'Setter',4),('Gaurav Rao',14,'Spiker',7),
('Ritesh Malhotra',16,'Singles',1);

-- ── TABLE 5: Matches ─────────────────────────────────────
CREATE TABLE Matches (
    Match_ID       INT AUTO_INCREMENT PRIMARY KEY,
    Sport_ID       INT NOT NULL,
    Team_A_ID      INT NOT NULL,
    Team_B_ID      INT NOT NULL,
    Match_Date     DATE NOT NULL,
    Match_Time     TIME NOT NULL,
    Venue_ID       INT NOT NULL,
    Stage          ENUM('Group Stage','Quarter-Final','Semi-Final','Final') DEFAULT 'Group Stage',
    Winner_Team_ID INT DEFAULT NULL,
    Status         ENUM('Scheduled','Completed','Cancelled') DEFAULT 'Scheduled',
    FOREIGN KEY (Sport_ID)       REFERENCES Sports(Sport_ID),
    FOREIGN KEY (Team_A_ID)      REFERENCES Teams(Team_ID),
    FOREIGN KEY (Team_B_ID)      REFERENCES Teams(Team_ID),
    FOREIGN KEY (Venue_ID)       REFERENCES Venues(Venue_ID),
    FOREIGN KEY (Winner_Team_ID) REFERENCES Teams(Team_ID),
    CONSTRAINT chk_teams CHECK (Team_A_ID != Team_B_ID)
);
INSERT INTO Matches (Sport_ID,Team_A_ID,Team_B_ID,Match_Date,Match_Time,Venue_ID,Stage,Winner_Team_ID,Status) VALUES
(1,1,2,'2025-03-10','09:00:00',4,'Group Stage',1,'Completed'),
(1,3,4,'2025-03-10','14:00:00',4,'Group Stage',3,'Completed'),
(2,5,6,'2025-03-11','10:00:00',2,'Group Stage',5,'Completed'),
(2,7,8,'2025-03-11','14:00:00',2,'Group Stage',7,'Completed'),
(3,9,10,'2025-03-12','11:00:00',3,'Group Stage',9,'Completed'),
(4,12,13,'2025-03-13','10:00:00',5,'Semi-Final',12,'Completed'),
(5,14,15,'2025-03-13','14:00:00',2,'Group Stage',14,'Completed'),
(1,1,3,'2025-03-14','10:00:00',4,'Semi-Final',NULL,'Scheduled'),
(2,5,7,'2025-03-14','14:00:00',2,'Semi-Final',NULL,'Scheduled'),
(3,9,11,'2025-03-15','11:00:00',3,'Final',NULL,'Scheduled');

-- ── TABLE 6-8: Scorecards ────────────────────────────────
CREATE TABLE Scorecard_Cricket (
    Stat_ID       INT AUTO_INCREMENT PRIMARY KEY,
    Match_ID      INT NOT NULL,
    Player_ID     INT NOT NULL,
    Runs_Scored   INT DEFAULT 0,
    Wickets_Taken INT DEFAULT 0,
    Overs_Bowled  DECIMAL(4,1) DEFAULT 0.0,
    Catches       INT DEFAULT 0,
    FOREIGN KEY (Match_ID)  REFERENCES Matches(Match_ID),
    FOREIGN KEY (Player_ID) REFERENCES Players(Player_ID),
    CONSTRAINT chk_runs CHECK (Runs_Scored >= 0),
    CONSTRAINT chk_wkts CHECK (Wickets_Taken BETWEEN 0 AND 10),
    CONSTRAINT chk_ovrs CHECK (Overs_Bowled >= 0)
);

CREATE TABLE Scorecard_Football (
    Stat_ID      INT AUTO_INCREMENT PRIMARY KEY,
    Match_ID     INT NOT NULL,
    Player_ID    INT NOT NULL,
    Goals        INT DEFAULT 0,
    Assists      INT DEFAULT 0,
    Yellow_Cards INT DEFAULT 0,
    Red_Cards    INT DEFAULT 0,
    FOREIGN KEY (Match_ID)  REFERENCES Matches(Match_ID),
    FOREIGN KEY (Player_ID) REFERENCES Players(Player_ID),
    CONSTRAINT chk_goals  CHECK (Goals >= 0),
    CONSTRAINT chk_asst   CHECK (Assists >= 0),
    CONSTRAINT chk_yc     CHECK (Yellow_Cards BETWEEN 0 AND 2),
    CONSTRAINT chk_rc     CHECK (Red_Cards BETWEEN 0 AND 1)
);

CREATE TABLE Scorecard_Basketball (
    Stat_ID   INT AUTO_INCREMENT PRIMARY KEY,
    Match_ID  INT NOT NULL,
    Player_ID INT NOT NULL,
    Points    INT DEFAULT 0,
    Rebounds  INT DEFAULT 0,
    Assists   INT DEFAULT 0,
    Steals    INT DEFAULT 0,
    FOREIGN KEY (Match_ID)  REFERENCES Matches(Match_ID),
    FOREIGN KEY (Player_ID) REFERENCES Players(Player_ID),
    CONSTRAINT chk_pts CHECK (Points >= 0),
    CONSTRAINT chk_reb CHECK (Rebounds >= 0)
);

-- ── TABLE 9: Users ───────────────────────────────────────
CREATE TABLE Users (
    User_ID    INT AUTO_INCREMENT PRIMARY KEY,
    Username   VARCHAR(50) NOT NULL UNIQUE,
    Password   VARCHAR(255) NOT NULL,
    Role       ENUM('admin','manager','viewer') DEFAULT 'viewer',
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO Users (Username, Password, Role) VALUES
('admin','arena@admin123','admin'),
('mudit','mudit123','admin'),
('manager1','manage123','manager'),
('viewer1','view123','viewer');

-- ── TABLE 10: Audit_Log ─────────────────────────────────
CREATE TABLE Audit_Log (
    Log_ID     INT AUTO_INCREMENT PRIMARY KEY,
    Table_Name VARCHAR(50) NOT NULL,
    Operation  ENUM('INSERT','UPDATE','DELETE') NOT NULL,
    Record_ID  INT,
    Changed_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Old_Value  TEXT,
    New_Value  TEXT
);

-- ── TABLE 11: Predictions ───────────────────────────────
CREATE TABLE Predictions (
    Pred_ID         INT AUTO_INCREMENT PRIMARY KEY,
    Player_ID       INT NOT NULL,
    Sport_Name      VARCHAR(50),
    Predicted_Score DECIMAL(10,2),
    Predicted_At    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Player_ID) REFERENCES Players(Player_ID)
);

-- ── INSERT SCORECARD DUMMY DATA ──────────────────────────
INSERT INTO Scorecard_Cricket (Match_ID,Player_ID,Runs_Scored,Wickets_Taken,Overs_Bowled,Catches) VALUES
(1,1,85,0,0.0,1),(1,2,12,3,4.0,0),(1,3,45,1,2.0,1),
(1,4,32,1,3.0,0),(1,5,8,2,4.0,1),
(2,7,55,0,0.0,0),(2,8,28,1,2.0,1);

INSERT INTO Scorecard_Football (Match_ID,Player_ID,Goals,Assists,Yellow_Cards,Red_Cards) VALUES
(3,7,2,1,0,0),(3,8,0,2,1,0),(3,9,0,0,0,0),
(4,10,1,0,1,0),(4,11,0,1,0,0);

INSERT INTO Scorecard_Basketball (Match_ID,Player_ID,Points,Rebounds,Assists,Steals) VALUES
(5,12,24,3,8,2),(5,13,18,12,2,1),(5,14,15,4,6,3),
(5,15,20,6,3,2),(5,16,12,8,1,1);

-- ── INDEXES ─────────────────────────────────────────────
CREATE INDEX idx_matches_date    ON Matches(Match_Date);
CREATE INDEX idx_matches_sport   ON Matches(Sport_ID);
CREATE INDEX idx_players_team    ON Players(Team_ID);
CREATE INDEX idx_cricket_player  ON Scorecard_Cricket(Player_ID);
CREATE INDEX idx_football_player ON Scorecard_Football(Player_ID);

SELECT 'ARENA_SNU base setup complete! Now run advanced_queries.sql' AS Status;
