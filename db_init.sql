CREATE DATABASE IF NOT EXISTS myappdb;
USE myappdb;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL
);

INSERT INTO users (name, email) VALUES ('suresh','suresh@gmail.com'), ('lehar','lehar@gmail.com'), ('prasanna','prasanna@gmail.com'), ('aashish','aashish@gmail.com');
