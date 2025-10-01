CREATE DATABASE IF NOT EXISTS alumni_connect;
USE alumni_connect;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  role ENUM('alumni','student') NOT NULL DEFAULT 'student'
);

INSERT INTO users (name, role) VALUES
  ('Alice Alumni','alumni'),
  ('Sam Student','student')
ON DUPLICATE KEY UPDATE name=VALUES(name);


