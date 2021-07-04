-- phpMyAdmin SQL Dump
-- version 4.0.4.2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 09, 2021 at 09:56 PM
-- Server version: 5.6.13
-- PHP Version: 5.4.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `test`
--
CREATE DATABASE IF NOT EXISTS `data_bot` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `data_bot`;

-- --------------------------------------------------------

--
-- Table structure for table `admin_manager`
--

CREATE TABLE IF NOT EXISTS `admin_manager` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`user_name`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `admin_manager`
--

INSERT INTO `admin_manager` (`id`, `user_name`, `password`, `status`) VALUES
(1, 'admin', 'pbkdf2:sha256:150000$D8JNnhoz$d01241d60f042c53b1721fbf95508f7439ace95e51ff471aa686e6e0bc377aca', 1);

--
-- Table structure for table `power_record`
--
CREATE TABLE IF NOT EXISTS `power_record` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `time_record` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `voltage` varchar(100) NOT NULL,
  `capacity` varchar(100) NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=0 ;

-- --------------------------------------------------------

--
-- Table structure for table `alert_list`
--

CREATE TABLE IF NOT EXISTS `alert_list` (
  `user_id` varchar(50) CHARACTER SET cp1251 COLLATE cp1251_bin NOT NULL,
  `time_create` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_name` varchar(50) CHARACTER SET cp1251 COLLATE cp1251_bin NOT NULL,
  `permission` tinyint(1) NOT NULL,
  `comment` varchar(200) CHARACTER SET cp1251 COLLATE cp1251_bin DEFAULT NULL,
  `expiration` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `alert_list`
--

INSERT INTO `alert_list` (`user_id`, `time_create`, `user_name`, `permission`, `comment`, `expiration`) VALUES
('1343733841', '2020-10-28 18:43:35', 'nguyen van trung', 1, 'пользователь 1', '2022-12-06 21:01:00');

-- --------------------------------------------------------

--
-- Table structure for table `climate`
--

CREATE TABLE IF NOT EXISTS `climate` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `Time_request` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Temperature` decimal(10,2) NOT NULL,
  `Humidity` decimal(10,2) NOT NULL,
  `Temperature_set` decimal(7,2) DEFAULT NULL,
  `Humidity_set` decimal(7,2) DEFAULT NULL,
  `Profile No.` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Profile Name` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Profile Cycles` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Active Cycles` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Total Loops` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Act Loops` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Segment` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Active Time` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Profile Time` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Total Time` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Segment Type` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Segment Total Time` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Segment Remain Time` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Status` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4026 ;
--
-- Table structure for table `para_manager`
--

CREATE TABLE IF NOT EXISTS `para_manager` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `parameter` varchar(50) DEFAULT NULL,
  `on_message` tinyint(1) DEFAULT NULL,
  `value` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=23 ;

--
-- Dumping data for table `para_manager`
--

INSERT INTO `para_manager` (`id`, `parameter`, `on_message`, `value`) VALUES
(1, 'id', 1, NULL),
(2, 'Time_request', 1, NULL),
(3, 'Temperature', 1, NULL),
(4, 'Temperature_set', 1, NULL),
(5, 'Humidity', 1, NULL),
(6, 'Humidity_set', 1, NULL),
(7, 'Profile No.', 1, NULL),
(8, 'Profile Name', 1, NULL),
(9, 'Profile Cycles', 0, NULL),
(10, 'Active Cycles', 0, NULL),
(11, 'Total Loops', 0, NULL),
(12, 'Act Loops', 0, NULL),
(13, 'Segment', 0, NULL),
(14, 'Active Time', 0, NULL),
(15, 'Profile Time', 0, NULL),
(16, 'Total Time', 0, NULL),
(17, 'Segment Type', 0, NULL),
(18, 'Segment Total Time', 0, NULL),
(19, 'Segment Remain Time', 0, NULL),
(20, 'Status', 0, NULL),
(21, 'Time_cycle', 0, '13'),
(22, 'Time_req', 0, '0.2');
