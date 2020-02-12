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
  `width` double DEFAULT NULL,
  `height` double DEFAULT NULL,
  `average_x` double DEFAULT NULL,
  `average_y` double DEFAULT NULL,
  `average_validity` int(11) DEFAULT NULL,
  `t` int(11) DEFAULT NULL,
  `t_order` int(11) DEFAULT NULL,
  `pupil_diameter` double DEFAULT NULL,
  `pupil_validity` int(11) DEFAULT NULL,
  `ispupil` int(11) DEFAULT NULL,
  `card_width` double DEFAULT NULL,
  `card_height` double DEFAULT NULL,
  `card_horizontal_margin` double DEFAULT NULL,
  `card_vertical_margin` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
