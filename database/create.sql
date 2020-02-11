CREATE DATABASE tobii;

USE tobii;

CREATE TABLE `game` (
  `id` varchar(255) NOT NULL,
  `left_x` double DEFAULT NULL,
  `left_y` double DEFAULT NULL,
  `left_validity` int(11) DEFAULT NULL,
  `right_x` double DEFAULT NULL,
  `right_y` double DEFAULT NULL,
  `right_validity` double DEFAULT NULL,
  `width` int(11) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `average_x` double DEFAULT NULL,
  `average_y` double DEFAULT NULL,
  `average_validity` int(11) DEFAULT NULL,
  `t` int(11) DEFAULT NULL,
  `t_order` int(11) DEFAULT NULL,
  `pupil_diameter` varchar(255) DEFAULT NULL,
  `pupil_validity` int(11) DEFAULT NULL,
  `ispupil` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
