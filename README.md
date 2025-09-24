# Workshop2025
Creation de la BDD ia_project avec : 

CREATE database ia_project;
USE ia_project;

CREATE TABLE users (
    ->     id INT AUTO_INCREMENT PRIMARY KEY,
    ->     username VARCHAR(50) NOT NULL UNIQUE,
    ->     password VARCHAR(255) NOT NULL
    -> );

INSERT INTO users (username, password)
    -> VALUES ('admin', 'admin');

SELECT * FROM users;

INSERT INTO users (username, password)
    -> VALUES ('admin', 'admin');