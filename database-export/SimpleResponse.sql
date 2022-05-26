CREATE DATABASE  IF NOT EXISTS `simpleresponse` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `simpleresponse`;
-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: simpleresponse
-- ------------------------------------------------------
-- Server version	8.0.28

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
-- Table structure for table `actie`
--

DROP TABLE IF EXISTS `actie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actie` (
  `actieid` int NOT NULL AUTO_INCREMENT,
  `actiebeschrijving` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`actieid`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actie`
--

LOCK TABLES `actie` WRITE;
/*!40000 ALTER TABLE `actie` DISABLE KEYS */;
INSERT INTO `actie` VALUES (1,'orci. Ut semper pretium'),(2,'tempus mauris erat eget ipsum. Suspendisse sagittis. Nullam vitae'),(3,'amet diam eu dolor egestas rhoncus. Proin'),(4,'et, euismod et, commodo at, libero. Morbi'),(5,'elit. Nulla facilisi. Sed neque. Sed'),(6,'auctor odio a purus. Duis elementum, dui quis accumsan'),(7,'montes, nascetur ridiculus'),(8,'Curabitur egestas nunc sed libero. Proin'),(9,'aliquet libero. Integer in magna. Phasellus dolor elit,'),(10,'mus. Donec dignissim magna'),(11,'mi fringilla mi'),(12,'et'),(13,'ultricies ligula. Nullam enim.'),(14,'Donec nibh enim,'),(15,'adipiscing non, luctus sit amet, faucibus'),(16,'neque. Sed eget'),(17,'Nullam nisl. Maecenas malesuada fringilla est. Mauris eu turpis. Nulla'),(18,'commodo ipsum. Suspendisse'),(19,'mollis. Phasellus libero mauris, aliquam'),(20,'urna convallis erat, eget tincidunt dui augue'),(21,'est. Nunc ullamcorper, velit in aliquet lobortis, nisi'),(22,'augue scelerisque mollis. Phasellus'),(23,'ornare, libero at auctor ullamcorper, nisl arcu'),(24,'tortor, dictum eu,'),(25,'Curabitur consequat, lectus sit amet luctus vulputate, nisi sem'),(26,'ac, eleifend vitae, erat. Vivamus nisi. Mauris nulla. Integer urna.'),(27,'quis diam luctus lobortis. Class'),(28,'justo. Proin non massa non ante bibendum ullamcorper. Duis'),(29,'semper, dui lectus'),(30,'magna. Phasellus'),(31,'magna. Duis dignissim tempor arcu. Vestibulum ut'),(32,'lobortis quis, pede. Suspendisse dui. Fusce diam nunc, ullamcorper'),(33,'turpis non enim. Mauris quis turpis vitae'),(34,'vitae, aliquet nec, imperdiet nec, leo. Morbi'),(35,'dictum. Phasellus in felis.'),(36,'senectus et netus'),(37,'lorem, luctus ut, pellentesque eget, dictum'),(38,'vestibulum, neque sed dictum eleifend, nunc risus varius'),(39,'nec metus facilisis lorem tristique aliquet. Phasellus fermentum'),(40,'mollis. Phasellus libero mauris, aliquam eu, accumsan sed, facilisis'),(41,'natoque penatibus et magnis dis'),(42,'Fusce diam nunc, ullamcorper'),(43,'id ante dictum cursus.'),(44,'accumsan convallis, ante lectus convallis est,'),(45,'lectus pede et risus. Quisque libero'),(46,'leo elementum sem, vitae aliquam eros'),(47,'eget varius ultrices, mauris ipsum porta elit, a feugiat'),(48,'cursus luctus, ipsum leo elementum sem, vitae aliquam'),(49,'at sem molestie sodales.'),(50,'mauris, aliquam eu, accumsan sed, facilisis vitae, orci. Phasellus dapibus');
/*!40000 ALTER TABLE `actie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bericht`
--

DROP TABLE IF EXISTS `bericht`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bericht` (
  `berichtid` int NOT NULL AUTO_INCREMENT,
  `berichtinhoud` varchar(128) DEFAULT NULL,
  `gebruiker_gebruikerid` int NOT NULL,
  PRIMARY KEY (`berichtid`,`gebruiker_gebruikerid`),
  KEY `fk_bericht_gebruiker1_idx` (`gebruiker_gebruikerid`),
  CONSTRAINT `fk_bericht_gebruiker1` FOREIGN KEY (`gebruiker_gebruikerid`) REFERENCES `gebruiker` (`gebruikerid`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bericht`
--

LOCK TABLES `bericht` WRITE;
/*!40000 ALTER TABLE `bericht` DISABLE KEYS */;
INSERT INTO `bericht` VALUES (1,'Suspendisse aliquet, sem',2),(2,'massa rutrum magna. Cras convallis',1),(3,'sit amet, dapibus id,',1),(4,'Nulla',2),(5,'non arcu. Vivamus sit',2),(6,'nunc, ullamcorper eu, euismod ac,',1),(7,'gravida. Praesent eu nulla at sem',2),(8,'neque. Sed eget lacus. Mauris non dui nec',1),(9,'Duis dignissim tempor arcu. Vestibulum ut',1),(10,'vestibulum, neque sed dictum',2),(11,'ullamcorper magna. Sed eu eros. Nam consequat dolor',1),(12,'mi fringilla mi lacinia mattis. Integer eu lacus. Quisque',1),(13,'vel arcu eu odio tristique pharetra. Quisque ac',2),(14,'risus. Nulla eget metus eu erat semper',2),(15,'a odio semper cursus. Integer mollis. Integer',1),(16,'nulla. Integer urna.',2),(17,'Nam tempor',1),(18,'ad litora torquent per conubia nostra, per inceptos hymenaeos. Mauris',1),(19,'enim commodo hendrerit. Donec porttitor',1),(20,'rutrum, justo.',2),(21,'ipsum dolor',1),(22,'Aliquam nec enim. Nunc ut erat. Sed nunc',2),(23,'faucibus orci luctus et',1),(24,'nibh. Phasellus nulla. Integer vulputate, risus a ultricies',1),(25,'Aenean eget metus. In nec orci. Donec nibh. Quisque',1),(26,'Donec est mauris, rhoncus id,',1),(27,'imperdiet ullamcorper. Duis at lacus.',2),(28,'Nulla eu neque pellentesque massa lobortis ultrices. Vivamus rhoncus.',1),(29,'iaculis nec, eleifend non, dapibus rutrum, justo.',2),(30,'suscipit, est ac facilisis facilisis, magna tellus',1),(31,'non, lobortis quis, pede.',1),(32,'aliquet',1),(33,'arcu iaculis',1),(34,'faucibus leo, in',2),(35,'arcu eu odio tristique pharetra.',2),(36,'Sed molestie. Sed id',2),(37,'enim non nisi. Aenean eget',1),(38,'Curabitur massa. Vestibulum',1),(39,'conubia nostra, per inceptos hymenaeos.',1),(40,'non, feugiat',2),(41,'in lobortis tellus justo sit amet nulla. Donec non justo.',1),(42,'tempus non,',1),(43,'orci quis lectus. Nullam suscipit, est ac facilisis facilisis,',2),(44,'ornare lectus justo',1),(45,'lorem lorem, luctus ut, pellentesque',1),(46,'elit pede, malesuada vel, venenatis',2),(47,'scelerisque sed, sapien. Nunc pulvinar arcu et pede. Nunc sed',1),(48,'lectus, a sollicitudin',1),(49,'Maecenas libero est, congue a, aliquet vel, vulputate eu,',1),(50,'Duis dignissim tempor arcu. Vestibulum ut',1);
/*!40000 ALTER TABLE `bericht` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device` (
  `deviceid` int NOT NULL AUTO_INCREMENT,
  `Naam` varchar(50) DEFAULT NULL,
  `Merk` varchar(75) DEFAULT NULL,
  `Beschrijving` varchar(125) DEFAULT NULL,
  `Type` varchar(50) DEFAULT NULL,
  `Aankoopkost` double DEFAULT NULL,
  `Meeteenheid` varchar(3) DEFAULT NULL,
  PRIMARY KEY (`deviceid`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
INSERT INTO `device` VALUES (1,'Inez','scelerisque dui.','Donec vitae erat vel pede','semper',32,'°C'),(2,'Uma','nisl. Nulla','purus, accumsan','eu',28,'°C'),(3,'Chancellor','malesuada malesuada.','dolor vitae dolor. Donec fringilla. Donec feugiat','gravida.',20,'°C'),(4,'Troy','quam. Curabitur','risus. Quisque libero lacus, varius et, euismod et,','ultrices',8,'°C'),(5,'Yolanda','vitae semper','faucibus leo, in lobortis tellus justo','eget,',17,'°C'),(6,'Jared','risus, at','magnis dis parturient montes, nascetur ridiculus mus. Donec dignissim magna','vulputate,',39,'°C'),(7,'Germane','molestie arcu.','Donec vitae erat vel pede blandit congue. In scelerisque scelerisque','ipsum',35,'°C'),(8,'Karly','leo. Cras','rhoncus id, mollis nec, cursus a, enim. Suspendisse','lectus',41,'°C'),(9,'Lars','amet, risus.','magna, malesuada vel, convallis in, cursus et, eros.','neque.',15,'°C'),(10,'Harding','egestas. Sed','ac nulla.','Sed',18,'°C'),(11,'Yardley','ac urna.','eu lacus. Quisque imperdiet, erat nonummy ultricies ornare,','nisl.',20,'°C'),(12,'Jonah','accumsan interdum','commodo','Fusce',38,'°C'),(13,'Karina','vel, convallis','suscipit, est ac facilisis facilisis, magna tellus faucibus','Quisque',2,'°C'),(14,'Cailin','et libero.','non, luctus sit amet, faucibus ut, nulla. Cras eu','Phasellus',31,'°C'),(15,'Gannon','elementum at,','tincidunt orci quis lectus.','metus',18,'°C'),(16,'Colton','tincidunt vehicula','nulla magna, malesuada vel, convallis in, cursus et, eros.','elit,',6,'°C'),(17,'Iola','aliquam, enim','Nulla interdum. Curabitur','sit',13,'°C'),(18,'Imogene','Morbi vehicula.','molestie in, tempus eu, ligula.','augue,',2,'%'),(19,'Clark','consequat, lectus','euismod enim. Etiam gravida molestie arcu. Sed','turpis',4,'%'),(20,'Kenneth','Proin mi.','Aliquam auctor, velit','amet',5,'%'),(21,'Rose','risus. Quisque','Ut sagittis','non,',40,'%'),(22,'Margaret','feugiat tellus','magna nec quam. Curabitur vel lectus.','rutrum',16,'%'),(23,'Cameran','magna. Nam','elementum purus, accumsan interdum libero dui','In',37,'%'),(24,'Wallace','Pellentesque ultricies','facilisis lorem tristique aliquet. Phasellus','eget',40,'%'),(25,'Lamar','mollis vitae,','arcu. Curabitur ut odio vel est','vulputate',28,'%'),(26,'Shoshana','blandit enim','nisi magna sed','ipsum',48,'%'),(27,'Benjamin','non enim.','sociosqu ad litora torquent per conubia nostra,','nisi.',29,'%'),(28,'Ryan','Nunc mauris','in lobortis tellus justo sit amet nulla. Donec non justo.','auctor',7,'%'),(29,'Lester','lacus. Quisque','eu, accumsan sed, facilisis vitae, orci.','rutrum',35,'%'),(30,'Shelly','eget tincidunt','sed leo. Cras vehicula aliquet libero. Integer in','euismod',39,'%'),(31,'Kato','libero est,','adipiscing ligula. Aenean','non',43,'%'),(32,'Kevyn','Quisque imperdiet,','id ante dictum cursus. Nunc mauris','ut',41,'%'),(33,'Keelie','Lorem ipsum','suscipit, est ac facilisis','eget',40,'%'),(34,'Avram','neque et','sagittis lobortis mauris. Suspendisse aliquet molestie tellus. Aenean egestas hendrerit','vitae',42,'%'),(35,'Hyatt','In ornare','sodales elit erat vitae','neque',7,'%'),(36,'Yuli','ornare tortor','Nunc lectus pede, ultrices a, auctor non, feugiat nec, diam.','ligula.',40,'%'),(37,'Dahlia','amet ornare','scelerisque mollis. Phasellus libero mauris, aliquam eu, accumsan','risus',22,'°C'),(38,'Shafira','id magna','Vivamus euismod','nascetur',36,'°C'),(39,'Ariana','ultrices a,','semper egestas, urna justo faucibus lectus, a sollicitudin orci sem','sit',17,'°C'),(40,'Hayes','Duis cursus,','felis ullamcorper viverra. Maecenas iaculis','ligula',38,'°C'),(41,'Florence','consectetuer adipiscing','non','dictum',44,'°C'),(42,'Rajah','imperdiet nec,','est, vitae sodales nisi','ultrices.',8,'°C'),(43,'Grant','Cras sed','velit. Quisque','Donec',32,'°C'),(44,'Mufutau','ac turpis','a, arcu. Sed','dolor',8,'°C'),(45,'Simone','Sed congue,','hendrerit consectetuer, cursus et, magna. Praesent interdum','ac',35,'°C'),(46,'Dieter','eleifend non,','mus. Proin vel','dignissim',16,'°C'),(47,'Reese','scelerisque neque.','fames ac turpis egestas. Fusce aliquet','tempus',31,'°C'),(48,'Alexa','Nunc ut','felis ullamcorper viverra.','nulla.',14,'°C'),(49,'Ulric','accumsan convallis,','Nullam velit dui, semper et, lacinia vitae, sodales at,','magnis',32,'°C'),(50,'Galena','ipsum. Suspendisse','sit amet diam eu dolor egestas rhoncus. Proin nisl','vel,',33,'°C');
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gebruiker`
--

DROP TABLE IF EXISTS `gebruiker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gebruiker` (
  `gebruikerid` int NOT NULL,
  `naam` varchar(75) DEFAULT NULL,
  PRIMARY KEY (`gebruikerid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gebruiker`
--

LOCK TABLES `gebruiker` WRITE;
/*!40000 ALTER TABLE `gebruiker` DISABLE KEYS */;
INSERT INTO `gebruiker` VALUES (1,'Gregory'),(2,'Alden');
/*!40000 ALTER TABLE `gebruiker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historiek`
--

DROP TABLE IF EXISTS `historiek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historiek` (
  `volgnummer` int NOT NULL AUTO_INCREMENT,
  `Device_deviceid` int DEFAULT NULL,
  `actie_actieid` int NOT NULL,
  `bericht_berichtid` int DEFAULT NULL,
  `datum` datetime DEFAULT NULL,
  `waarde` double DEFAULT NULL,
  `commentaar` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`volgnummer`,`actie_actieid`),
  KEY `fk_Historiek_Device_idx` (`Device_deviceid`),
  KEY `fk_Historiek_bericht1_idx` (`bericht_berichtid`),
  KEY `fk_Historiek_actie1_idx` (`actie_actieid`),
  CONSTRAINT `fk_Historiek_actie1` FOREIGN KEY (`actie_actieid`) REFERENCES `actie` (`actieid`),
  CONSTRAINT `fk_Historiek_bericht1` FOREIGN KEY (`bericht_berichtid`) REFERENCES `bericht` (`berichtid`),
  CONSTRAINT `fk_Historiek_Device` FOREIGN KEY (`Device_deviceid`) REFERENCES `device` (`deviceid`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historiek`
--

LOCK TABLES `historiek` WRITE;
/*!40000 ALTER TABLE `historiek` DISABLE KEYS */;
INSERT INTO `historiek` VALUES (1,46,44,33,'2021-02-07 23:13:55',59,'auctor odio a purus. Duis'),(2,34,18,37,'2021-05-12 04:48:03',66,'pede, malesuada vel,'),(3,30,47,33,'2021-05-20 22:25:29',71,'commodo tincidunt nibh. Phasellus nulla. Integer vulputate, risus a'),(4,17,42,13,'2021-01-10 02:27:18',13,'sed turpis nec mauris blandit mattis. Cras eget'),(5,22,15,20,'2021-05-02 08:16:20',3,'urna convallis erat, eget tincidunt dui augue eu tellus. Phasellus'),(6,46,44,9,'2021-04-24 18:35:09',25,'malesuada ut, sem. Nulla interdum. Curabitur dictum.'),(7,36,14,25,'2021-05-22 10:52:11',97,'semper auctor.'),(8,48,26,32,'2021-05-16 13:12:35',2,'Pellentesque habitant morbi tristique senectus'),(9,35,20,40,'2021-05-02 18:45:11',43,'elit sed consequat auctor, nunc nulla vulputate dui,'),(10,25,3,7,'2021-05-07 10:50:22',7,'elit. Etiam laoreet, libero et tristique'),(11,46,8,8,'2021-01-24 00:47:40',84,'pharetra sed, hendrerit a,'),(12,13,30,29,'2021-01-19 10:19:27',89,'Sed diam lorem, auctor'),(13,42,37,46,'2021-01-09 21:07:07',49,'sodales elit erat vitae risus.'),(14,29,32,45,'2021-05-04 18:02:56',82,'massa. Suspendisse eleifend. Cras sed'),(15,12,25,36,'2021-04-28 20:39:56',63,'Proin ultrices. Duis'),(16,27,42,35,'2021-05-16 07:17:31',41,'a, auctor non, feugiat nec, diam.'),(17,48,16,7,'2021-05-12 05:07:44',63,'ut eros non enim'),(18,10,11,10,'2021-04-26 00:38:46',74,'facilisis eget, ipsum. Donec sollicitudin adipiscing ligula. Aenean'),(19,18,50,11,'2021-05-12 05:05:44',19,'at sem molestie'),(20,46,46,27,'2021-01-07 16:28:10',38,'sit amet'),(21,38,8,2,'2021-03-07 02:09:16',99,'consectetuer rhoncus.'),(22,3,20,47,'2021-03-04 01:48:49',60,'dolor, nonummy ac, feugiat non, lobortis quis,'),(23,22,36,34,'2021-04-29 10:20:30',31,'luctus et ultrices posuere cubilia Curae'),(24,41,50,30,'2021-05-14 03:26:47',97,'Sed diam lorem,'),(25,45,27,32,'2021-04-22 12:55:54',26,'scelerisque scelerisque dui. Suspendisse ac metus'),(26,2,34,46,'2021-03-31 12:34:35',96,'lacus. Quisque imperdiet, erat nonummy ultricies'),(27,5,15,36,'2021-01-07 11:56:23',45,'euismod est arcu ac orci. Ut'),(28,19,25,3,'2021-04-07 12:43:06',98,'et, magna. Praesent interdum ligula eu enim. Etiam imperdiet'),(29,11,44,31,'2021-04-06 11:47:19',86,'nibh. Donec est'),(30,45,12,34,'2021-01-31 01:07:55',93,'In at pede. Cras vulputate velit eu sem.'),(31,41,48,36,'2021-02-11 17:03:26',41,'fermentum risus,'),(32,14,11,16,'2021-05-19 04:59:49',45,'ac urna. Ut tincidunt vehicula risus.'),(33,48,5,21,'2021-04-01 04:40:11',77,'sit amet risus. Donec egestas. Aliquam nec enim.'),(34,23,20,16,'2021-04-15 07:57:39',41,'in faucibus orci luctus et ultrices posuere cubilia Curae Donec'),(35,27,21,44,'2021-02-01 18:56:07',7,'scelerisque, lorem'),(36,48,42,37,'2021-03-05 15:32:23',14,'ornare placerat, orci lacus vestibulum'),(37,18,35,4,'2021-01-30 17:00:08',57,'vel arcu eu odio tristique'),(38,50,44,14,'2021-01-06 18:03:56',71,'risus. Morbi metus. Vivamus euismod urna. Nullam lobortis'),(39,3,32,25,'2021-05-01 17:42:37',18,'lectus pede et risus. Quisque libero lacus, varius'),(40,10,45,40,'2021-04-17 17:30:30',44,'dictum magna. Ut tincidunt orci quis lectus. Nullam suscipit, est'),(41,32,10,26,'2021-04-07 08:57:15',19,'nec, euismod in, dolor.'),(42,36,38,5,'2021-04-28 22:19:15',56,'cursus et, magna. Praesent interdum ligula eu enim.'),(43,14,29,43,'2021-02-14 10:27:24',72,'ligula. Donec luctus aliquet odio. Etiam ligula'),(44,17,15,28,'2021-02-05 00:12:59',3,'vulputate eu, odio. Phasellus at'),(45,48,38,17,'2021-05-20 21:59:55',96,'dolor. Nulla semper tellus id nunc interdum feugiat. Sed'),(46,49,24,11,'2021-02-17 10:07:51',51,'purus ac'),(47,31,17,16,'2021-03-07 01:40:38',48,'Aliquam erat volutpat. Nulla facilisis. Suspendisse commodo'),(48,29,20,36,'2021-02-08 07:28:03',36,'venenatis lacus. Etiam bibendum fermentum metus. Aenean sed pede'),(49,33,8,42,'2021-01-10 17:44:23',38,'a, malesuada id, erat. Etiam vestibulum massa'),(50,15,34,6,'2021-02-13 14:52:48',95,'nulla. Integer urna. Vivamus molestie dapibus ligula. Aliquam');
/*!40000 ALTER TABLE `historiek` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-23 17:26:32
