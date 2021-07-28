-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: zrp.cool    Database: CAMotion
-- ------------------------------------------------------
-- Server version	5.7.34-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cams`
--

DROP TABLE IF EXISTS `cams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cams` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `rtmp_url` varchar(256) NOT NULL DEFAULT ' ',
  `area` varchar(255) DEFAULT '0',
  `flv_url` varchar(255) NOT NULL DEFAULT ' ',
  `working` tinyint(1) NOT NULL DEFAULT '0',
  `uid` int(11) NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  KEY `cams_users_id_fk` (`uid`),
  CONSTRAINT `cams_users_id_fk` FOREIGN KEY (`uid`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `info` varchar(255) NOT NULL,
  `time` datetime NOT NULL,
  `img_url` varchar(255) DEFAULT NULL,
  `cid` int(11) NOT NULL,
  `delete_img` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `logs_cams_id_fk` (`cid`),
  CONSTRAINT `logs_cams_id_fk` FOREIGN KEY (`cid`) REFERENCES `cams` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=273 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `report`
--

DROP TABLE IF EXISTS `report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `info` varchar(255) NOT NULL,
  `uid` int(11) DEFAULT NULL,
  `done` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `report_users_id_fk` (`uid`),
  CONSTRAINT `report_users_id_fk` FOREIGN KEY (`uid`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `password` varchar(256) NOT NULL,
  `salt` varchar(64) DEFAULT NULL,
  `role` int(11) NOT NULL DEFAULT '0',
  `last_login` datetime DEFAULT NULL,
  `banned` tinyint(1) NOT NULL DEFAULT '0',
  `register_time` datetime NOT NULL,
  `notify` int(11) NOT NULL DEFAULT '1',
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_username_uindex` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=222 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-28 16:38:25
