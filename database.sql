CREATE DATABASE IF NOT EXISTS taskflow;

USE taskflow;

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority ENUM('low','medium','high') DEFAULT 'medium',
    status ENUM('pending','completed') DEFAULT 'pending',
    due_date DATE
);