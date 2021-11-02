-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 01, 2021 at 02:07 PM
-- Server version: 5.7.34
-- PHP Version: 8.0.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `SPM`
--

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`) VALUES
(1);

--
-- Dumping data for table `chapter`
--

INSERT INTO `chapter` (`course_id`, `class_id`, `chapter_id`, `chapter_name`) VALUES
('IS110', 1, 1, 'String Methods'),
('IS111', 2, 1, 'String Methods'),
('IS111', 1, 2, 'Conditional Statements'),
('IS112', 2, 2, 'Conditional Statements');

--
-- Dumping data for table `classes`
--

INSERT INTO `classes` (`course_id`, `class_id`, `class_creator_id`, `start_datetime`, `end_datetime`, `class_size`, `trainer_id`) VALUES
('IS110', 1, 'Patrick Thng', '2021-08-31 00:00:00', '2021-11-29 00:00:00', 40, 3),
('IS111', 1, 'Lee Yeow Leong', '2021-08-31 00:00:00', '2021-11-29 00:00:00', 40, 3),
('IS112', 1, 'Lee Yeow Leong', '2021-08-31 00:00:00', '2021-11-29 00:00:00', 40, 3),
('IS110', 2, 'Lee Yeow Leong', '2021-08-31 00:00:00', '2021-11-29 00:00:00', 40, 3),
('IS112', 2, 'Lee Yeow Leong', '2021-08-31 00:00:00', '2021-11-29 00:00:00', 40, 3);

--
-- Dumping data for table `course`
--

INSERT INTO `course` (`course_id`, `course_name`, `course_description`, `course_creator_id`, `date_created`) VALUES
('IS110', 'Information Systems and Innovation', 'Overview of Business Cases', 'HR Adrian', '2021-08-16 00:00:00'),
('IS111', 'Introduction to Programming', 'Basic to Python', 'HR Adrian', '2021-08-16 00:00:00'),
('IS112', 'Introduction to Coding', 'Basic to Python', 'HR101', '2021-08-20 00:00:00');

--
-- Dumping data for table `learner`
--

INSERT INTO `learner` (`learner_id`) VALUES
(2);

--
-- Dumping data for table `learner_enrolment`
--

INSERT INTO `learner_enrolment` (`learner_id`, `course_id`, `class_id`, `enrol_date`) VALUES
(2, 'IS110', 1, '2021-11-01 21:53:34'),
(2, 'IS112', 1, '2021-11-01 22:05:27');

--
-- Dumping data for table `quiz`
--

INSERT INTO `quiz` (`course_id`, `class_id`, `quiz_id`, `duration`) VALUES
('IS110', 1, 1, 100),
('IS111', 1, 2, 100),
('IS112', 1, 3, 100);

--
-- Dumping data for table `quiz_questions`
--

INSERT INTO `quiz_questions` (`course_id`, `class_id`, `quiz_id`, `question_id`, `question_description`) VALUES
('IS110', 1, 1, 1, 'Are you smart?'),
('IS111', 1, 2, 1, 'Are you dumb?'),
('IS112', 1, 3, 1, 'Are you funky?'),
('IS111', 1, 2, 2, 'Are you cool?');

--
-- Dumping data for table `quiz_questions_options`
--

INSERT INTO `quiz_questions_options` (`course_id`, `class_id`, `quiz_id`, `question_id`, `option`, `is_correct_answer`) VALUES
('IS110', 1, 1, 1, 'No', 0),
('IS112', 1, 3, 1, 'no', 0),
('IS111', 1, 2, 2, 'treu', 1),
('IS111', 1, 2, 1, 'yes', 0);

--
-- Dumping data for table `trainer`
--

INSERT INTO `trainer` (`trainer_id`) VALUES
(3);

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `name`, `department`, `position`, `user_type`) VALUES
(1, 'Admin User', 'Human Resource', 'HR Junior', 'admin'),
(2, 'Learner User', 'Data Science', 'Junior Engineer', 'learner'),
(3, 'Trainer User', 'Data Science', 'Senior Engineer', 'trainer');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
