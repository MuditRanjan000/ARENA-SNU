-- ============================================================
--  ARENA SNU v6 — Complete Database Setup
--  SURGE 2025 Sports Festival · Shiv Nadar University
--  System Architect: Mudit | Run this FIRST
-- ============================================================

DROP DATABASE IF EXISTS ARENA_SNU;
CREATE DATABASE ARENA_SNU CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ARENA_SNU;

-- ── TABLE 1: Sports ─────────────────────────────────────────
CREATE TABLE Sports (
    Sport_ID   INT AUTO_INCREMENT PRIMARY KEY,
    Sport_Name VARCHAR(50) NOT NULL UNIQUE,
    Team_Size  INT NOT NULL,
    Format     VARCHAR(200),
    Icon       VARCHAR(10) DEFAULT '🏅',
    CONSTRAINT chk_team_size CHECK (Team_Size BETWEEN 1 AND 15)
);

INSERT INTO Sports (Sport_Name, Team_Size, Format, Icon) VALUES
('Cricket',    11, 'T20 format · Group Stage → Knockouts · DL method if rain', '🏏'),
('Football',   11, '90 min · Extra time in knockouts · Penalty shootout if level', '⚽'),
('Basketball',  5, '4×10 min quarters · FIBA rules · Overtime if tied', '🏀'),
('Badminton',   2, 'Best of 3 sets · 21 points · Singles + Doubles categories', '🏸'),
('Table Tennis',1, 'Best of 5 games · 11 points per game · Singles round-robin', '🏓'),
('Volleyball',  6, 'Best of 5 sets · 25 points · Rally scoring', '🏐');

-- ── TABLE 2: Venues ─────────────────────────────────────────
CREATE TABLE Venues (
    Venue_ID   INT AUTO_INCREMENT PRIMARY KEY,
    Venue_Name VARCHAR(100) NOT NULL UNIQUE,
    Location   VARCHAR(150) NOT NULL,
    Capacity   INT,
    Surface    VARCHAR(50) DEFAULT 'Turf',
    CONSTRAINT chk_capacity CHECK (Capacity > 0)
);

INSERT INTO Venues (Venue_Name, Location, Capacity, Surface) VALUES
('SNU Cricket Ground',          'Block F, Shiv Nadar University, Greater Noida', 1200, 'Natural Grass'),
('SNU Football Ground',         'Block G, Shiv Nadar University, Greater Noida', 1500, 'Natural Grass'),
('SNU Basketball Court A',      'Indoor Sports Complex, SNU',                     600, 'Hardwood'),
('SNU Basketball Court B',      'Indoor Sports Complex, SNU',                     400, 'Hardwood'),
('SNU Badminton Hall',          'Indoor Sports Complex, SNU',                     300, 'Wooden'),
('SNU Table Tennis Arena',      'Indoor Sports Complex, SNU',                     200, 'Composite'),
('SNU Volleyball Court',        'Block H Open Courts, SNU',                       500, 'Sand/Grass'),
('SNU Indoor Sports Complex',   'Main Arena Building, SNU',                       800, 'Mixed');

-- ── TABLE 3: Teams ─────────────────────────────────────────
CREATE TABLE Teams (
    Team_ID    INT AUTO_INCREMENT PRIMARY KEY,
    Team_Name  VARCHAR(100) NOT NULL,
    University VARCHAR(150) NOT NULL,
    Sport_ID   INT NOT NULL,
    Coach_Name VARCHAR(100),
    Group_Name VARCHAR(10) DEFAULT 'A',
    FOREIGN KEY (Sport_ID) REFERENCES Sports(Sport_ID),
    CONSTRAINT uq_team_sport UNIQUE (Team_Name, Sport_ID)
);

-- ── CRICKET TEAMS (SURGE 2025) ──────────────────────────────
INSERT INTO Teams (Team_Name, University, Sport_ID, Coach_Name, Group_Name) VALUES
('SNU Stallions',        'Shiv Nadar University',          1, 'Vikram Rathore',   'A'),
('JIIT Thunderbolts',    'JAYPEE Institute of IT, Noida',  1, 'Prashant Naik',    'A'),
('Amity Titans',         'Amity University, Noida',        1, 'Deepak Sharma',    'A'),
('GL Bajaj Chargers',    'GL Bajaj Institute, Gr. Noida',  1, 'Rohit Verma',      'B'),
('Bennett Blazers',      'Bennett University, Gr. Noida',  1, 'Anil Kumble Jr',   'B'),
('Galgotias Gladiators', 'Galgotias University, Gr. Noida',1, 'Suresh Menon',     'B'),
('NIET Knights',         'NIET, Gr. Noida',                1, 'Ramesh Poonia',    'C'),
('ShardaStrikes',        'Sharda University, Gr. Noida',   1, 'Manish Rana',      'C');

-- ── FOOTBALL TEAMS ───────────────────────────────────────────
INSERT INTO Teams (Team_Name, University, Sport_ID, Coach_Name, Group_Name) VALUES
('SNU FC',               'Shiv Nadar University',          2, 'Carlos Fernandez',  'A'),
('JIIT United',          'JAYPEE Institute of IT, Noida',  2, 'Ahmed Hussain',     'A'),
('Amity Athletic',       'Amity University, Noida',        2, 'Kiran Babu',        'A'),
('GL Bajaj FC',          'GL Bajaj Institute, Gr. Noida',  2, 'Paulo Silva',       'B'),
('Bennett FC',           'Bennett University, Gr. Noida',  2, 'Harsh Pathak',      'B'),
('Galgotias United',     'Galgotias University, Gr. Noida',2, 'Marco Rossi',       'B');

-- ── BASKETBALL TEAMS ──────────────────────────────────────────
INSERT INTO Teams (Team_Name, University, Sport_ID, Coach_Name, Group_Name) VALUES
('SNU Hoopsters',        'Shiv Nadar University',          3, 'Dave Thompson',     'A'),
('JIIT Ballers',         'JAYPEE Institute of IT, Noida',  3, 'Naveen Gupta',      'A'),
('Amity Dunkers',        'Amity University, Noida',        3, 'Priya Sharma',      'A'),
('GL Bajaj Rockets',     'GL Bajaj Institute, Gr. Noida',  3, 'Jason Lee',         'B'),
('Bennett Bulls',        'Bennett University, Gr. Noida',  3, 'Rajesh Kumar',      'B'),
('Galgotias Raptors',    'Galgotias University, Gr. Noida',3, 'Samuel Okafor',     'B');

-- ── BADMINTON TEAMS ────────────────────────────────────────────
INSERT INTO Teams (Team_Name, University, Sport_ID, Coach_Name, Group_Name) VALUES
('SNU Smashers',         'Shiv Nadar University',          4, 'Lin Wei',           'A'),
('JIIT Shuttlers',       'JAYPEE Institute of IT, Noida',  4, 'Anand Prakash',     'A'),
('Amity Aces',           'Amity University, Noida',        4, 'Kavita Rao',        'B'),
('GL Bajaj Feathers',    'GL Bajaj Institute, Gr. Noida',  4, 'Deepak Nair',       'B'),
('Bennett Birdie',       'Bennett University, Gr. Noida',  4, 'Swati Mishra',      'A'),
('Galgotias Smash',      'Galgotias University, Gr. Noida',4, 'Arun Khanna',       'B');

-- ── TABLE TENNIS TEAMS ────────────────────────────────────────
INSERT INTO Teams (Team_Name, University, Sport_ID, Coach_Name, Group_Name) VALUES
('SNU Spin Masters',     'Shiv Nadar University',          5, 'Zhang Wei',         'A'),
('JIIT Paddlers',        'JAYPEE Institute of IT, Noida',  5, 'Rahul Singh',       'A'),
('Amity Spinners',       'Amity University, Noida',        5, 'Nisha Joshi',       'B'),
('GL Bajaj Pingsters',   'GL Bajaj Institute, Gr. Noida',  5, 'Mukesh Yadav',      'B'),
('Bennett Slammers',     'Bennett University, Gr. Noida',  5, 'Pooja Nair',        'A'),
('Galgotias TT',         'Galgotias University, Gr. Noida',5, 'Sunil Mehta',       'B');

-- ── VOLLEYBALL TEAMS ──────────────────────────────────────────
INSERT INTO Teams (Team_Name, University, Sport_ID, Coach_Name, Group_Name) VALUES
('SNU Spikers',          'Shiv Nadar University',          6, 'Mikhail Petrov',    'A'),
('JIIT Servers',         'JAYPEE Institute of IT, Noida',  6, 'Vijay Tomar',       'A'),
('Amity Aces VB',        'Amity University, Noida',        6, 'Sunita Reddy',      'B'),
('GL Bajaj Setters',     'GL Bajaj Institute, Gr. Noida',  6, 'Arjun Desai',       'B'),
('Bennett Blockers',     'Bennett University, Gr. Noida',  6, 'Priyanka Sharma',   'A'),
('Galgotias Smashers',   'Galgotias University, Gr. Noida',6, 'Ravi Kumar',        'B');

-- ── TABLE 4: Players ──────────────────────────────────────────
CREATE TABLE Players (
    Player_ID   INT AUTO_INCREMENT PRIMARY KEY,
    Player_Name VARCHAR(100) NOT NULL,
    Team_ID     INT NOT NULL,
    Role        VARCHAR(60),
    Jersey_No   INT,
    Form_Status VARCHAR(20) DEFAULT 'Neutral',
    FOREIGN KEY (Team_ID) REFERENCES Teams(Team_ID),
    CONSTRAINT chk_jersey CHECK (Jersey_No BETWEEN 1 AND 99),
    CONSTRAINT uq_jersey_team UNIQUE (Jersey_No, Team_ID)
);

-- ── CRICKET PLAYERS — SNU Stallions ────────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No, Form_Status) VALUES
('Arjun Sharma',       1, 'Batsman',         7,  'In Form'),
('Karan Mehta',        1, 'All-rounder',      11, 'In Form'),
('Rohit Nair',         1, 'Wicket-keeper',    5,  'Neutral'),
('Siddharth Rao',      1, 'Fast Bowler',      9,  'Neutral'),
('Aakash Verma',       1, 'Spinner',          13, 'Neutral'),
('Priyank Joshi',      1, 'Batsman',          17, 'In Form'),
('Nikhil Patel',       1, 'All-rounder',      21, 'Neutral'),
('Tushar Gupta',       1, 'Fast Bowler',      25, 'Out of Form'),
('Manav Singh',        1, 'Batsman',          3,  'Neutral'),
('Dev Chauhan',        1, 'Spinner',          33, 'Neutral'),
('Yash Kumar',         1, 'Batsman',          1,  'In Form');

-- ── CRICKET PLAYERS — JIIT Thunderbolts ───────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No, Form_Status) VALUES
('Rahul Dubey',        2, 'Batsman',         7,  'In Form'),
('Mohit Sharma',       2, 'Fast Bowler',      11, 'Neutral'),
('Arun Yadav',         2, 'Wicket-keeper',    5,  'Neutral'),
('Kabir Singh',        2, 'All-rounder',      9,  'In Form'),
('Tanmay Gupta',       2, 'Spinner',          13, 'Neutral'),
('Lakshay Khanna',     2, 'Batsman',          17, 'Neutral'),
('Vishal Mittal',      2, 'Fast Bowler',      21, 'Neutral'),
('Hitesh Anand',       2, 'Batsman',          25, 'In Form'),
('Sameer Walia',       2, 'All-rounder',      3,  'Neutral'),
('Pranav Bhatia',      2, 'Spinner',          33, 'Neutral'),
('Ujjwal Singh',       2, 'Batsman',          1,  'Neutral');

-- ── CRICKET PLAYERS — Amity Titans ──────────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No, Form_Status) VALUES
('Aditya Saxena',      3, 'Batsman',         7,  'Neutral'),
('Rishi Agarwal',      3, 'Fast Bowler',      11, 'In Form'),
('Shiv Chauhan',       3, 'Wicket-keeper',    5,  'Neutral'),
('Aman Tyagi',         3, 'All-rounder',      9,  'Neutral'),
('Deepak Pandey',      3, 'Spinner',          13, 'Neutral'),
('Harshal Jain',       3, 'Batsman',          17, 'In Form'),
('Vinay Tripathi',     3, 'Fast Bowler',      21, 'Neutral'),
('Sachin Rawat',       3, 'Batsman',          25, 'Neutral'),
('Gaurav Thakur',      3, 'All-rounder',      3,  'Neutral'),
('Ishan Goel',         3, 'Spinner',          33, 'Neutral'),
('Vikas Bhatt',        3, 'Batsman',          1,  'Neutral');

-- ── CRICKET PLAYERS — GL Bajaj Chargers ─────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No, Form_Status) VALUES
('Dhruv Agnihotri',    4, 'Batsman',         7,  'In Form'),
('Parth Srivastava',   4, 'Fast Bowler',      11, 'Neutral'),
('Sumit Kaul',         4, 'Wicket-keeper',    5,  'Neutral'),
('Abhijit Roy',        4, 'All-rounder',      9,  'In Form'),
('Shubham Rana',       4, 'Spinner',          13, 'Neutral'),
('Rajveer Gill',       4, 'Batsman',          17, 'Neutral'),
('Kunal Sharma',       4, 'Fast Bowler',      21, 'Neutral'),
('Harsh Puri',         4, 'Batsman',          25, 'Neutral'),
('Aryan Malhotra',     4, 'All-rounder',      3,  'Neutral'),
('Param Sethi',        4, 'Spinner',          33, 'Neutral'),
('Nitin Kapoor',       4, 'Batsman',          1,  'Neutral');

-- ── CRICKET PLAYERS — Bennett Blazers ────────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No, Form_Status) VALUES
('Vivek Narayan',      5, 'Batsman',         7,  'Neutral'),
('Saurabh Kaushik',    5, 'Fast Bowler',      11, 'In Form'),
('Mehul Joshi',        5, 'Wicket-keeper',    5,  'Neutral'),
('Ankit Bajpai',       5, 'All-rounder',      9,  'Neutral'),
('Rajeev Bhardwaj',    5, 'Spinner',          13, 'Neutral'),
('Kartik Mathur',      5, 'Batsman',          17, 'Neutral'),
('Divyam Tandon',      5, 'Fast Bowler',      21, 'Neutral'),
('Alok Chauhan',       5, 'Batsman',          25, 'Neutral'),
('Pratik Singh',       5, 'All-rounder',      3,  'Neutral'),
('Manoj Kashyap',      5, 'Spinner',          33, 'Neutral'),
('Vikrant Misra',      5, 'Batsman',          1,  'Neutral');

-- ── CRICKET PLAYERS — Galgotias Gladiators ───────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No, Form_Status) VALUES
('Sanjay Rawat',       6, 'Batsman',         7,  'Neutral'),
('Ashish Sehgal',      6, 'Fast Bowler',      11, 'Neutral'),
('Nitin Dixit',        6, 'Wicket-keeper',    5,  'Neutral'),
('Ratan Saini',        6, 'All-rounder',      9,  'Neutral'),
('Piyush Dubey',       6, 'Spinner',          13, 'In Form'),
('Rajesh Kumar',       6, 'Batsman',          17, 'Neutral'),
('Naveen Tripathi',    6, 'Fast Bowler',      21, 'Neutral'),
('Sudesh Pathak',      6, 'Batsman',          25, 'Neutral'),
('Bhanu Pratap',       6, 'All-rounder',      3,  'Neutral'),
('Manoj Yadav',        6, 'Spinner',          33, 'Neutral'),
('Lokesh Misra',       6, 'Batsman',          1,  'Neutral');

-- ── CRICKET PLAYERS — NIET Knights ───────────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No, Form_Status) VALUES
('Akash Tiwari',       7, 'Batsman',         7,  'Neutral'),
('Prashant Vimal',     7, 'Fast Bowler',      11, 'Neutral'),
('Vinod Yadav',        7, 'Wicket-keeper',    5,  'Neutral'),
('Sachin Choudhury',   7, 'All-rounder',      9,  'Neutral'),
('Pradeep Bhatia',     7, 'Spinner',          13, 'Neutral'),
('Aashish Tomar',      7, 'Batsman',          17, 'Neutral'),
('Rohit Bansal',       7, 'Fast Bowler',      21, 'Neutral'),
('Sunil Negi',         7, 'Batsman',          25, 'Neutral'),
('Dheeraj Pawar',      7, 'All-rounder',      3,  'Neutral'),
('Vijay Bhardwaj',     7, 'Spinner',          33, 'Neutral'),
('Tarun Rawat',        7, 'Batsman',          1,  'Neutral');

-- ── CRICKET PLAYERS — ShardaStrikes ────────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No, Form_Status) VALUES
('Anand Trivedi',      8, 'Batsman',         7,  'Neutral'),
('Suman Das',          8, 'Fast Bowler',      11, 'Neutral'),
('Bipin Roy',          8, 'Wicket-keeper',    5,  'Neutral'),
('Jaydeep Shah',       8, 'All-rounder',      9,  'Neutral'),
('Mitesh Patel',       8, 'Spinner',          13, 'Neutral'),
('Parag Modi',         8, 'Batsman',          17, 'Neutral'),
('Nilesh Solanki',     8, 'Fast Bowler',      21, 'Neutral'),
('Varun Joshi',        8, 'Batsman',          25, 'Neutral'),
('Krish Mehta',        8, 'All-rounder',      3,  'Neutral'),
('Raj Trivedi',        8, 'Spinner',          33, 'Neutral'),
('Jeet Shah',          8, 'Batsman',          1,  'Neutral');

-- ── FOOTBALL PLAYERS — SNU FC ───────────────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Akash Mishra',       9,  'Striker',         9),
('Siddharth Rajan',    9,  'Midfielder',      8),
('Dev Patel',          9,  'Goalkeeper',      1),
('Harsh Sharma',       9,  'Defender',        4),
('Sumit Verma',        9,  'Midfielder',      6),
('Aryan Thakur',       9,  'Striker',         10),
('Nishant Anand',      9,  'Defender',        5),
('Rahul Jha',          9,  'Midfielder',      7),
('Vedant Bose',        9,  'Defender',        3),
('Tanveer Hussain',    9,  'Midfielder',      11),
('Krishank Arora',     9,  'Striker',         19);

-- ── FOOTBALL PLAYERS — JIIT United ──────────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Rohan Dubey',        10, 'Striker',         9),
('Ankush Garg',        10, 'Midfielder',      8),
('Pankaj Nath',        10, 'Goalkeeper',      1),
('Sahil Sharma',       10, 'Defender',        4),
('Ravi Tiwari',        10, 'Midfielder',      6),
('Manish Pal',         10, 'Striker',         10),
('Vinit Srivastava',   10, 'Defender',        5),
('Puneet Dhiman',      10, 'Midfielder',      7),
('Rishab Goel',        10, 'Defender',        3),
('Nikhil Rawat',       10, 'Midfielder',      11),
('Amit Bhatia',        10, 'Striker',         19);

-- ── FOOTBALL PLAYERS — Amity Athletic ───────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Sreejith Nair',      11, 'Striker',         9),
('Akshay Reddy',       11, 'Midfielder',      8),
('Rohit Thomas',       11, 'Goalkeeper',      1),
('Divij Menon',        11, 'Defender',        4),
('Siddhant Kumar',     11, 'Midfielder',      6),
('Joel Mathew',        11, 'Striker',         10),
('Rajan Pillai',       11, 'Defender',        5),
('Francis George',     11, 'Midfielder',      7),
('Kevin Joseph',       11, 'Defender',        3),
('Binu Thomas',        11, 'Midfielder',      11),
('Abel Simon',         11, 'Striker',         19);

-- ── FOOTBALL PLAYERS — GL Bajaj FC ──────────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Gaurav Bajpai',      12, 'Striker',         9),
('Ashish Rana',        12, 'Midfielder',      8),
('Deepak Joshi',       12, 'Goalkeeper',      1),
('Prateek Singh',      12, 'Defender',        4),
('Vikas Garg',         12, 'Midfielder',      6),
('Mohit Awasthi',      12, 'Striker',         10),
('Suresh Verma',       12, 'Defender',        5),
('Ajay Pandey',        12, 'Midfielder',      7),
('Rakesh Yadav',       12, 'Defender',        3),
('Sandeep Negi',       12, 'Midfielder',      11),
('Tarun Gupta',        12, 'Striker',         19);

-- ── FOOTBALL PLAYERS — Bennett FC ───────────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Dheeraj Malhotra',   13, 'Striker',         9),
('Kshitij Mittal',     13, 'Midfielder',      8),
('Ritesh Sharma',      13, 'Goalkeeper',      1),
('Anuj Verma',         13, 'Defender',        4),
('Yuvraj Anand',       13, 'Midfielder',      6),
('Parth Maheshwari',   13, 'Striker',         10),
('Rahul Bansal',       13, 'Defender',        5),
('Ankur Kapoor',       13, 'Midfielder',      7),
('Sahil Chaudhary',    13, 'Defender',        3),
('Ritul Bose',         13, 'Midfielder',      11),
('Mihir Jain',         13, 'Striker',         19);

-- ── FOOTBALL PLAYERS — Galgotias United ─────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Udit Sharma',        14, 'Striker',         9),
('Saurabh Aggarwal',   14, 'Midfielder',      8),
('Prabhat Singh',      14, 'Goalkeeper',      1),
('Karun Mehta',        14, 'Defender',        4),
('Naveen Dubey',       14, 'Midfielder',      6),
('Lakshit Gupta',      14, 'Striker',         10),
('Manas Singh',        14, 'Defender',        5),
('Anshul Rawat',       14, 'Midfielder',      7),
('Nitesh Pal',         14, 'Defender',        3),
('Siddhi Nath',        14, 'Midfielder',      11),
('Arjit Pandey',       14, 'Striker',         19);

-- ── BASKETBALL PLAYERS — SNU Hoopsters ──────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Jatin Bhasin',       15, 'Point Guard',      5),
('Samar Preet',        15, 'Shooting Guard',  11),
('Kabir Ahuja',        15, 'Small Forward',   23),
('Devraj Sood',        15, 'Power Forward',   32),
('Ankur Seth',         15, 'Center',           4),
('Nihal Kapoor',       15, 'Guard',           15),
('Vishal Puri',        15, 'Forward',         33);

-- ── BASKETBALL PLAYERS — JIIT Ballers ───────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Preet Walia',        16, 'Point Guard',      5),
('Rohit Mallik',       16, 'Shooting Guard',  11),
('Arpit Tiwari',       16, 'Small Forward',   23),
('Gaurav Diwan',       16, 'Power Forward',   32),
('Sunny Bhatti',       16, 'Center',           4),
('Rajan Mehta',        16, 'Guard',           15),
('Vicky Rana',         16, 'Forward',         33);

-- ── BASKETBALL PLAYERS — Amity Dunkers ──────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Ajinkya Patil',      17, 'Point Guard',      5),
('Chetan Lokhande',    17, 'Shooting Guard',  11),
('Rushikesh More',     17, 'Small Forward',   23),
('Prathamesh Jadhav',  17, 'Power Forward',   32),
('Shreyas Kulkarni',   17, 'Center',           4),
('Omkar Deshmukh',     17, 'Guard',           15),
('Tejas Bhosale',      17, 'Forward',         33);

-- ── BASKETBALL PLAYERS — GL Bajaj Rockets ──────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Bhagwan Sahay',      18, 'Point Guard',      5),
('Deepu Misra',        18, 'Shooting Guard',  11),
('Saket Srivastava',   18, 'Small Forward',   23),
('Alok Trivedi',       18, 'Power Forward',   32),
('Ashwin Shukla',      18, 'Center',           4),
('Girish Pandey',      18, 'Guard',           15),
('Mukund Yadav',       18, 'Forward',         33);

-- ── BASKETBALL PLAYERS — Bennett Bulls ──────────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Aditya Tandon',      19, 'Point Guard',      5),
('Harsh Agarwal',      19, 'Shooting Guard',  11),
('Nitin Sharma',       19, 'Small Forward',   23),
('Saurabh Sharma',     19, 'Power Forward',   32),
('Akash Garg',         19, 'Center',           4),
('Ritesh Singh',       19, 'Guard',           15),
('Sachin Tyagi',       19, 'Forward',         33);

-- ── BASKETBALL PLAYERS — Galgotias Raptors ───────────────────
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Rahul Kashyap',      20, 'Point Guard',      5),
('Prashant Ghosh',     20, 'Shooting Guard',  11),
('Adarsh Negi',        20, 'Small Forward',   23),
('Shantanu Roy',       20, 'Power Forward',   32),
('Hemant Datta',       20, 'Center',           4),
('Kunal Banerjee',     20, 'Guard',           15),
('Ranit Mukherjee',    20, 'Forward',         33);

-- ── BADMINTON PLAYERS ───────────────────────────────────────
-- SNU Smashers (Team 21)
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Ananya Joshi',       21, 'Singles',          1),
('Nikhil Arora',       21, 'Doubles',          2),
('Sneha Garg',         21, 'Doubles',          3),
('Aditya Kumar',       21, 'Singles',          4);

-- JIIT Shuttlers (Team 22)
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Riya Sharma',        22, 'Singles',          1),
('Kartik Bhatia',      22, 'Doubles',          2),
('Meera Saxena',       22, 'Doubles',          3),
('Manav Rana',         22, 'Singles',          4);

-- Amity Aces (Team 23)
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Priya Nair',         23, 'Singles',          1),
('Alok Nair',          23, 'Doubles',          2),
('Kavya Menon',        23, 'Doubles',          3),
('Sid Thomas',         23, 'Singles',          4);

-- GL Bajaj Feathers (Team 24)
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Sonal Gupta',        24, 'Singles',          1),
('Vaibhav Bajaj',      24, 'Doubles',          2),
('Jaya Trivedi',       24, 'Doubles',          3),
('Kunal Mehta',        24, 'Singles',          4);

-- Bennett Birdie (Team 25)
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Puja Sharma',        25, 'Singles',          1),
('Abhinav Rao',        25, 'Doubles',          2),
('Shikha Kumari',      25, 'Doubles',          3),
('Saurabh Dev',        25, 'Singles',          4);

-- Galgotias Smash (Team 26)
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Anuja Tyagi',        26, 'Singles',          1),
('Rohan Srivastava',   26, 'Doubles',          2),
('Chhavi Sharma',      26, 'Doubles',          3),
('Prabhat Dixit',      26, 'Singles',          4);

-- ── TABLE TENNIS PLAYERS ───────────────────────────────────
-- SNU Spin Masters (Team 27)
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Rahul Bansal',       27, 'Singles',          1),
('Nidhi Gupta',        27, 'Singles',          2),
('Abhay Mehta',        27, 'Doubles',          3),
('Simran Kaur',        27, 'Doubles',          4);

-- JIIT Paddlers (Team 28)
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Tarun Bhatia',       28, 'Singles',          1),
('Sakshi Singh',       28, 'Singles',          2),
('Rahul Malhotra',     28, 'Doubles',          3),
('Priya Kapoor',       28, 'Doubles',          4);

-- Amity Spinners (Team 29)
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Ankit Sharma',       29, 'Singles',          1),
('Shreya Nair',        29, 'Singles',          2),
('Gaurav Pillai',      29, 'Doubles',          3),
('Divya Thomas',       29, 'Doubles',          4);

-- GL Bajaj Pingsters (Team 30)
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Rohit Srivastava',   30, 'Singles',          1),
('Neha Gupta',         30, 'Singles',          2),
('Shashank Yadav',     30, 'Doubles',          3),
('Manu Sharma',        30, 'Doubles',          4);

-- Bennett Slammers (Team 31)
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Vikas Misra',        31, 'Singles',          1),
('Pallavi Singh',      31, 'Singles',          2),
('Rajat Kumar',        31, 'Doubles',          3),
('Rashmi Aggarwal',    31, 'Doubles',          4);

-- Galgotias TT (Team 32)
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Keshav Rana',        32, 'Singles',          1),
('Varsha Mehta',       32, 'Singles',          2),
('Naveen Joshi',       32, 'Doubles',          3),
('Deepika Sharma',     32, 'Doubles',          4);

-- ── VOLLEYBALL PLAYERS ─────────────────────────────────────
-- SNU Spikers (Team 33)
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Anand Pandey',       33, 'Setter',           3),
('Ravi Joshi',         33, 'Outside Hitter',   7),
('Sunil Bhatt',        33, 'Libero',           10),
('Vikas Negi',         33, 'Middle Blocker',   5),
('Prakash Misra',      33, 'Opposite Hitter',  12),
('Kartik Chauhan',     33, 'Middle Blocker',   9);

-- JIIT Servers (Team 34)
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Aman Bhardwaj',      34, 'Setter',           3),
('Rajiv Kumar',        34, 'Outside Hitter',   7),
('Dharam Singh',       34, 'Libero',           10),
('Saurav Tomar',       34, 'Middle Blocker',   5),
('Rohit Jain',         34, 'Opposite Hitter',  12),
('Navneet Singh',      34, 'Middle Blocker',   9);

-- Amity Aces VB (Team 35)
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Sundar Krishnan',    35, 'Setter',           3),
('Suresh Nambiar',     35, 'Outside Hitter',   7),
('Arun Kumar',         35, 'Libero',           10),
('Vikram Menon',       35, 'Middle Blocker',   5),
('Sarath Nair',        35, 'Opposite Hitter',  12),
('Nithin George',      35, 'Middle Blocker',   9);

-- GL Bajaj Setters (Team 36)
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Deepak Gupta',       36, 'Setter',           3),
('Ashish Shukla',      36, 'Outside Hitter',   7),
('Ranjit Yadav',       36, 'Libero',           10),
('Amar Singh',         36, 'Middle Blocker',   5),
('Girish Trivedi',     36, 'Opposite Hitter',  12),
('Jagdish Pandey',     36, 'Middle Blocker',   9);

-- Bennett Blockers (Team 37)
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Ajay Tomar',         37, 'Setter',           3),
('Vikash Singh',       37, 'Outside Hitter',   7),
('Mahesh Kumar',       37, 'Libero',           10),
('Nikhil Rao',         37, 'Middle Blocker',   5),
('Sunit Sharma',       37, 'Opposite Hitter',  12),
('Tarun Chauhan',      37, 'Middle Blocker',   9);

-- Galgotias Smashers (Team 38)
INSERT INTO Players (Player_Name, Team_ID, Role, Jersey_No) VALUES
('Abhishek Gupta',     38, 'Setter',           3),
('Sanjay Yadav',       38, 'Outside Hitter',   7),
('Rahul Shukla',       38, 'Libero',           10),
('Dinesh Rawat',       38, 'Middle Blocker',   5),
('Pradeep Tiwari',     38, 'Opposite Hitter',  12),
('Suresh Chauhan',     38, 'Middle Blocker',   9);

-- ── TABLE 5: Matches ─────────────────────────────────────────
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

-- ── SURGE 2025 CRICKET MATCHES ──────────────────────────────
INSERT INTO Matches (Sport_ID, Team_A_ID, Team_B_ID, Match_Date, Match_Time, Venue_ID, Stage, Winner_Team_ID, Status) VALUES
(1, 1, 2, '2025-02-14', '09:00:00', 1, 'Group Stage', 1, 'Completed'),
(1, 3, 4, '2025-02-14', '13:00:00', 1, 'Group Stage', 3, 'Completed'),
(1, 5, 6, '2025-02-15', '09:00:00', 1, 'Group Stage', 5, 'Completed'),
(1, 7, 8, '2025-02-15', '13:00:00', 1, 'Group Stage', 7, 'Completed'),
(1, 1, 3, '2025-02-16', '09:00:00', 1, 'Group Stage', 1, 'Completed'),
(1, 2, 4, '2025-02-16', '13:00:00', 1, 'Group Stage', 4, 'Completed'),
(1, 5, 7, '2025-02-17', '09:00:00', 1, 'Group Stage', 5, 'Completed'),
(1, 6, 8, '2025-02-17', '13:00:00', 1, 'Group Stage', 6, 'Completed'),
(1, 1, 5, '2025-02-18', '10:00:00', 1, 'Semi-Final',  1, 'Completed'),
(1, 3, 7, '2025-02-18', '14:00:00', 1, 'Semi-Final',  3, 'Completed'),
(1, 1, 3, '2025-02-20', '11:00:00', 1, 'Final',       NULL, 'Scheduled');

-- ── SURGE 2025 FOOTBALL MATCHES ─────────────────────────────
INSERT INTO Matches (Sport_ID, Team_A_ID, Team_B_ID, Match_Date, Match_Time, Venue_ID, Stage, Winner_Team_ID, Status) VALUES
(2,  9, 10, '2025-02-14', '10:00:00', 2, 'Group Stage',  9, 'Completed'),
(2, 11, 12, '2025-02-14', '14:00:00', 2, 'Group Stage', 11, 'Completed'),
(2, 13, 14, '2025-02-15', '10:00:00', 2, 'Group Stage', 13, 'Completed'),
(2,  9, 11, '2025-02-16', '10:00:00', 2, 'Group Stage',  9, 'Completed'),
(2, 10, 12, '2025-02-16', '14:00:00', 2, 'Group Stage', 12, 'Completed'),
(2,  9, 13, '2025-02-18', '10:00:00', 2, 'Semi-Final',   9, 'Completed'),
(2, 11, 12, '2025-02-18', '14:00:00', 2, 'Semi-Final',  11, 'Completed'),
(2,  9, 11, '2025-02-20', '14:00:00', 2, 'Final',       NULL, 'Scheduled');

-- ── SURGE 2025 BASKETBALL MATCHES ────────────────────────────
INSERT INTO Matches (Sport_ID, Team_A_ID, Team_B_ID, Match_Date, Match_Time, Venue_ID, Stage, Winner_Team_ID, Status) VALUES
(3, 15, 16, '2025-02-14', '11:00:00', 3, 'Group Stage', 15, 'Completed'),
(3, 17, 18, '2025-02-14', '15:00:00', 3, 'Group Stage', 17, 'Completed'),
(3, 19, 20, '2025-02-15', '11:00:00', 3, 'Group Stage', 19, 'Completed'),
(3, 15, 17, '2025-02-16', '11:00:00', 3, 'Group Stage', 15, 'Completed'),
(3, 16, 18, '2025-02-16', '15:00:00', 3, 'Group Stage', 18, 'Completed'),
(3, 15, 19, '2025-02-18', '11:00:00', 3, 'Semi-Final',  15, 'Completed'),
(3, 17, 18, '2025-02-18', '15:00:00', 3, 'Semi-Final',  17, 'Completed'),
(3, 15, 17, '2025-02-20', '09:00:00', 3, 'Final',       NULL, 'Scheduled');

-- ── SURGE 2025 BADMINTON MATCHES ─────────────────────────────
INSERT INTO Matches (Sport_ID, Team_A_ID, Team_B_ID, Match_Date, Match_Time, Venue_ID, Stage, Winner_Team_ID, Status) VALUES
(4, 21, 22, '2025-02-14', '09:00:00', 5, 'Group Stage', 21, 'Completed'),
(4, 23, 24, '2025-02-14', '11:00:00', 5, 'Group Stage', 23, 'Completed'),
(4, 25, 26, '2025-02-14', '13:00:00', 5, 'Group Stage', 25, 'Completed'),
(4, 21, 23, '2025-02-15', '09:00:00', 5, 'Group Stage', 21, 'Completed'),
(4, 22, 24, '2025-02-15', '11:00:00', 5, 'Group Stage', 24, 'Completed'),
(4, 21, 25, '2025-02-17', '09:00:00', 5, 'Semi-Final',  21, 'Completed'),
(4, 23, 25, '2025-02-17', '11:00:00', 5, 'Semi-Final',  23, 'Completed'),
(4, 21, 23, '2025-02-20', '13:00:00', 5, 'Final',       NULL, 'Scheduled');

-- ── SURGE 2025 TABLE TENNIS MATCHES ──────────────────────────
INSERT INTO Matches (Sport_ID, Team_A_ID, Team_B_ID, Match_Date, Match_Time, Venue_ID, Stage, Winner_Team_ID, Status) VALUES
(5, 27, 28, '2025-02-13', '10:00:00', 6, 'Group Stage', 27, 'Completed'),
(5, 29, 30, '2025-02-13', '12:00:00', 6, 'Group Stage', 30, 'Completed'),
(5, 31, 32, '2025-02-13', '14:00:00', 6, 'Group Stage', 31, 'Completed'),
(5, 27, 30, '2025-02-15', '10:00:00', 6, 'Semi-Final',  27, 'Completed'),
(5, 28, 31, '2025-02-15', '12:00:00', 6, 'Semi-Final',  31, 'Completed'),
(5, 27, 31, '2025-02-20', '15:00:00', 6, 'Final',       NULL, 'Scheduled');

-- ── SURGE 2025 VOLLEYBALL MATCHES ────────────────────────────
INSERT INTO Matches (Sport_ID, Team_A_ID, Team_B_ID, Match_Date, Match_Time, Venue_ID, Stage, Winner_Team_ID, Status) VALUES
(6, 33, 34, '2025-02-13', '09:00:00', 7, 'Group Stage', 33, 'Completed'),
(6, 35, 36, '2025-02-13', '11:00:00', 7, 'Group Stage', 35, 'Completed'),
(6, 37, 38, '2025-02-13', '13:00:00', 7, 'Group Stage', 37, 'Completed'),
(6, 33, 35, '2025-02-15', '09:00:00', 7, 'Semi-Final',  33, 'Completed'),
(6, 34, 37, '2025-02-15', '11:00:00', 7, 'Semi-Final',  37, 'Completed'),
(6, 33, 37, '2025-02-20', '11:00:00', 7, 'Final',       NULL, 'Scheduled');

-- ── TABLE 6: Scorecard_Cricket ───────────────────────────────
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

-- ── CRICKET SCORECARD DATA (SURGE 2025) ──────────────────────
-- Match 1: SNU Stallions vs JIIT Thunderbolts — SNU wins 174/6 vs 149/8
INSERT INTO Scorecard_Cricket (Match_ID, Player_ID, Runs_Scored, Wickets_Taken, Overs_Bowled, Catches) VALUES
(1,  1, 68, 0, 0.0, 1),(1,  2, 22, 2, 4.0, 0),(1,  3, 15, 0, 0.0, 1),
(1,  4,  0, 3, 4.0, 0),(1,  5,  0, 1, 4.0, 0),(1,  6, 34, 0, 0.0, 0),
(1,  7, 18, 0, 0.0, 1),(1,  8,  0, 0, 4.0, 0),(1,  9,  7, 0, 0.0, 0),
(1, 10,  0, 0, 4.0, 1),(1, 11, 10, 0, 0.0, 0),
(1, 12, 41, 0, 0.0, 0),(1, 13,  0, 2, 4.0, 0),(1, 14, 28, 0, 0.0, 0),
(1, 15,  0, 2, 4.0, 0),(1, 16, 18, 0, 0.0, 0),(1, 17, 22, 0, 0.0, 1),
(1, 18,  0, 2, 4.0, 0),(1, 19, 12, 0, 0.0, 0),(1, 20,  0, 0, 4.0, 0),
(1, 21, 15, 0, 0.0, 0),(1, 22, 13, 0, 0.0, 0);

-- Match 2: Amity Titans vs GL Bajaj Chargers — Amity wins 161/5 vs 138/9
INSERT INTO Scorecard_Cricket (Match_ID, Player_ID, Runs_Scored, Wickets_Taken, Overs_Bowled, Catches) VALUES
(2, 23, 55, 0, 0.0, 0),(2, 24,  0, 2, 4.0, 0),(2, 25, 18, 0, 0.0, 1),
(2, 26,  0, 1, 4.0, 0),(2, 27,  0, 2, 4.0, 0),(2, 28, 42, 0, 0.0, 0),
(2, 29, 30, 0, 0.0, 0),(2, 30,  0, 0, 4.0, 0),(2, 31, 16, 0, 0.0, 0),
(2, 32,  0, 0, 4.0, 1),(2, 33,  0, 0, 0.0, 0),
(2, 34, 33, 0, 0.0, 0),(2, 35,  0, 2, 4.0, 0),(2, 36, 24, 0, 0.0, 0),
(2, 37,  0, 1, 4.0, 0),(2, 38, 28, 0, 0.0, 0),(2, 39, 15, 0, 0.0, 1),
(2, 40,  0, 2, 4.0, 0),(2, 41, 10, 0, 0.0, 0),(2, 42,  0, 0, 4.0, 0),
(2, 43, 13, 0, 0.0, 0),(2, 44,  5, 2, 0.0, 0);

-- Match 5: SNU Stallions vs Amity Titans — SNU wins 188/4 vs 151/8
INSERT INTO Scorecard_Cricket (Match_ID, Player_ID, Runs_Scored, Wickets_Taken, Overs_Bowled, Catches) VALUES
(5,  1, 82, 0, 0.0, 1),(5,  2, 35, 1, 4.0, 0),(5,  6, 54, 0, 0.0, 0),
(5,  4,  0, 2, 4.0, 0),(5,  5,  0, 2, 4.0, 0),(5,  7, 17, 0, 0.0, 0),
(5, 23, 28, 0, 0.0, 0),(5, 24,  0, 3, 4.0, 0),(5, 28, 36, 0, 0.0, 0),
(5, 27,  0, 1, 4.0, 0),(5, 33, 30, 0, 0.0, 0);

-- Semi Final: SNU vs Bennett — SNU wins 195/3 vs 142/10
INSERT INTO Scorecard_Cricket (Match_ID, Player_ID, Runs_Scored, Wickets_Taken, Overs_Bowled, Catches) VALUES
(9,  1,105, 0, 0.0, 1),(9,  6, 61, 0, 0.0, 0),(9,  2, 18, 2, 4.0, 0),
(9,  4,  0, 3, 3.0, 0),(9,  5,  0, 2, 4.0, 0),(9, 11, 11, 0, 0.0, 0),
(9, 45, 22, 0, 0.0, 0),(9, 46,  0, 2, 4.0, 0),(9, 49, 36, 0, 0.0, 0),
(9, 50,  0, 1, 4.0, 0),(9, 51, 38, 0, 0.0, 0);

-- ── TABLE 7: Scorecard_Football ──────────────────────────────
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

-- Match 12: SNU FC vs JIIT United (SNU wins 3-1)
INSERT INTO Scorecard_Football (Match_ID, Player_ID, Goals, Assists, Yellow_Cards, Red_Cards) VALUES
(12, 101, 2, 1, 0, 0),(12, 106, 1, 0, 1, 0),(12, 108, 0, 2, 0, 0),
(12, 110, 0, 0, 1, 0),(12, 111, 0, 1, 0, 0),
(12, 112, 1, 0, 0, 0),(12, 113, 0, 1, 1, 0),(12, 116, 0, 0, 1, 0);

-- Match 13: Amity Athletic vs GL Bajaj FC (Amity wins 2-0)
INSERT INTO Scorecard_Football (Match_ID, Player_ID, Goals, Assists, Yellow_Cards, Red_Cards) VALUES
(13, 122, 1, 1, 0, 0),(13, 127, 1, 0, 0, 0),(13, 123, 0, 1, 1, 0),
(13, 133, 0, 0, 1, 0),(13, 134, 0, 0, 1, 0);

-- Match 14: Bennett FC vs Galgotias United (Bennett wins 1-0)
INSERT INTO Scorecard_Football (Match_ID, Player_ID, Goals, Assists, Yellow_Cards, Red_Cards) VALUES
(14, 145, 1, 0, 0, 0),(14, 148, 0, 1, 1, 0),(14, 156, 0, 0, 0, 0),(14, 153, 0, 0, 1, 0);

-- Match 15: SNU FC vs Amity Athletic (SNU wins 2-1)
INSERT INTO Scorecard_Football (Match_ID, Player_ID, Goals, Assists, Yellow_Cards, Red_Cards) VALUES
(15, 101, 1, 0, 0, 0),(15, 106, 1, 1, 0, 0),(15, 108, 0, 1, 1, 0),
(15, 122, 1, 0, 1, 0),(15, 127, 0, 1, 1, 0),(15, 123, 0, 0, 1, 0);

-- Semi-Final: SNU FC vs Bennett FC (SNU wins 3-0)
INSERT INTO Scorecard_Football (Match_ID, Player_ID, Goals, Assists, Yellow_Cards, Red_Cards) VALUES
(18, 101, 2, 0, 0, 0),(18, 106, 1, 1, 0, 0),(18, 111, 0, 2, 0, 0),
(18, 108, 0, 0, 1, 0),(18, 145, 0, 0, 1, 0),(18, 148, 0, 0, 1, 0);

-- ── TABLE 8: Scorecard_Basketball ────────────────────────────
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

-- Match 20: SNU Hoopsters vs JIIT Ballers (SNU wins 78-61)
INSERT INTO Scorecard_Basketball (Match_ID, Player_ID, Points, Rebounds, Assists, Steals) VALUES
(20, 167, 24, 5, 8, 3),(20, 168, 18, 7, 3, 1),(20, 169, 14, 9, 2, 2),
(20, 170,  8, 11,1, 0),(20, 171, 14, 3, 5, 2),(20, 172,  0, 2, 2, 1),
(20, 174, 18, 4, 7, 2),(20, 175, 15, 6, 2, 1),(20, 176, 12, 8, 1, 1),
(20, 177,  9, 5, 4, 1),(20, 178,  7, 3, 3, 2);

-- Match 21: Amity Dunkers vs GL Bajaj Rockets (Amity wins 65-54)
INSERT INTO Scorecard_Basketball (Match_ID, Player_ID, Points, Rebounds, Assists, Steals) VALUES
(21, 181, 22, 4, 9, 2),(21, 182, 16, 8, 3, 1),(21, 183, 12, 7, 2, 2),
(21, 184,  7, 12,1, 0),(21, 185,  8, 3, 4, 2),(21, 186,  0, 2, 1, 0),
(21, 188, 14, 5, 6, 1),(21, 189, 13, 8, 2, 1),(21, 190, 11, 9, 2, 2),
(21, 191,  9, 4, 3, 1),(21, 192,  7, 2, 2, 1);

-- Match 24: SNU Hoopsters vs Amity Dunkers (SNU wins 82-70)
INSERT INTO Scorecard_Basketball (Match_ID, Player_ID, Points, Rebounds, Assists, Steals) VALUES
(24, 167, 28, 6, 9, 4),(24, 168, 22, 8, 4, 2),(24, 169, 16, 10,3, 1),
(24, 170, 10, 12,1, 0),(24, 171,  6, 4, 5, 2),
(24, 181, 25, 5, 8, 2),(24, 182, 18, 9, 3, 1),(24, 183, 14, 8, 2, 1),
(24, 184,  8, 11,1, 0),(24, 185,  5, 2, 4, 1);

-- Semi Final: SNU vs Bennett (SNU wins 74-62)
INSERT INTO Scorecard_Basketball (Match_ID, Player_ID, Points, Rebounds, Assists, Steals) VALUES
(26, 167, 26, 7, 10,3),(26, 168, 20, 8, 4, 2),(26, 169, 16, 9, 2, 1),
(26, 170,  6, 10,1, 0),(26, 171,  6, 4, 5, 1),
(26, 195, 18, 5, 5, 1),(26, 196, 15, 7, 3, 1),(26, 197, 14, 8, 2, 1),
(26, 198,  9, 11,2, 0),(26, 199,  6, 3, 2, 1);

-- ── TABLE 9: Scorecard_Badminton ─────────────────────────────
CREATE TABLE Scorecard_Badminton (
    Stat_ID      INT AUTO_INCREMENT PRIMARY KEY,
    Match_ID     INT NOT NULL,
    Player_ID    INT NOT NULL,
    Sets_Won     INT DEFAULT 0,
    Sets_Lost    INT DEFAULT 0,
    Points_Won   INT DEFAULT 0,
    Category     ENUM('Singles','Doubles') DEFAULT 'Singles',
    FOREIGN KEY (Match_ID)  REFERENCES Matches(Match_ID),
    FOREIGN KEY (Player_ID) REFERENCES Players(Player_ID)
);

-- ── TABLE 10: Scorecard_TableTennis ──────────────────────────
CREATE TABLE Scorecard_TableTennis (
    Stat_ID      INT AUTO_INCREMENT PRIMARY KEY,
    Match_ID     INT NOT NULL,
    Player_ID    INT NOT NULL,
    Games_Won    INT DEFAULT 0,
    Games_Lost   INT DEFAULT 0,
    Points_Won   INT DEFAULT 0,
    Category     ENUM('Singles','Doubles') DEFAULT 'Singles',
    FOREIGN KEY (Match_ID)  REFERENCES Matches(Match_ID),
    FOREIGN KEY (Player_ID) REFERENCES Players(Player_ID)
);

-- ── TABLE 11: Scorecard_Volleyball ───────────────────────────
CREATE TABLE Scorecard_Volleyball (
    Stat_ID      INT AUTO_INCREMENT PRIMARY KEY,
    Match_ID     INT NOT NULL,
    Player_ID    INT NOT NULL,
    Kills        INT DEFAULT 0,
    Blocks       INT DEFAULT 0,
    Aces         INT DEFAULT 0,
    Digs         INT DEFAULT 0,
    FOREIGN KEY (Match_ID)  REFERENCES Matches(Match_ID),
    FOREIGN KEY (Player_ID) REFERENCES Players(Player_ID)
);

-- ── TABLE 12: Users ──────────────────────────────────────────
CREATE TABLE Users (
    User_ID    INT AUTO_INCREMENT PRIMARY KEY,
    Username   VARCHAR(50) NOT NULL UNIQUE,
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

-- ── TABLE 13: Audit_Log ──────────────────────────────────────
CREATE TABLE Audit_Log (
    Log_ID     INT AUTO_INCREMENT PRIMARY KEY,
    Table_Name VARCHAR(50) NOT NULL,
    Operation  ENUM('INSERT','UPDATE','DELETE') NOT NULL,
    Record_ID  INT,
    Changed_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Changed_By VARCHAR(50) DEFAULT NULL,
    Old_Value  TEXT,
    New_Value  TEXT
);

-- ── TABLE 14: Predictions ────────────────────────────────────
CREATE TABLE Predictions (
    Pred_ID         INT AUTO_INCREMENT PRIMARY KEY,
    Player_ID       INT NOT NULL,
    Sport_Name      VARCHAR(50),
    Predicted_Score DECIMAL(10,2),
    Predicted_At    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Player_ID) REFERENCES Players(Player_ID)
);

-- ── INDEXES ──────────────────────────────────────────────────
CREATE INDEX idx_matches_date      ON Matches(Match_Date);
CREATE INDEX idx_matches_sport     ON Matches(Sport_ID);
CREATE INDEX idx_players_team      ON Players(Team_ID);
CREATE INDEX idx_cricket_player    ON Scorecard_Cricket(Player_ID);
CREATE INDEX idx_football_player   ON Scorecard_Football(Player_ID);
CREATE INDEX idx_basketball_player ON Scorecard_Basketball(Player_ID);
CREATE INDEX idx_audit_changed_at  ON Audit_Log(Changed_At);

SELECT 'ARENA_SNU v6 base setup complete! Now run advanced_queries.sql' AS Status;
SELECT CONCAT('Teams: ', COUNT(*)) AS Info FROM Teams;
SELECT CONCAT('Players: ', COUNT(*)) AS Info FROM Players;
SELECT CONCAT('Matches: ', COUNT(*)) AS Info FROM Matches;