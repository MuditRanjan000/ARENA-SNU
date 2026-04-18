-- ============================================================
--  ARENA SNU v7 — Complete Database Setup
--  SURGE 2025 Sports Festival · Shiv Nadar University
--  Sports: Cricket · Football · Basketball
--  System Architect: Mudit | Run this FIRST
-- ============================================================

DROP DATABASE IF EXISTS ARENA_SNU;
CREATE DATABASE ARENA_SNU CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ARENA_SNU;

-- ── TABLE 1: Sports ─────────────────────────────────────────
CREATE TABLE Sports (
    Sport_ID   INT AUTO_INCREMENT PRIMARY KEY,
    Sport_Name VARCHAR(50)  NOT NULL UNIQUE,
    Team_Size  INT          NOT NULL,
    Format     VARCHAR(200),
    Icon       VARCHAR(10)  DEFAULT '🏅',
    CONSTRAINT chk_team_size CHECK (Team_Size BETWEEN 1 AND 15)
);

INSERT INTO Sports (Sport_Name, Team_Size, Format, Icon) VALUES
('Cricket',    11, 'T20 format · Group Stage → Semi Finals → Final · DL method if rain', '🏏'),
('Football',   11, '90 min · Extra time in knockouts · Penalty shootout if level',        '⚽'),
('Basketball',  5, '4×10 min quarters · FIBA rules · Overtime if tied at full time',      '🏀');

-- ── TABLE 2: Venues ─────────────────────────────────────────
CREATE TABLE Venues (
    Venue_ID   INT AUTO_INCREMENT PRIMARY KEY,
    Venue_Name VARCHAR(100) NOT NULL UNIQUE,
    Location   VARCHAR(150) NOT NULL,
    Capacity   INT,
    Surface    VARCHAR(50)  DEFAULT 'Turf',
    CONSTRAINT chk_capacity CHECK (Capacity > 0)
);

INSERT INTO Venues (Venue_Name, Location, Capacity, Surface) VALUES
('SNU Cricket Ground',      'Block F, Shiv Nadar University, Greater Noida', 1200, 'Natural Grass'),
('SNU Football Ground',     'Block G, Shiv Nadar University, Greater Noida', 1500, 'Natural Grass'),
('SNU Basketball Court A',  'Indoor Sports Complex, SNU',                     600, 'Hardwood'),
('SNU Basketball Court B',  'Indoor Sports Complex, SNU',                     400, 'Hardwood'),
('SNU Main Arena',          'Main Arena Building, SNU',                       800, 'Mixed');

-- ── TABLE 3: Teams ──────────────────────────────────────────
CREATE TABLE Teams (
    Team_ID    INT AUTO_INCREMENT PRIMARY KEY,
    Team_Name  VARCHAR(100) NOT NULL,
    University VARCHAR(150) NOT NULL,
    Sport_ID   INT          NOT NULL,
    Coach_Name VARCHAR(100),
    Group_Name CHAR(1)      DEFAULT 'A',
    FOREIGN KEY (Sport_ID) REFERENCES Sports(Sport_ID),
    CONSTRAINT uq_team_sport UNIQUE (Team_Name, Sport_ID)
);

-- Cricket teams
INSERT INTO Teams (Team_Name, University, Sport_ID, Coach_Name, Group_Name) VALUES
('SNU Stallions',        'Shiv Nadar University',             1, 'Vikram Rathore',  'A'),
('JIIT Thunderbolts',    'JAYPEE Institute of IT, Noida',     1, 'Prashant Naik',   'A'),
('Amity Titans',         'Amity University, Noida',           1, 'Deepak Sharma',   'A'),
('GL Bajaj Chargers',    'GL Bajaj Institute, Greater Noida', 1, 'Rohit Verma',     'B'),
('Bennett Blazers',      'Bennett University, Greater Noida', 1, 'Anil Sood',       'B'),
('Galgotias Gladiators', 'Galgotias University',              1, 'Suresh Menon',    'B');

-- Football teams
INSERT INTO Teams (Team_Name, University, Sport_ID, Coach_Name, Group_Name) VALUES
('SNU FC',               'Shiv Nadar University',             2, 'Carlos Fernandez','A'),
('JIIT United',          'JAYPEE Institute of IT, Noida',     2, 'Ahmed Hussain',   'A'),
('Amity Athletic',       'Amity University, Noida',           2, 'Kiran Babu',      'A'),
('GL Bajaj FC',          'GL Bajaj Institute, Greater Noida', 2, 'Paulo Silva',     'B'),
('Bennett FC',           'Bennett University, Greater Noida', 2, 'Harsh Pathak',    'B'),
('Galgotias United',     'Galgotias University',              2, 'Marco Rossi',     'B');

-- Basketball teams
INSERT INTO Teams (Team_Name, University, Sport_ID, Coach_Name, Group_Name) VALUES
('SNU Hoopsters',        'Shiv Nadar University',             3, 'Dave Thompson',   'A'),
('JIIT Ballers',         'JAYPEE Institute of IT, Noida',     3, 'Naveen Gupta',    'A'),
('Amity Dunkers',        'Amity University, Noida',           3, 'Priya Sharma',    'A'),
('GL Bajaj Rockets',     'GL Bajaj Institute, Greater Noida', 3, 'Jason Lee',       'B'),
('Bennett Bulls',        'Bennett University, Greater Noida', 3, 'Rajesh Kumar',    'B'),
('Galgotias Raptors',    'Galgotias University',              3, 'Samuel Okafor',   'B');

-- ── TABLE 4: Players ────────────────────────────────────────
CREATE TABLE Players (
    Player_ID   INT AUTO_INCREMENT PRIMARY KEY,
    Player_Name VARCHAR(100) NOT NULL,
    Team_ID     INT          NOT NULL,
    Role        VARCHAR(60),
    Jersey_No   INT,
    Form_Status VARCHAR(20)  DEFAULT 'Neutral',
    FOREIGN KEY (Team_ID) REFERENCES Teams(Team_ID),
    CONSTRAINT chk_jersey      CHECK (Jersey_No BETWEEN 1 AND 99),
    CONSTRAINT uq_jersey_team  UNIQUE (Jersey_No, Team_ID)
);

-- ── CRICKET: SNU Stallions (Team 1) ─────────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No, Form_Status) VALUES
('Arjun Sharma',    1,'Batsman',        7, 'In Form'),
('Karan Mehta',     1,'All-rounder',   11, 'In Form'),
('Rohit Nair',      1,'Wicket-keeper',  5, 'Neutral'),
('Siddharth Rao',   1,'Fast Bowler',    9, 'Neutral'),
('Aakash Verma',    1,'Spinner',       13, 'Neutral'),
('Priyank Joshi',   1,'Batsman',       17, 'In Form'),
('Nikhil Patel',    1,'All-rounder',   21, 'Neutral'),
('Tushar Gupta',    1,'Fast Bowler',   25, 'Out of Form'),
('Manav Singh',     1,'Batsman',        3, 'Neutral'),
('Dev Chauhan',     1,'Spinner',       33, 'Neutral'),
('Yash Kumar',      1,'Batsman',        1, 'In Form');

-- ── CRICKET: JIIT Thunderbolts (Team 2) ─────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No, Form_Status) VALUES
('Rahul Dubey',     2,'Batsman',        7, 'In Form'),
('Mohit Sharma',    2,'Fast Bowler',   11, 'Neutral'),
('Arun Yadav',      2,'Wicket-keeper',  5, 'Neutral'),
('Kabir Singh',     2,'All-rounder',    9, 'In Form'),
('Tanmay Gupta',    2,'Spinner',       13, 'Neutral'),
('Lakshay Khanna',  2,'Batsman',       17, 'Neutral'),
('Vishal Mittal',   2,'Fast Bowler',   21, 'Neutral'),
('Hitesh Anand',    2,'Batsman',       25, 'In Form'),
('Sameer Walia',    2,'All-rounder',    3, 'Neutral'),
('Pranav Bhatia',   2,'Spinner',       33, 'Neutral'),
('Ujjwal Singh',    2,'Batsman',        1, 'Neutral');

-- ── CRICKET: Amity Titans (Team 3) ──────────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No, Form_Status) VALUES
('Aditya Saxena',   3,'Batsman',        7, 'Neutral'),
('Rishi Agarwal',   3,'Fast Bowler',   11, 'In Form'),
('Shiv Chauhan',    3,'Wicket-keeper',  5, 'Neutral'),
('Aman Tyagi',      3,'All-rounder',    9, 'Neutral'),
('Deepak Pandey',   3,'Spinner',       13, 'Neutral'),
('Harshal Jain',    3,'Batsman',       17, 'In Form'),
('Vinay Tripathi',  3,'Fast Bowler',   21, 'Neutral'),
('Sachin Rawat',    3,'Batsman',       25, 'Neutral'),
('Gaurav Thakur',   3,'All-rounder',    3, 'Neutral'),
('Ishan Goel',      3,'Spinner',       33, 'Neutral'),
('Vikas Bhatt',     3,'Batsman',        1, 'Neutral');

-- ── CRICKET: GL Bajaj Chargers (Team 4) ─────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No, Form_Status) VALUES
('Dhruv Agnihotri', 4,'Batsman',        7, 'In Form'),
('Parth Srivastava',4,'Fast Bowler',   11, 'Neutral'),
('Sumit Kaul',      4,'Wicket-keeper',  5, 'Neutral'),
('Abhijit Roy',     4,'All-rounder',    9, 'In Form'),
('Shubham Rana',    4,'Spinner',       13, 'Neutral'),
('Rajveer Gill',    4,'Batsman',       17, 'Neutral'),
('Kunal Sharma',    4,'Fast Bowler',   21, 'Neutral'),
('Harsh Puri',      4,'Batsman',       25, 'Neutral'),
('Aryan Malhotra',  4,'All-rounder',    3, 'Neutral'),
('Param Sethi',     4,'Spinner',       33, 'Neutral'),
('Nitin Kapoor',    4,'Batsman',        1, 'Neutral');

-- ── CRICKET: Bennett Blazers (Team 5) ───────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No, Form_Status) VALUES
('Vivek Narayan',   5,'Batsman',        7, 'Neutral'),
('Saurabh Kaushik', 5,'Fast Bowler',   11, 'In Form'),
('Mehul Joshi',     5,'Wicket-keeper',  5, 'Neutral'),
('Ankit Bajpai',    5,'All-rounder',    9, 'Neutral'),
('Rajeev Bhardwaj', 5,'Spinner',       13, 'Neutral'),
('Kartik Mathur',   5,'Batsman',       17, 'Neutral'),
('Divyam Tandon',   5,'Fast Bowler',   21, 'Neutral'),
('Alok Chauhan',    5,'Batsman',       25, 'Neutral'),
('Pratik Singh',    5,'All-rounder',    3, 'Neutral'),
('Manoj Kashyap',   5,'Spinner',       33, 'Neutral'),
('Vikrant Misra',   5,'Batsman',        1, 'Neutral');

-- ── CRICKET: Galgotias Gladiators (Team 6) ──────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No, Form_Status) VALUES
('Sanjay Rawat',    6,'Batsman',        7, 'Neutral'),
('Ashish Sehgal',   6,'Fast Bowler',   11, 'Neutral'),
('Nitin Dixit',     6,'Wicket-keeper',  5, 'Neutral'),
('Ratan Saini',     6,'All-rounder',    9, 'Neutral'),
('Piyush Dubey',    6,'Spinner',       13, 'In Form'),
('Rajesh Kumar',    6,'Batsman',       17, 'Neutral'),
('Naveen Tripathi', 6,'Fast Bowler',   21, 'Neutral'),
('Sudesh Pathak',   6,'Batsman',       25, 'Neutral'),
('Bhanu Pratap',    6,'All-rounder',    3, 'Neutral'),
('Manoj Yadav',     6,'Spinner',       33, 'Neutral'),
('Lokesh Misra',    6,'Batsman',        1, 'Neutral');

-- ── FOOTBALL: SNU FC (Team 7) ───────────────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Akash Mishra',     7,'Striker',     9),
('Siddharth Rajan',  7,'Midfielder',  8),
('Dev Patel',        7,'Goalkeeper',  1),
('Harsh Sharma',     7,'Defender',    4),
('Sumit Verma',      7,'Midfielder',  6),
('Aryan Thakur',     7,'Striker',    10),
('Nishant Anand',    7,'Defender',    5),
('Rahul Jha',        7,'Midfielder',  7),
('Vedant Bose',      7,'Defender',    3),
('Tanveer Hussain',  7,'Midfielder', 11),
('Krishank Arora',   7,'Striker',    19);

-- ── FOOTBALL: JIIT United (Team 8) ──────────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Rohan Dubey',      8,'Striker',     9),
('Ankush Garg',      8,'Midfielder',  8),
('Pankaj Nath',      8,'Goalkeeper',  1),
('Sahil Sharma',     8,'Defender',    4),
('Ravi Tiwari',      8,'Midfielder',  6),
('Manish Pal',       8,'Striker',    10),
('Vinit Srivastava', 8,'Defender',    5),
('Puneet Dhiman',    8,'Midfielder',  7),
('Rishab Goel',      8,'Defender',    3),
('Nikhil Rawat',     8,'Midfielder', 11),
('Amit Bhatia',      8,'Striker',    19);

-- ── FOOTBALL: Amity Athletic (Team 9) ───────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Sreejith Nair',    9,'Striker',     9),
('Akshay Reddy',     9,'Midfielder',  8),
('Rohit Thomas',     9,'Goalkeeper',  1),
('Divij Menon',      9,'Defender',    4),
('Siddhant Kumar',   9,'Midfielder',  6),
('Joel Mathew',      9,'Striker',    10),
('Rajan Pillai',     9,'Defender',    5),
('Francis George',   9,'Midfielder',  7),
('Kevin Joseph',     9,'Defender',    3),
('Binu Thomas',      9,'Midfielder', 11),
('Abel Simon',       9,'Striker',    19);

-- ── FOOTBALL: GL Bajaj FC (Team 10) ─────────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Gaurav Bajpai',   10,'Striker',     9),
('Ashish Rana',     10,'Midfielder',  8),
('Deepak Joshi',    10,'Goalkeeper',  1),
('Prateek Singh',   10,'Defender',    4),
('Vikas Garg',      10,'Midfielder',  6),
('Mohit Awasthi',   10,'Striker',    10),
('Suresh Verma',    10,'Defender',    5),
('Ajay Pandey',     10,'Midfielder',  7),
('Rakesh Yadav',    10,'Defender',    3),
('Sandeep Negi',    10,'Midfielder', 11),
('Tarun Gupta',     10,'Striker',    19);

-- ── FOOTBALL: Bennett FC (Team 11) ──────────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Dheeraj Malhotra',11,'Striker',     9),
('Kshitij Mittal',  11,'Midfielder',  8),
('Ritesh Sharma',   11,'Goalkeeper',  1),
('Anuj Verma',      11,'Defender',    4),
('Yuvraj Anand',    11,'Midfielder',  6),
('Parth Maheshwari',11,'Striker',    10),
('Rahul Bansal',    11,'Defender',    5),
('Ankur Kapoor',    11,'Midfielder',  7),
('Sahil Chaudhary', 11,'Defender',    3),
('Ritul Bose',      11,'Midfielder', 11),
('Mihir Jain',      11,'Striker',    19);

-- ── FOOTBALL: Galgotias United (Team 12) ────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Udit Sharma',     12,'Striker',     9),
('Saurabh Aggarwal',12,'Midfielder',  8),
('Prabhat Singh',   12,'Goalkeeper',  1),
('Karun Mehta',     12,'Defender',    4),
('Naveen Dubey',    12,'Midfielder',  6),
('Lakshit Gupta',   12,'Striker',    10),
('Manas Singh',     12,'Defender',    5),
('Anshul Rawat',    12,'Midfielder',  7),
('Nitesh Pal',      12,'Defender',    3),
('Siddhi Nath',     12,'Midfielder', 11),
('Arjit Pandey',    12,'Striker',    19);

-- ── BASKETBALL: SNU Hoopsters (Team 13) ─────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Jatin Bhasin',    13,'Point Guard',      5),
('Samar Preet',     13,'Shooting Guard',  11),
('Kabir Ahuja',     13,'Small Forward',   23),
('Devraj Sood',     13,'Power Forward',   32),
('Ankur Seth',      13,'Center',           4),
('Nihal Kapoor',    13,'Guard',           15),
('Vishal Puri',     13,'Forward',         33);

-- ── BASKETBALL: JIIT Ballers (Team 14) ──────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Preet Walia',     14,'Point Guard',      5),
('Rohit Mallik',    14,'Shooting Guard',  11),
('Arpit Tiwari',    14,'Small Forward',   23),
('Gaurav Diwan',    14,'Power Forward',   32),
('Sunny Bhatti',    14,'Center',           4),
('Rajan Mehta',     14,'Guard',           15),
('Vicky Rana',      14,'Forward',         33);

-- ── BASKETBALL: Amity Dunkers (Team 15) ─────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Ajinkya Patil',   15,'Point Guard',      5),
('Chetan Lokhande', 15,'Shooting Guard',  11),
('Rushikesh More',  15,'Small Forward',   23),
('Prathamesh Jadhav',15,'Power Forward',  32),
('Shreyas Kulkarni',15,'Center',           4),
('Omkar Deshmukh',  15,'Guard',           15),
('Tejas Bhosale',   15,'Forward',         33);

-- ── BASKETBALL: GL Bajaj Rockets (Team 16) ──────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Bhagwan Sahay',   16,'Point Guard',      5),
('Deepu Misra',     16,'Shooting Guard',  11),
('Saket Srivastava',16,'Small Forward',   23),
('Alok Trivedi',    16,'Power Forward',   32),
('Ashwin Shukla',   16,'Center',           4),
('Girish Pandey',   16,'Guard',           15),
('Mukund Yadav',    16,'Forward',         33);

-- ── BASKETBALL: Bennett Bulls (Team 17) ─────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Aditya Tandon',   17,'Point Guard',      5),
('Harsh Agarwal',   17,'Shooting Guard',  11),
('Nitin Sharma',    17,'Small Forward',   23),
('Saurabh Sharma',  17,'Power Forward',   32),
('Akash Garg',      17,'Center',           4),
('Ritesh Singh',    17,'Guard',           15),
('Sachin Tyagi',    17,'Forward',         33);

-- ── BASKETBALL: Galgotias Raptors (Team 18) ─────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Rahul Kashyap',   18,'Point Guard',      5),
('Prashant Ghosh',  18,'Shooting Guard',  11),
('Adarsh Negi',     18,'Small Forward',   23),
('Shantanu Roy',    18,'Power Forward',   32),
('Hemant Datta',    18,'Center',           4),
('Kunal Banerjee',  18,'Guard',           15),
('Ranit Mukherjee', 18,'Forward',         33);

-- ── TABLE 5: Matches ────────────────────────────────────────
CREATE TABLE Matches (
    Match_ID       INT AUTO_INCREMENT PRIMARY KEY,
    Sport_ID       INT  NOT NULL,
    Team_A_ID      INT  NOT NULL,
    Team_B_ID      INT  NOT NULL,
    Match_Date     DATE NOT NULL,
    Match_Time     TIME NOT NULL,
    Venue_ID       INT  NOT NULL,
    Stage          ENUM('Group Stage','Quarter-Final','Semi-Final','Final') DEFAULT 'Group Stage',
    Winner_Team_ID INT  DEFAULT NULL,
    Status         ENUM('Scheduled','Completed','Cancelled') DEFAULT 'Scheduled',
    FOREIGN KEY (Sport_ID)       REFERENCES Sports(Sport_ID),
    FOREIGN KEY (Team_A_ID)      REFERENCES Teams(Team_ID),
    FOREIGN KEY (Team_B_ID)      REFERENCES Teams(Team_ID),
    FOREIGN KEY (Venue_ID)       REFERENCES Venues(Venue_ID),
    FOREIGN KEY (Winner_Team_ID) REFERENCES Teams(Team_ID),
    CONSTRAINT chk_teams CHECK (Team_A_ID != Team_B_ID)
);

-- ── CRICKET MATCHES ─────────────────────────────────────────
INSERT INTO Matches (Sport_ID,Team_A_ID,Team_B_ID,Match_Date,Match_Time,Venue_ID,Stage,Winner_Team_ID,Status) VALUES
(1,1,2,'2025-02-14','09:00:00',1,'Group Stage',1,'Completed'),
(1,3,4,'2025-02-14','13:30:00',1,'Group Stage',3,'Completed'),
(1,5,6,'2025-02-15','09:00:00',1,'Group Stage',5,'Completed'),
(1,1,3,'2025-02-15','13:30:00',1,'Group Stage',1,'Completed'),
(1,2,4,'2025-02-16','09:00:00',1,'Group Stage',4,'Completed'),
(1,5,1,'2025-02-16','13:30:00',1,'Group Stage',1,'Completed'),
(1,3,6,'2025-02-17','09:00:00',1,'Group Stage',3,'Completed'),
(1,2,5,'2025-02-17','13:30:00',1,'Group Stage',5,'Completed'),
(1,1,4,'2025-02-18','09:00:00',1,'Semi-Final', 1,'Completed'),
(1,3,5,'2025-02-18','13:30:00',1,'Semi-Final', 3,'Completed'),
(1,1,3,'2025-02-20','11:00:00',1,'Final',      NULL,'Scheduled');

-- ── FOOTBALL MATCHES ────────────────────────────────────────
INSERT INTO Matches (Sport_ID,Team_A_ID,Team_B_ID,Match_Date,Match_Time,Venue_ID,Stage,Winner_Team_ID,Status) VALUES
(2, 7, 8,'2025-02-14','10:00:00',2,'Group Stage', 7,'Completed'),
(2, 9,10,'2025-02-14','14:00:00',2,'Group Stage', 9,'Completed'),
(2,11,12,'2025-02-15','10:00:00',2,'Group Stage',11,'Completed'),
(2, 7, 9,'2025-02-15','14:00:00',2,'Group Stage', 7,'Completed'),
(2, 8,10,'2025-02-16','10:00:00',2,'Group Stage',10,'Completed'),
(2,11, 7,'2025-02-16','14:00:00',2,'Group Stage', 7,'Completed'),
(2, 9,12,'2025-02-17','10:00:00',2,'Group Stage', 9,'Completed'),
(2, 7,10,'2025-02-18','10:00:00',2,'Semi-Final',  7,'Completed'),
(2, 9,11,'2025-02-18','14:00:00',2,'Semi-Final',  9,'Completed'),
(2, 7, 9,'2025-02-20','14:00:00',2,'Final',       NULL,'Scheduled');

-- ── BASKETBALL MATCHES ──────────────────────────────────────
INSERT INTO Matches (Sport_ID,Team_A_ID,Team_B_ID,Match_Date,Match_Time,Venue_ID,Stage,Winner_Team_ID,Status) VALUES
(3,13,14,'2025-02-14','11:00:00',3,'Group Stage',13,'Completed'),
(3,15,16,'2025-02-14','15:00:00',3,'Group Stage',15,'Completed'),
(3,17,18,'2025-02-15','11:00:00',3,'Group Stage',17,'Completed'),
(3,13,15,'2025-02-15','15:00:00',3,'Group Stage',13,'Completed'),
(3,14,16,'2025-02-16','11:00:00',3,'Group Stage',16,'Completed'),
(3,17,13,'2025-02-16','15:00:00',3,'Group Stage',13,'Completed'),
(3,15,18,'2025-02-17','11:00:00',3,'Group Stage',15,'Completed'),
(3,13,16,'2025-02-18','11:00:00',3,'Semi-Final', 13,'Completed'),
(3,15,17,'2025-02-18','15:00:00',3,'Semi-Final', 15,'Completed'),
(3,13,15,'2025-02-20','09:00:00',3,'Final',       NULL,'Scheduled');

-- ── TABLE 6: Scorecard_Cricket ──────────────────────────────
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
    CONSTRAINT chk_runs CHECK (Runs_Scored   >= 0),
    CONSTRAINT chk_wkts CHECK (Wickets_Taken BETWEEN 0 AND 10),
    CONSTRAINT chk_ovrs CHECK (Overs_Bowled  >= 0)
);

-- Match 1: SNU Stallions beat JIIT 174/6 vs 149
INSERT INTO Scorecard_Cricket (Match_ID,Player_ID,Runs_Scored,Wickets_Taken,Overs_Bowled,Catches) VALUES
(1, 1,68,0,0.0,1),(1, 2,22,2,4.0,0),(1, 3,15,0,0.0,1),(1, 4, 0,3,4.0,0),
(1, 5, 0,1,4.0,0),(1, 6,34,0,0.0,0),(1, 7,18,0,0.0,1),(1, 8, 0,0,4.0,0),
(1, 9, 7,0,0.0,0),(1,10, 0,0,4.0,1),(1,11,10,0,0.0,0),
(1,12,41,0,0.0,0),(1,13, 0,2,4.0,0),(1,14,28,0,0.0,0),(1,15, 0,2,4.0,0),
(1,16,18,0,0.0,0),(1,17,22,0,0.0,1),(1,18, 0,2,4.0,0),(1,19,12,0,0.0,0),
(1,20, 0,0,4.0,0),(1,21,15,0,0.0,0),(1,22,13,0,0.0,0);

-- Match 2: Amity Titans beat GL Bajaj 161 vs 138
INSERT INTO Scorecard_Cricket (Match_ID,Player_ID,Runs_Scored,Wickets_Taken,Overs_Bowled,Catches) VALUES
(2,23,55,0,0.0,0),(2,24, 0,2,4.0,0),(2,25,18,0,0.0,1),(2,26, 0,1,4.0,0),
(2,27, 0,2,4.0,0),(2,28,42,0,0.0,0),(2,29,30,0,0.0,0),(2,30, 0,0,4.0,0),
(2,31,16,0,0.0,0),(2,32, 0,0,4.0,1),(2,33, 0,0,0.0,0),
(2,34,33,0,0.0,0),(2,35, 0,2,4.0,0),(2,36,24,0,0.0,0),(2,37, 0,1,4.0,0),
(2,38,28,0,0.0,0),(2,39,15,0,0.0,1),(2,40, 0,2,4.0,0),(2,41,10,0,0.0,0),
(2,42, 0,0,4.0,0),(2,43,13,0,0.0,0),(2,44, 5,2,0.0,0);

-- Match 4: SNU beat Amity 188 vs 151
INSERT INTO Scorecard_Cricket (Match_ID,Player_ID,Runs_Scored,Wickets_Taken,Overs_Bowled,Catches) VALUES
(4, 1,82,0,0.0,1),(4, 2,35,1,4.0,0),(4, 6,54,0,0.0,0),(4, 4, 0,2,4.0,0),
(4, 5, 0,2,4.0,0),(4, 7,17,0,0.0,0),
(4,23,28,0,0.0,0),(4,24, 0,3,4.0,0),(4,28,36,0,0.0,0),(4,27, 0,1,4.0,0),(4,33,30,0,0.0,0);

-- Match 9 (Semi): SNU beat GL Bajaj 195 vs 142
INSERT INTO Scorecard_Cricket (Match_ID,Player_ID,Runs_Scored,Wickets_Taken,Overs_Bowled,Catches) VALUES
(9, 1,105,0,0.0,1),(9, 6, 61,0,0.0,0),(9, 2, 18,2,4.0,0),(9, 4,  0,3,3.0,0),
(9, 5,  0,2,4.0,0),(9,11, 11,0,0.0,0),
(9,34, 33,0,0.0,0),(9,35,  0,2,4.0,0),(9,36, 24,0,0.0,0),(9,37,  0,1,4.0,0),(9,38, 28,0,0.0,0);

-- Match 10 (Semi): Amity beat Bennett 168 vs 145
INSERT INTO Scorecard_Cricket (Match_ID,Player_ID,Runs_Scored,Wickets_Taken,Overs_Bowled,Catches) VALUES
(10,23,72,0,0.0,0),(10,28,48,0,0.0,0),(10,24, 0,3,4.0,0),(10,27, 0,2,4.0,0),(10,33,22,0,0.0,1),
(10,45,38,0,0.0,0),(10,46, 0,2,4.0,0),(10,49,36,0,0.0,0),(10,50, 0,1,4.0,0),(10,51,38,0,0.0,0),(10,52,20,0,0.0,0);

-- ── TABLE 7: Scorecard_Football ─────────────────────────────
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
    CONSTRAINT chk_goals CHECK (Goals        >= 0),
    CONSTRAINT chk_asst  CHECK (Assists      >= 0),
    CONSTRAINT chk_yc    CHECK (Yellow_Cards BETWEEN 0 AND 2),
    CONSTRAINT chk_rc    CHECK (Red_Cards    BETWEEN 0 AND 1)
);

-- Match 12: SNU FC 3-1 JIIT United
INSERT INTO Scorecard_Football (Match_ID,Player_ID,Goals,Assists,Yellow_Cards,Red_Cards) VALUES
(12,67,2,1,0,0),(12,72,1,0,1,0),(12,74,0,2,0,0),(12,76,0,0,1,0),(12,77,0,1,0,0),
(12,78,1,0,0,0),(12,79,0,1,1,0),(12,82,0,0,1,0);

-- Match 13: Amity 2-0 GL Bajaj
INSERT INTO Scorecard_Football (Match_ID,Player_ID,Goals,Assists,Yellow_Cards,Red_Cards) VALUES
(13,89,1,1,0,0),(13,94,1,0,0,0),(13,90,0,1,1,0),(13,100,0,0,1,0);

-- Match 14: Bennett 1-0 Galgotias
INSERT INTO Scorecard_Football (Match_ID,Player_ID,Goals,Assists,Yellow_Cards,Red_Cards) VALUES
(14,112,1,0,0,0),(14,115,0,1,1,0),(14,123,0,0,0,0),(14,120,0,0,1,0);

-- Match 15: SNU 2-1 Amity
INSERT INTO Scorecard_Football (Match_ID,Player_ID,Goals,Assists,Yellow_Cards,Red_Cards) VALUES
(15,67,1,0,0,0),(15,72,1,1,0,0),(15,74,0,1,1,0),
(15,89,1,0,1,0),(15,94,0,1,1,0),(15,90,0,0,1,0);

-- Match 16: GL Bajaj 2-0 JIIT United
INSERT INTO Scorecard_Football (Match_ID,Player_ID,Goals,Assists,Yellow_Cards,Red_Cards) VALUES
(16,100,1,1,0,0),(16,101,1,0,0,0),(16,78,0,0,1,0),(16,80,0,0,0,0);

-- Match 17: SNU 3-0 Bennett FC (Group Stage)
INSERT INTO Scorecard_Football (Match_ID,Player_ID,Goals,Assists,Yellow_Cards,Red_Cards) VALUES
(17,67,2,0,0,0),(17,72,1,1,0,0),(17,77,0,2,0,0),(17,74,0,0,1,0),(17,112,0,0,1,0),(17,115,0,0,2,0);

-- Match 20 (Semi): Amity 2-1 Bennett FC
INSERT INTO Scorecard_Football (Match_ID,Player_ID,Goals,Assists,Yellow_Cards,Red_Cards) VALUES
(20,89,2,0,0,0),(20,94,0,1,0,0),(20,90,0,1,1,0),(20,112,1,0,0,0),(20,115,0,1,1,0);

-- ── TABLE 8: Scorecard_Basketball ───────────────────────────
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
    CONSTRAINT chk_pts CHECK (Points   >= 0),
    CONSTRAINT chk_reb CHECK (Rebounds >= 0)
);

-- Match 22: SNU 78-61 JIIT
INSERT INTO Scorecard_Basketball (Match_ID,Player_ID,Points,Rebounds,Assists,Steals) VALUES
(22,133,24,5,8,3),(22,134,18,7,3,1),(22,135,14,9,2,2),(22,136, 8,11,1,0),(22,137,14,3,5,2),
(22,140,18,4,7,2),(22,141,15,6,2,1),(22,142,12,8,1,1),(22,143, 9,5,4,1),(22,144, 7,3,3,2);

-- Match 23: Amity 65-54 GL Bajaj
INSERT INTO Scorecard_Basketball (Match_ID,Player_ID,Points,Rebounds,Assists,Steals) VALUES
(23,147,22,4,9,2),(23,148,16,8,3,1),(23,149,12,7,2,2),(23,150, 7,12,1,0),(23,151, 8,3,4,2),
(23,154,14,5,6,1),(23,155,13,8,2,1),(23,156,11,9,2,2),(23,157, 9,4,3,1),(23,158, 7,2,2,1);

-- Match 25: SNU 82-70 Amity
INSERT INTO Scorecard_Basketball (Match_ID,Player_ID,Points,Rebounds,Assists,Steals) VALUES
(25,133,28,6,9,4),(25,134,22,8,4,2),(25,135,16,10,3,1),(25,136,10,12,1,0),(25,137, 6,4,5,2),
(25,147,25,5,8,2),(25,148,18,9,3,1),(25,149,14,8,2,1),(25,150, 8,11,1,0),(25,151, 5,2,4,1);

-- Match 29 (Semi): SNU 74-62 GL Bajaj
INSERT INTO Scorecard_Basketball (Match_ID,Player_ID,Points,Rebounds,Assists,Steals) VALUES
(29,133,26,7,10,3),(29,134,20,8,4,2),(29,135,16,9,2,1),(29,136, 6,10,1,0),(29,137, 6,4,5,1),
(29,154,14,5,6,1),(29,155,18,8,3,1),(29,156,14,9,2,1),(29,157, 9,11,2,0),(29,158, 7,3,2,1);

-- Match 30 (Semi): Amity 68-65 Bennett
INSERT INTO Scorecard_Basketball (Match_ID,Player_ID,Points,Rebounds,Assists,Steals) VALUES
(30,147,29,5,8,2),(30,148,20,9,3,1),(30,149,12,8,2,1),(30,150, 7,11,1,0),(30,151, 0,2,2,0),
(30,161,22,6,6,2),(30,162,18,8,3,1),(30,163,14,9,2,1),(30,164, 7,10,2,0),(30,165, 4,3,3,1);

-- ── TABLE 9: Users ───────────────────────────────────────────
CREATE TABLE Users (
    User_ID    INT AUTO_INCREMENT PRIMARY KEY,
    Username   VARCHAR(50)  NOT NULL UNIQUE,
    Password   VARCHAR(255) NOT NULL,
    Role       ENUM('admin','organiser','manager','viewer') DEFAULT 'viewer',
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO Users (Username, Password, Role) VALUES
('admin',      'arena@admin123', 'admin'),
('mudit',      'mudit123',       'admin'),
('organiser1', 'org@123',        'organiser'),
('manager1',   'manage123',      'manager'),
('viewer1',    'view123',        'viewer');

-- ── TABLE 10: Audit_Log ─────────────────────────────────────
CREATE TABLE Audit_Log (
    Log_ID     INT AUTO_INCREMENT PRIMARY KEY,
    Table_Name VARCHAR(50)  NOT NULL,
    Operation  ENUM('INSERT','UPDATE','DELETE') NOT NULL,
    Record_ID  INT,
    Changed_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Changed_By VARCHAR(50)  DEFAULT NULL,
    Old_Value  TEXT,
    New_Value  TEXT
);

-- ── TABLE 11: Predictions ───────────────────────────────────
CREATE TABLE Predictions (
    Pred_ID         INT AUTO_INCREMENT PRIMARY KEY,
    Player_ID       INT NOT NULL,
    Sport_Name      VARCHAR(50),
    Predicted_Score DECIMAL(10,2),
    Predicted_At    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Player_ID) REFERENCES Players(Player_ID)
);

-- ── INDEXES ─────────────────────────────────────────────────
CREATE INDEX idx_matches_date      ON Matches(Match_Date);
CREATE INDEX idx_matches_sport     ON Matches(Sport_ID);
CREATE INDEX idx_matches_status    ON Matches(Status);
CREATE INDEX idx_players_team      ON Players(Team_ID);
CREATE INDEX idx_cricket_player    ON Scorecard_Cricket(Player_ID);
CREATE INDEX idx_football_player   ON Scorecard_Football(Player_ID);
CREATE INDEX idx_basketball_player ON Scorecard_Basketball(Player_ID);
CREATE INDEX idx_audit_changed     ON Audit_Log(Changed_At);

SELECT 'ARENA_SNU v7 base setup complete! Run advanced_queries.sql next.' AS Status;
SELECT CONCAT('Teams inserted: ',   COUNT(*)) AS Info FROM Teams;
SELECT CONCAT('Players inserted: ', COUNT(*)) AS Info FROM Players;
SELECT CONCAT('Matches inserted: ', COUNT(*)) AS Info FROM Matches;