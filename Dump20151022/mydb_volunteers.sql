CREATE DATABASE  IF NOT EXISTS `mydb` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `mydb`;
-- MySQL dump 10.13  Distrib 5.6.17, for Win32 (x86)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	5.6.10

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `volunteers`
--

DROP TABLE IF EXISTS `volunteers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `volunteers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `surname` varchar(45) NOT NULL,
  `forenames` varchar(45) NOT NULL,
  `initials` varchar(5) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `title` varchar(12) DEFAULT NULL,
  `sex` varchar(1) DEFAULT NULL,
  `addr1` varchar(45) DEFAULT NULL,
  `addr2` varchar(45) DEFAULT NULL,
  `town` varchar(45) DEFAULT NULL,
  `county` varchar(45) DEFAULT NULL,
  `postcode` varchar(45) DEFAULT NULL,
  `home_tel` varchar(45) DEFAULT NULL,
  `work_tel` varchar(45) DEFAULT NULL,
  `mobile` varchar(45) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `nhs_no` varchar(45) DEFAULT NULL,
  `moved_away` int(11) DEFAULT NULL,
  `diabetes_diagnosed` int(11) DEFAULT NULL,
  `modified_by` varchar(45) DEFAULT NULL,
  `reason` int(11) DEFAULT NULL,
  `phase1_comment` text,
  `phase2_comment` text,
  `modified` datetime DEFAULT NULL,
  `surgeries_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_volunteers_surgeries_idx` (`surgeries_id`),
  CONSTRAINT `fk_volunteers_surgeries` FOREIGN KEY (`surgeries_id`) REFERENCES `surgeries` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `volunteers`
--

LOCK TABLES `volunteers` WRITE;
/*!40000 ALTER TABLE `volunteers` DISABLE KEYS */;
INSERT INTO `volunteers` VALUES (1,'Gillies','David','','1978-03-21','Mr','M','Some Street','','Glasgow','Strathclyde','G84 8LH','','','','','',2,2,'admin',NULL,'','','2015-04-28 14:01:18',3),(2,'Numan','Artur','','1965-04-07','Mr','M','','','Cambridge','','RH5 6YH','','','','','',NULL,2,'admin',NULL,'','','2015-07-27 10:35:50',6),(3,'Ferguson','Alex','','1940-03-27','Mr','M','','','Glasgow','','G52','','','','','',1,2,'admin',NULL,'','','2015-07-09 09:40:53',4),(6,'Van CartHorse','Gio','','1940-03-27','Mr','','','','Cardiff','','AM67 7YH','','','','','',NULL,NULL,'admin',NULL,'','','2015-04-30 16:38:00',4),(7,'Hamster','Jorg','','1968-03-23','Mr','','','','Cardiff','','HA7 8AH','','','','','',NULL,NULL,'admin',NULL,'','','2015-05-06 13:35:38',4),(8,'Bishop','Kerry','','1968-03-23','Miss','','Ramsay Street','Erinsborough','Aberdeen','','M67 6TY','','','','','',NULL,NULL,'admin',NULL,'','','2015-05-01 09:51:48',4),(9,'Kerr','Morag','','1950-03-03','Miss','','','','Luss','','G87 9YH','','','','','',NULL,NULL,'admin',NULL,NULL,NULL,'2015-04-22 10:18:32',4),(10,'Kerr','Tom','','1948-03-03','Mr','','Inverdarroch','','Luss','','G87 9TH','','','','','',NULL,NULL,'',NULL,NULL,NULL,NULL,4),(11,'Sneddon','Dave','','1955-03-03','Mr','','','','Luss','','','','','','','',NULL,NULL,'admin',NULL,NULL,NULL,'2015-04-30 16:08:02',4),(12,'Ben','Mr','','1955-03-03','Mr','','','','London','','','','','','','',NULL,NULL,'',NULL,NULL,NULL,NULL,4),(13,'Bagpuss','Mr','','1970-03-03','Mr','','Emily\'s Shop','','Ipswich','','','','','','','',NULL,NULL,'admin',NULL,'','','2015-04-30 16:37:09',4),(14,'Dragon','Soup','','1968-03-03','Mr','','','','Liverpool','','','','','','','',NULL,NULL,'david',NULL,'','','2015-05-01 14:19:06',4),(15,'Abdoujaparov','Djamolidine','','1978-03-21','Mr','M','Some Street','','Glasgow','Kazakhstan','G84 8LH','','','','','',2,1,'admin',NULL,'','','2015-06-23 09:37:29',4),(25,'Vennegoor of Hesselink','Jan','','1967-04-22','Mr','M','Some Street','','Glasgow','','G84 8LH','','','','','',2,2,'admin',NULL,'','','2015-04-22 10:15:02',2),(26,'Gillespie','Mary','M','1896-04-27','Ms','F','Grangepans','','Grangemouth','Falkirk','','','','','','',NULL,2,'admin',NULL,'','','2015-07-09 14:20:56',5),(27,'Thistle','Kingsley','','1980-06-23','Mr','','','','Beckington','Somerset','','','','','','',1,1,'admin',NULL,NULL,NULL,'2015-07-09 14:29:10',4);
/*!40000 ALTER TABLE `volunteers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-10-22 16:47:18
