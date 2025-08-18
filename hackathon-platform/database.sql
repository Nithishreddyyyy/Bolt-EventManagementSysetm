create database hackdb;
use hackdb;

-- ==========================
-- USERS TABLE
-- ==========================
CREATE TABLE Users (
    user_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('participant', 'judge', 'organizer') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- ==========================
-- EVENTS TABLE
-- ==========================
CREATE TABLE Events (
    event_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    theme VARCHAR(100),
    rules TEXT,
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    prizes JSON,
    created_by INT UNSIGNED NOT NULL,
    FOREIGN KEY (created_by) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- ==========================
-- TEAMS TABLE
-- ==========================
CREATE TABLE Teams (
    team_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    event_id INT UNSIGNED NOT NULL,
    leader_id INT UNSIGNED NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES Events(event_id) ON DELETE CASCADE,
    FOREIGN KEY (leader_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- ==========================
-- TEAM MEMBERS TABLE
-- ==========================
CREATE TABLE TeamMembers (
    member_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    team_id INT UNSIGNED NOT NULL,
    user_id INT UNSIGNED NOT NULL,
    role VARCHAR(50) DEFAULT 'member',
    FOREIGN KEY (team_id) REFERENCES Teams(team_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- ==========================
-- JUDGING SCORES TABLE
-- ==========================
CREATE TABLE JudgingScores (
    score_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    submission_id VARCHAR(50) NOT NULL, -- Refers to MongoDB Submission _id
    judge_id INT UNSIGNED NOT NULL,
    score INT CHECK (score >= 0 AND score <= 100),
    feedback TEXT,
    round INT DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (judge_id) REFERENCES Users(user_id) ON DELETE CASCADE
);
