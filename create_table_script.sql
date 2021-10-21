CREATE SCHEMA IF NOT EXISTS SPM;
USE SPM;
SHOW TABLES;

CREATE TABLE IF NOT EXISTS TODOS (
id INT PRIMARY KEY AUTO_INCREMENT, 
title varchar(20), 
todo_description varchar(100));

CREATE TABLE IF NOT EXISTS COURSES (
course_id varchar(20) PRIMARY KEY, 
title varchar(20), 
course_description varchar(100));