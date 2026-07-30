CREATE DATABASE intercollege_event;
USE intercollege_event;


CREATE TABLE colleges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    college_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL
);

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    college_id INT,
    password VARCHAR(255) NOT NULL,
    FOREIGN KEY (college_id) REFERENCES colleges(id)
);

CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(100) NOT NULL,
    event_date DATE,
    event_type ENUM('Technical','Cultural','Sports'),
    description TEXT,
    max_participants INT
);

CREATE TABLE registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    event_id INT,
    status ENUM('Pending','Approved','Rejected') DEFAULT 'Pending',
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);

-- Insert Sample College
INSERT INTO colleges (college_name, city)
VALUES ('ABC Engineering College', 'Mumbai');
INSERT INTO colleges (college_name, city)
VALUES ('cocsit college ', 'Latur');


-- Insert Sample Event
INSERT INTO events (event_name, event_date, event_type, description, max_participants)
VALUES ('Coding Competition', '2026-03-10', 'Technical', 'Inter college coding challenge', 100);

SHOW TABLES;

