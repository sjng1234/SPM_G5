DROP SCHEMA IF EXISTS SPM;
CREATE SCHEMA SPM;
USE SPM;
SHOW TABLES;

CREATE TABLE IF NOT EXISTS TODOS (
id INT PRIMARY KEY AUTO_INCREMENT, 
title varchar(20), 
todo_description varchar(100));

CREATE TABLE IF NOT EXISTS `course` (
  `course_id` varchar(255) PRIMARY KEY,
  `course_name` varchar(255),
  `course_description` varchar(255),
  `course_creator_id` varchar(255),
  `date_created` datetime,
  UNIQUE(course_id)
);

CREATE TABLE IF NOT EXISTS `class` (
  `course_id` varchar(255),
  `class_id` int AUTO_INCREMENT,
  `class_creator_id` varchar(255),
  `start_datetime` datetime,
  `end_datetime` datetime,
  `class_size` int,
  `trainer_id` int,
  UNIQUE(class_id),
  PRIMARY KEY (`class_id`, `course_id`)
);

CREATE TABLE IF NOT EXISTS `chapter` (
  `course_id` varchar(255),
  `class_id` int,
  `chapter_id` int AUTO_INCREMENT,
  `chapter_name` varchar(255),
  UNIQUE(chapter_id),
  PRIMARY KEY (`chapter_id`, `class_id`, `course_id`)
);

CREATE TABLE IF NOT EXISTS `material` (
  `course_id` varchar(255),
  `class_id` int,
  `chapter_id` int,
  `material_id` int AUTO_INCREMENT,
  `material_reference` varchar(255),
  UNIQUE(material_id),
  PRIMARY KEY (`material_id`, `chapter_id`, `class_id`, `course_id`)
);

CREATE TABLE IF NOT EXISTS `material_completion_status` (
  `user_id` int,
  `course_id` varchar(255),
  `class_id` int,
  `chapter_id` int,
  `material_id` int,
  `is_completed` boolean,
  PRIMARY KEY (`user_id`, `material_id`, `chapter_id`, `class_id`, `course_id`)
);

CREATE TABLE IF NOT EXISTS `quiz` (
  `course_id` varchar(255),
  `class_id` int,
  `quiz_id` int,
  `duration` int,
  UNIQUE(quiz_id),
  PRIMARY KEY (`course_id`, `class_id`, `quiz_id`)
);

CREATE TABLE IF NOT EXISTS `quiz_questions` (
  `course_id` varchar(255),
  `class_id` int,
  `quiz_id` int,
  `question_id` varchar(255),
  `answer_course_id` varchar(255),
  `answer_class_id` int,
  `answer_quiz_id` int,
  `answer_question_id` varchar(255),
  `answer_option` varchar(255),
  
  
  PRIMARY KEY (`question_id`, `quiz_id`, `class_id`, `course_id`)
);

CREATE TABLE IF NOT EXISTS `quiz_questions_options` (
  `course_id` varchar(255),
  `class_id` int,
  `quiz_id` int,
  `question_id` varchar(255),
  `option` varchar(255),
  UNIQUE(`course_id`),
  UNIQUE(`class_id`),
  UNIQUE(`quiz_id`),
  UNIQUE(`question_id`),
  UNIQUE(`option`),
  PRIMARY KEY (`option`, `question_id`, `quiz_id`, `class_id`, `course_id`)
);

CREATE TABLE IF NOT EXISTS `quiz_results` (
  `user_id` int,
  `course_id` varchar(255),
  `class_id` int,
  `quiz_id` int,
  `score` int,
  PRIMARY KEY (`user_id`, `quiz_id`, `class_id`, `course_id`)
);

CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255),
  `department` varchar(255),
  `position` varchar(255),
  `is_learner` boolean,
  `is_trainer` boolean,
  `is_hr` boolean
);

CREATE TABLE IF NOT EXISTS `qualifications` (
  `user_id` int,
  `course_id` varchar(255),
  `is_qualified` boolean,
  PRIMARY KEY (`user_id`, `course_id`)
);

ALTER TABLE `class` ADD FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`);

ALTER TABLE `chapter` ADD FOREIGN KEY (`course_id`) REFERENCES `class` (`course_id`);

ALTER TABLE `chapter` ADD FOREIGN KEY (`class_id`) REFERENCES `class` (`class_id`);

ALTER TABLE `material` ADD FOREIGN KEY (`course_id`) REFERENCES `chapter` (`course_id`);

ALTER TABLE `material` ADD FOREIGN KEY (`class_id`) REFERENCES `chapter` (`class_id`);

ALTER TABLE `material` ADD FOREIGN KEY (`chapter_id`) REFERENCES `chapter` (`chapter_id`);

ALTER TABLE `material_completion_status` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

ALTER TABLE `material_completion_status` ADD FOREIGN KEY (`course_id`) REFERENCES `material` (`course_id`);

ALTER TABLE `material_completion_status` ADD FOREIGN KEY (`class_id`) REFERENCES `material` (`class_id`);

ALTER TABLE `material_completion_status` ADD FOREIGN KEY (`chapter_id`) REFERENCES `material` (`chapter_id`);

ALTER TABLE `material_completion_status` ADD FOREIGN KEY (`material_id`) REFERENCES `material` (`material_id`);

ALTER TABLE `quiz` ADD FOREIGN KEY (`course_id`) REFERENCES `class` (`course_id`);

ALTER TABLE `quiz` ADD FOREIGN KEY (`class_id`) REFERENCES `class` (`class_id`);

ALTER TABLE `quiz_questions` ADD FOREIGN KEY (`course_id`) REFERENCES `quiz` (`course_id`);

ALTER TABLE `quiz_questions` ADD FOREIGN KEY (`class_id`) REFERENCES `quiz` (`class_id`);

ALTER TABLE `quiz_questions` ADD FOREIGN KEY (`quiz_id`) REFERENCES `quiz` (`quiz_id`);

ALTER TABLE `quiz_questions` ADD FOREIGN KEY (`answer_course_id`) REFERENCES `quiz_questions_options` (`course_id`);

ALTER TABLE `quiz_questions` ADD FOREIGN KEY (`answer_class_id`) REFERENCES `quiz_questions_options` (`class_id`);

ALTER TABLE `quiz_questions` ADD FOREIGN KEY (`answer_quiz_id`) REFERENCES `quiz_questions_options` (`quiz_id`);

ALTER TABLE `quiz_questions` ADD FOREIGN KEY (`answer_question_id`) REFERENCES `quiz_questions_options` (`question_id`);

ALTER TABLE `quiz_questions` ADD FOREIGN KEY (`answer_option`) REFERENCES `quiz_questions_options` (`option`);

ALTER TABLE `quiz_questions_options` ADD FOREIGN KEY (`course_id`) REFERENCES `quiz_questions` (`course_id`);

ALTER TABLE `quiz_questions_options` ADD FOREIGN KEY (`class_id`) REFERENCES `quiz_questions` (`class_id`);

ALTER TABLE `quiz_questions_options` ADD FOREIGN KEY (`quiz_id`) REFERENCES `quiz_questions` (`quiz_id`);

ALTER TABLE `quiz_questions_options` ADD FOREIGN KEY (`question_id`) REFERENCES `quiz_questions` (`question_id`);

ALTER TABLE `quiz_results` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

ALTER TABLE `quiz_results` ADD FOREIGN KEY (`course_id`) REFERENCES `quiz` (`course_id`);

ALTER TABLE `quiz_results` ADD FOREIGN KEY (`class_id`) REFERENCES `quiz` (`class_id`);

ALTER TABLE `quiz_results` ADD FOREIGN KEY (`quiz_id`) REFERENCES `quiz` (`quiz_id`);

ALTER TABLE `qualifications` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

ALTER TABLE `qualifications` ADD FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`);

