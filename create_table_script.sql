DROP SCHEMA IF EXISTS SPM;
CREATE SCHEMA SPM CHARACTER SET utf8;
USE SPM;
SHOW TABLES;

CREATE TABLE IF NOT EXISTS TODOS (
id INT PRIMARY KEY AUTO_INCREMENT, 
title varchar(20), 
todo_description varchar(100));

CREATE TABLE IF NOT EXISTS `course` (
  `course_id` varchar(50),
  `course_name` varchar(255),
  `course_description` varchar(255),
  `course_creator_id` varchar(255),
  `date_created` datetime,
  UNIQUE(`course_id`),
  PRIMARY KEY (`course_id`)
);

CREATE TABLE IF NOT EXISTS `classes` (
  `course_id` varchar(50),
  `class_id` int AUTO_INCREMENT,
  `class_creator_id` varchar(255),
  `start_datetime` datetime,
  `end_datetime` datetime,
  `class_size` int,
  `trainer_id` int,
  PRIMARY KEY (`class_id`, `course_id`)
);

CREATE TABLE IF NOT EXISTS `chapter` (
  `course_id` varchar(50),
  `class_id` int,
  `chapter_id` int AUTO_INCREMENT,
  `chapter_name` varchar(255),
  PRIMARY KEY (`chapter_id`, `class_id`, `course_id`)
);

CREATE TABLE IF NOT EXISTS `material` (
  `course_id` varchar(50),
  `class_id` int,
  `chapter_id` int,
  `mateial_name` varchar(255),
  `material_id` int AUTO_INCREMENT,
  `material_reference` varchar(255),
  PRIMARY KEY (`material_id`, `chapter_id`, `class_id`, `course_id`)
);

CREATE TABLE IF NOT EXISTS `material_completion_status` (
  `learner_id` int,
  `course_id` varchar(50),
  `class_id` int,
  `chapter_id` int,
  `material_id` int,
  `material_name` varchar(255),
  `is_completed` boolean,
  PRIMARY KEY (`learner_id`, `material_id`, `chapter_id`, `class_id`, `course_id`)
);

CREATE TABLE IF NOT EXISTS `quiz` (
  `quiz_id` int,
  `course_id` varchar(50),
  `class_id` int,
  `duration` int,
  PRIMARY KEY (`quiz_id`,`course_id`,`class_id`)
);

CREATE TABLE IF NOT EXISTS `quiz_questions` (
  `course_id` varchar(50),
  `class_id` int,
  `quiz_id` int,
  `question_id` int,
  `question_description` varchar(255),
  PRIMARY KEY (`question_id`, `quiz_id`, `class_id`, `course_id`)
);

CREATE TABLE IF NOT EXISTS `quiz_questions_options` (
  `course_id` varchar(50),
  `class_id` int,
  `quiz_id` int,
  `question_id` int,
  `option` varchar(255),
  `is_correct_answer` boolean,
  PRIMARY KEY (`option`, `question_id`, `quiz_id`, `class_id`, `course_id`)
);

CREATE TABLE IF NOT EXISTS `quiz_results` (
  `learner_id` int,
  `course_id` varchar(50),
  `class_id` int,
  `quiz_id` int,
  `score` int,
  PRIMARY KEY (`learner_id`, `quiz_id`, `class_id`, `course_id`)
);

CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255),
  `department` varchar(255),
  `position` varchar(255),
  `user_type` varchar(255)
);

CREATE TABLE IF NOT EXISTS `learner` (
  `learner_id` int PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS `admin` (
  `admin_id` int PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS `trainer` (
  `trainer_id` int PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS `qualifications` (
  `trainer_id` int,
  `course_id` varchar(50),
  `is_qualified` boolean,
  PRIMARY KEY (`trainer_id`, `course_id`)
);

CREATE TABLE IF NOT EXISTS `badge` (
  `learner_id` int,
  `course_id` varchar(50),
  `is_qualified` boolean,
  PRIMARY KEY (`learner_id`, `course_id`)
);

CREATE TABLE IF NOT EXISTS `learner_enrolment` (
  `learner_id` int,
  `course_id` varchar(50),
  `class_id` int,
  `enrol_date` datetime,
  PRIMARY KEY (`learner_id`, `course_id`)
);

CREATE TABLE IF NOT EXISTS `course_prerequisites` (
  `course_id` varchar(50),
  `prereq_course_id` varchar(50),
  PRIMARY KEY (`course_id`, `prereq_course_id`)
);

ALTER TABLE `learner` ADD FOREIGN KEY (`learner_id`) REFERENCES `user` (`user_id`);

ALTER TABLE `admin` ADD FOREIGN KEY (`admin_id`) REFERENCES `user` (`user_id`);

ALTER TABLE `trainer` ADD FOREIGN KEY (`trainer_id`) REFERENCES `user` (`user_id`);

ALTER TABLE `classes` ADD FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`);

ALTER TABLE `chapter` ADD FOREIGN KEY (`course_id`) REFERENCES `classes` (`course_id`);

ALTER TABLE `chapter` ADD FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`);

ALTER TABLE `material` ADD FOREIGN KEY (`course_id`) REFERENCES `chapter` (`course_id`);

ALTER TABLE `material` ADD FOREIGN KEY (`class_id`) REFERENCES `chapter` (`class_id`);

ALTER TABLE `material` ADD FOREIGN KEY (`chapter_id`) REFERENCES `chapter` (`chapter_id`);

ALTER TABLE `material_completion_status` ADD FOREIGN KEY (`learner_id`) REFERENCES `learner` (`learner_id`);

ALTER TABLE `material_completion_status` ADD FOREIGN KEY (`course_id`) REFERENCES `material` (`course_id`);

ALTER TABLE `material_completion_status` ADD FOREIGN KEY (`class_id`) REFERENCES `material` (`class_id`);

ALTER TABLE `material_completion_status` ADD FOREIGN KEY (`chapter_id`) REFERENCES `material` (`chapter_id`);

ALTER TABLE `material_completion_status` ADD FOREIGN KEY (`material_id`) REFERENCES `material` (`material_id`);

ALTER TABLE `quiz` ADD FOREIGN KEY (`course_id`) REFERENCES `classes` (`course_id`);

ALTER TABLE `quiz` ADD FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`);

ALTER TABLE `quiz_questions` ADD FOREIGN KEY (`course_id`) REFERENCES `quiz` (`course_id`);

ALTER TABLE `quiz_questions` ADD FOREIGN KEY (`class_id`) REFERENCES `quiz` (`class_id`);

ALTER TABLE `quiz_questions` ADD FOREIGN KEY (`quiz_id`) REFERENCES `quiz` (`quiz_id`);

ALTER TABLE `quiz_questions_options` ADD FOREIGN KEY (`course_id`) REFERENCES `quiz_questions` (`course_id`);

ALTER TABLE `quiz_questions_options` ADD FOREIGN KEY (`class_id`) REFERENCES `quiz_questions` (`class_id`);

ALTER TABLE `quiz_questions_options` ADD FOREIGN KEY (`quiz_id`) REFERENCES `quiz_questions` (`quiz_id`);

ALTER TABLE `quiz_questions_options` ADD FOREIGN KEY (`question_id`) REFERENCES `quiz_questions` (`question_id`);

ALTER TABLE `quiz_results` ADD FOREIGN KEY (`learner_id`) REFERENCES `learner` (`learner_id`);

ALTER TABLE `quiz_results` ADD FOREIGN KEY (`course_id`) REFERENCES `quiz` (`course_id`);

ALTER TABLE `quiz_results` ADD FOREIGN KEY (`class_id`) REFERENCES `quiz` (`class_id`);

ALTER TABLE `quiz_results` ADD FOREIGN KEY (`quiz_id`) REFERENCES `quiz` (`quiz_id`);

ALTER TABLE `qualifications` ADD FOREIGN KEY (`trainer_id`) REFERENCES `trainer` (`trainer_id`);

ALTER TABLE `qualifications` ADD FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`);

ALTER TABLE `badge` ADD FOREIGN KEY (`learner_id`) REFERENCES `learner` (`learner_id`);

ALTER TABLE `badge` ADD FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`);

ALTER TABLE `learner_enrolment` ADD FOREIGN KEY (`learner_id`) REFERENCES `learner` (`learner_id`);

ALTER TABLE `learner_enrolment` ADD FOREIGN KEY (`course_id`) REFERENCES `classes` (`course_id`);

ALTER TABLE `learner_enrolment` ADD FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`);

ALTER TABLE `course_prerequisites` ADD FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`);

ALTER TABLE `course_prerequisites` ADD FOREIGN KEY (`prereq_course_id`) REFERENCES `course` (`course_id`);