DELETE FROM JudgingScores;
DELETE FROM TeamMembers;
DELETE FROM Teams;
DELETE FROM Events;
DELETE FROM Users;

INSERT INTO Users (name, email, password, role) VALUES
('Alice Johnson', 'alice@example.com', 'alice123', 'participant'),
('Bob Smith', 'bob@example.com', 'bob123', 'participant'),
('Carol Lee', 'carol@example.com', 'carol123', 'judge'),
('David Kim', 'david@example.com', 'david123', 'organizer'),
('Eva Brown', 'eva@example.com', 'eva123', 'judge');

INSERT INTO Events (name, theme, rules, start_date, end_date, prizes, created_by) VALUES
('HackMania 2025', 'AI & Sustainability', 'Rule 1\nRule 2\nRule 3', '2025-09-01 10:00:00', '2025-09-03 18:00:00', '[{"position":"1st","prize":"₹50,000"},{"position":"2nd","prize":"₹30,000"},{"position":"3rd","prize":"₹20,000"}]', 91),
('CodeSprint', 'Blockchain', 'Rule 1\nRule 2', '2025-10-05 09:00:00', '2025-10-05 17:00:00', '[{"position":"1st","prize":"₹25,000"},{"position":"2nd","prize":"₹15,000"}]', 91),
('Designathon', 'UI/UX', 'Rule 1\nRule 2\nRule 3\nRule 4', '2025-11-10 11:00:00', '2025-11-12 16:00:00', '[{"position":"1st","prize":"₹40,000"},{"position":"2nd","prize":"₹20,000"}]', 91),
('RoboWars', 'Robotics', 'Rule 1\nRule 2', '2025-12-01 10:00:00', '2025-12-02 18:00:00', '[{"position":"1st","prize":"₹60,000"},{"position":"2nd","prize":"₹35,000"}]', 91),
('DataFest', 'Data Science', 'Rule 1\nRule 2\nRule 3', '2025-12-15 09:00:00', '2025-12-16 17:00:00', '[{"position":"1st","prize":"₹45,000"},{"position":"2nd","prize":"₹25,000"}]', 91);


INSERT INTO Events (event_id, name, theme, rules, start_date, end_date, prizes, created_by) VALUES
(97, 'HackMania 2025', 'AI & Sustainability', 'Rule 1\nRule 2\nRule 3', '2025-09-01 10:00:00', '2025-09-03 18:00:00', '[{"prize": "₹50,000", "position": "1st"}, {"prize": "₹30,000", "position": "2nd"}, {"prize": "₹20,000", "position": "3rd"}]', 91),
(98, 'CodeSprint', 'Blockchain', 'Rule 1\nRule 2', '2025-10-05 09:00:00', '2025-10-05 17:00:00', '[{"prize": "₹25,000", "position": "1st"}, {"prize": "₹15,000", "position": "2nd"}]', 91),
(99, 'Designathon', 'UI/UX', 'Rule 1\nRule 2\nRule 3\nRule 4', '2025-11-10 11:00:00', '2025-11-12 16:00:00', '[{"prize": "₹40,000", "position": "1st"}, {"prize": "₹20,000", "position": "2nd"}]', 91),
(100, 'RoboWars', 'Robotics', 'Rule 1\nRule 2', '2025-12-01 10:00:00', '2025-12-02 18:00:00', '[{"prize": "₹60,000", "position": "1st"}, {"prize": "₹35,000", "position": "2nd"}]', 91),
(101, 'DataFest', 'Data Science', 'Rule 1\nRule 2\nRule 3', '2025-12-15 09:00:00', '2025-12-16 17:00:00', '[{"prize": "₹45,000", "position": "1st"}, {"prize": "₹25,000", "position": "2nd"}]', 91);



DELETE FROM Events;

ALTER TABLE Events AUTO_INCREMENT = 97;


DELETE FROM JudgingScores;
DELETE FROM TeamMembers;
DELETE FROM Teams;
DELETE FROM Events;
DELETE FROM Users;

ALTER TABLE Users AUTO_INCREMENT = 88;
ALTER TABLE Events AUTO_INCREMENT = 97;
ALTER TABLE Teams AUTO_INCREMENT = 1;
ALTER TABLE TeamMembers AUTO_INCREMENT = 1;
ALTER TABLE JudgingScores AUTO_INCREMENT = 1;


select * from users;






INSERT INTO Users (user_id, name, email, password, role) VALUES
(88, 'Alice Johnson', 'alice@example.com', 'alice123', 'participant'),
(89, 'Bob Smith', 'bob@example.com', 'bob123', 'participant'),
(90, 'Carol Lee', 'carol@example.com', 'carol123', 'judge'),
(91, 'David Kim', 'david@example.com', 'david123', 'organizer'),
(92, 'Eva Brown', 'eva@example.com', 'eva123', 'judge');





INSERT INTO Events (event_id, name, theme, rules, start_date, end_date, prizes, created_by) VALUES
(97, 'HackMania 2025', 'AI & Sustainability', 'Rule 1\nRule 2\nRule 3', '2025-09-01 10:00:00', '2025-09-03 18:00:00', '[{"prize": "₹50,000", "position": "1st"}, {"prize": "₹30,000", "position": "2nd"}, {"prize": "₹20,000", "position": "3rd"}]', 91),
(98, 'CodeSprint', 'Blockchain', 'Rule 1\nRule 2', '2025-10-05 09:00:00', '2025-10-05 17:00:00', '[{"prize": "₹25,000", "position": "1st"}, {"prize": "₹15,000", "position": "2nd"}]', 91),
(99, 'Designathon', 'UI/UX', 'Rule 1\nRule 2\nRule 3\nRule 4', '2025-11-10 11:00:00', '2025-11-12 16:00:00', '[{"prize": "₹40,000", "position": "1st"}, {"prize": "₹20,000", "position": "2nd"}]', 91),
(100, 'RoboWars', 'Robotics', 'Rule 1\nRule 2', '2025-12-01 10:00:00', '2025-12-02 18:00:00', '[{"prize": "₹60,000", "position": "1st"}, {"prize": "₹35,000", "position": "2nd"}]', 91),
(101, 'DataFest', 'Data Science', 'Rule 1\nRule 2\nRule 3', '2025-12-15 09:00:00', '2025-12-16 17:00:00', '[{"prize": "₹45,000", "position": "1st"}, {"prize": "₹25,000", "position": "2nd"}]', 91);


INSERT INTO Teams (team_id, team_name, event_id, leader_id) VALUES
(1, 'Alpha Coders', 97, 88),
(2, 'Beta Hackers', 97, 89),
(3, 'Crypto Masters', 98, 88),
(4, 'UI Wizards', 99, 89),
(5, 'Robo Champs', 100, 88);


INSERT INTO TeamMembers (team_id, user_id, role) VALUES
(1, 88, 'leader'),
(1, 89, 'member'),
(2, 89, 'leader'),
(2, 92, 'member'),
(3, 88, 'leader'),
(3, 90, 'member'),
(4, 89, 'leader'),
(4, 91, 'member'),
(5, 88, 'leader'),
(5, 92, 'member');

INSERT INTO JudgingScores (submission_id, judge_id, score, feedback, round) VALUES
('sub_001', 90, 85, 'Good effort, but improve UI', 1),
('sub_002', 92, 90, 'Excellent idea and execution', 1),
('sub_003', 90, 78, 'Needs more features', 1),
('sub_004', 92, 92, 'Well structured and innovative', 1),
('sub_005', 90, 88, 'Great use of technology', 1);


