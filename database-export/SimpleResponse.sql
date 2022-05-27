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
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actie`
--

LOCK TABLES `actie` WRITE;
/*!40000 ALTER TABLE `actie` DISABLE KEYS */;
INSERT INTO `actie` VALUES (1,'Temparatuur uitlezen'),(2,'Licht uitlezen'),(3,'Joystick uitlezen'),(4,'RGB leds aan'),(5,'RGB leds uit'),(6,'RGB leds kleur veranderen'),(7,'Ventilator aan'),(8,'ventilator uit'),(9,'Status veranderen knop'),(10,'Bericht sturen naar lcd'),(11,'Bericht sturen naar website');
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bericht`
--

LOCK TABLES `bericht` WRITE;
/*!40000 ALTER TABLE `bericht` DISABLE KEYS */;
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
  `naam` varchar(50) DEFAULT NULL,
  `merk` varchar(75) DEFAULT NULL,
  `beschrijving` varchar(125) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `aankoopkost` double DEFAULT NULL,
  `meeteenheid` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`deviceid`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
INSERT INTO `device` VALUES (1,'One Wire','Maxim Integrated','1-wire temperatuur sensor (DS18B20)','Sensor',5.32,'°C'),(2,'LDR','Advanced Photonix','Lichtsensor (NSL 19M51 )','Sensor',1.95,'%'),(3,'Joystick module','Joy-it','Joystick (COM-KY023JM )','Sensor',1.59,'°'),(4,'RGB-led','Lucky Light','RGB led common anode','Actuator',1.82,'null'),(7,'Drukknop','null','Drukknop','Actuator',1.95,'null'),(8,'Tuimelschakelaar','Elear','Tuimelschakelaar voor pi af te sluiten (EP290B)','Actuator',1,'null'),(9,'Ventilator','Sunon','12v 80x80 ventilator (CY 205N )','Actuator',5.99,'null');
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gebruiker`
--

DROP TABLE IF EXISTS `gebruiker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gebruiker` (
  `gebruikerid` int NOT NULL AUTO_INCREMENT,
  `naam` varchar(75) DEFAULT NULL,
  PRIMARY KEY (`gebruikerid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gebruiker`
--

LOCK TABLES `gebruiker` WRITE;
/*!40000 ALTER TABLE `gebruiker` DISABLE KEYS */;
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
  `device_deviceid` int DEFAULT NULL,
  `actie_actieid` int NOT NULL,
  `bericht_berichtid` int DEFAULT NULL,
  `datum` datetime DEFAULT NULL,
  `waarde` double DEFAULT NULL,
  `commentaar` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`volgnummer`,`actie_actieid`),
  KEY `fk_Historiek_Device_idx` (`device_deviceid`),
  KEY `fk_Historiek_bericht1_idx` (`bericht_berichtid`),
  KEY `fk_Historiek_actie1_idx` (`actie_actieid`),
  CONSTRAINT `fk_Historiek_actie1` FOREIGN KEY (`actie_actieid`) REFERENCES `actie` (`actieid`),
  CONSTRAINT `fk_Historiek_bericht1` FOREIGN KEY (`bericht_berichtid`) REFERENCES `bericht` (`berichtid`),
  CONSTRAINT `fk_Historiek_Device` FOREIGN KEY (`device_deviceid`) REFERENCES `device` (`deviceid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historiek`
--

LOCK TABLES `historiek` WRITE;
/*!40000 ALTER TABLE `historiek` DISABLE KEYS */;
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

-- Dump completed on 2022-05-27 18:43:08
