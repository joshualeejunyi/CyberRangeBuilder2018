CREATE DATABASE  IF NOT EXISTS `CRB` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `CRB`;
-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: localhost    Database: CRB
-- ------------------------------------------------------
-- Server version	5.7.22-0ubuntu0.16.04.1

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
-- Table structure for table `Group`
--

DROP TABLE IF EXISTS `Group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Group` (
  `groupID` int(11) NOT NULL AUTO_INCREMENT,
  `groupName` varchar(45) NOT NULL,
  `dateCreated` date DEFAULT NULL,
  `timeCreated` time(6) DEFAULT NULL,
  `groupPoints` int(11) DEFAULT NULL,
  `lastModifiedDate` date DEFAULT NULL,
  `lastModifiedTime` time(6) DEFAULT NULL,
  `createdBy` varchar(254) DEFAULT NULL,
  `groupLeader` varchar(254) DEFAULT NULL,
  `lastModifiedBy` varchar(254) DEFAULT NULL,
  PRIMARY KEY (`groupID`),
  UNIQUE KEY `groupName` (`groupName`),
  KEY `Group_createdBy_e8a86322_fk_User_email` (`createdBy`),
  KEY `Group_groupLeader_dda63499_fk_User_email` (`groupLeader`),
  KEY `Group_lastModifiedBy_2b8379dc_fk_User_email` (`lastModifiedBy`),
  CONSTRAINT `Group_createdBy_e8a86322_fk_User_email` FOREIGN KEY (`createdBy`) REFERENCES `User` (`email`),
  CONSTRAINT `Group_groupLeader_dda63499_fk_User_email` FOREIGN KEY (`groupLeader`) REFERENCES `User` (`email`),
  CONSTRAINT `Group_lastModifiedBy_2b8379dc_fk_User_email` FOREIGN KEY (`lastModifiedBy`) REFERENCES `User` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Group`
--

LOCK TABLES `Group` WRITE;
/*!40000 ALTER TABLE `Group` DISABLE KEYS */;
INSERT INTO `Group` VALUES (1,'bestgroup','2018-07-11','00:46:10.654321',0,NULL,NULL,'karlkwan@gmail.com','joshualee@gmail.com',NULL),(2,'group','2018-07-12','14:47:03.516580',0,NULL,NULL,'karlkwan@gmail.com',NULL,NULL);
/*!40000 ALTER TABLE `Group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `GroupRange`
--

DROP TABLE IF EXISTS `GroupRange`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GroupRange` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `dateCreated` date DEFAULT NULL,
  `timeCreated` time(6) DEFAULT NULL,
  `groupRangePoints` int(11) DEFAULT NULL,
  `addedBy` varchar(254) DEFAULT NULL,
  `groupID` int(11) NOT NULL,
  `rangeID` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `GroupRange_addedBy_3485f07a_fk_User_email` (`addedBy`),
  KEY `GroupRange_groupID_1897bfba_fk_Group_groupID` (`groupID`),
  KEY `GroupRange_rangeID_834b66ea_fk_Range_rangeID` (`rangeID`),
  CONSTRAINT `GroupRange_addedBy_3485f07a_fk_User_email` FOREIGN KEY (`addedBy`) REFERENCES `User` (`email`),
  CONSTRAINT `GroupRange_groupID_1897bfba_fk_Group_groupID` FOREIGN KEY (`groupID`) REFERENCES `Group` (`groupID`),
  CONSTRAINT `GroupRange_rangeID_834b66ea_fk_Range_rangeID` FOREIGN KEY (`rangeID`) REFERENCES `Range` (`rangeID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `GroupRange`
--

LOCK TABLES `GroupRange` WRITE;
/*!40000 ALTER TABLE `GroupRange` DISABLE KEYS */;
/*!40000 ALTER TABLE `GroupRange` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MCQOptions`
--

DROP TABLE IF EXISTS `MCQOptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MCQOptions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `OptionOne` varchar(100) NOT NULL,
  `OptionTwo` varchar(100) NOT NULL,
  `OptionThree` varchar(100) NOT NULL,
  `OptionFour` varchar(100) NOT NULL,
  `questionid` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `MCQOptions_questionid_3371087c_uniq` (`questionid`),
  CONSTRAINT `MCQOptions_questionid_3371087c_fk_Questions_questionID` FOREIGN KEY (`questionid`) REFERENCES `Questions` (`questionID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MCQOptions`
--

LOCK TABLES `MCQOptions` WRITE;
/*!40000 ALTER TABLE `MCQOptions` DISABLE KEYS */;
INSERT INTO `MCQOptions` VALUES (1,'mcq','halp','bye','hay',3);
/*!40000 ALTER TABLE `MCQOptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `QuestionTopic`
--

DROP TABLE IF EXISTS `QuestionTopic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `QuestionTopic` (
  `topicid` int(11) NOT NULL AUTO_INCREMENT,
  `topicname` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`topicid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `QuestionTopic`
--

LOCK TABLES `QuestionTopic` WRITE;
/*!40000 ALTER TABLE `QuestionTopic` DISABLE KEYS */;
INSERT INTO `QuestionTopic` VALUES (1,'newtopic'),(2,'too hot salted egg'),(3,'testtopic'),(4,'flagtopic'),(5,'mcqtopic'),(6,'shortanswertopic'),(7,'openended'),(8,'truorfarlse');
/*!40000 ALTER TABLE `QuestionTopic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Questions`
--

DROP TABLE IF EXISTS `Questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Questions` (
  `questionID` int(11) NOT NULL AUTO_INCREMENT,
  `questiontype` varchar(100) NOT NULL,
  `questiontitle` varchar(255) DEFAULT NULL,
  `questiontext` longtext NOT NULL,
  `hint` longtext NOT NULL,
  `topicid` int(11) DEFAULT NULL,
  `usedocker` tinyint(1) NOT NULL,
  `createdby` varchar(254) DEFAULT NULL,
  `dateCreated` date DEFAULT NULL,
  `timecreated` time(6) DEFAULT NULL,
  PRIMARY KEY (`questionID`),
  KEY `Questions_topicid_f463268f_fk_QuestionTopic_topicid` (`topicid`),
  KEY `Questions_createdby_43a92c1c_fk_User_email` (`createdby`),
  CONSTRAINT `Questions_createdby_43a92c1c_fk_User_email` FOREIGN KEY (`createdby`) REFERENCES `User` (`email`),
  CONSTRAINT `Questions_topicid_f463268f_fk_QuestionTopic_topicid` FOREIGN KEY (`topicid`) REFERENCES `QuestionTopic` (`topicid`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Questions`
--

LOCK TABLES `Questions` WRITE;
/*!40000 ALTER TABLE `Questions` DISABLE KEYS */;
INSERT INTO `Questions` VALUES (1,'FL','test','test','test',1,1,'karlkwan@gmail.com','2018-07-11','15:07:10.277354'),(2,'FL','this is a flag question','this is a flag text','flag',4,0,'karlkwan@gmail.com','2018-07-11','17:33:48.901609'),(3,'MCQ','this is an mcq title','this is an mcq text','mcq',5,1,'karlkwan@gmail.com','2018-07-11','17:34:16.463635'),(4,'SA','this is a short answer','short answer text','short',6,1,'karlkwan@gmail.com','2018-07-11','17:35:03.456095'),(5,'OE','openendedbro','what is open','open',7,1,'karlkwan@gmail.com','2018-07-11','17:35:31.337931'),(6,'TF','this is true','this is false','what is tf',8,1,'karlkwan@gmail.com','2018-07-11','17:36:03.295252');
/*!40000 ALTER TABLE `Questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Range`
--

DROP TABLE IF EXISTS `Range`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Range` (
  `rangeID` int(11) NOT NULL AUTO_INCREMENT,
  `rangeName` varchar(45) NOT NULL,
  `createdby` varchar(254) NOT NULL,
  `dateCreated` date DEFAULT NULL,
  `dateEnd` date DEFAULT NULL,
  `dateStart` date DEFAULT NULL,
  `isDisabled` tinyint(1) NOT NULL,
  `lastModifiedBy` varchar(254) DEFAULT NULL,
  `lastModifiedDate` date DEFAULT NULL,
  `maxScore` int(11) DEFAULT NULL,
  `rangeActive` tinyint(1) NOT NULL,
  `rangeCode` int(11) DEFAULT NULL,
  `rangeURL` varchar(50) DEFAULT NULL,
  `studentsInRange` int(11) DEFAULT NULL,
  `timeEnd` time(6) DEFAULT NULL,
  `timeStart` time(6) DEFAULT NULL,
  `isOpen` tinyint(1) NOT NULL,
  PRIMARY KEY (`rangeID`),
  UNIQUE KEY `rangeCode` (`rangeCode`),
  UNIQUE KEY `Range_rangeURL_a80344a3_uniq` (`rangeURL`),
  KEY `Range_createdby_4d2f29e0_fk_User_email` (`createdby`),
  KEY `Range_lastModifiedBy_35f0a21b_fk_User_email` (`lastModifiedBy`),
  CONSTRAINT `Range_createdby_4d2f29e0_fk_User_email` FOREIGN KEY (`createdby`) REFERENCES `User` (`email`),
  CONSTRAINT `Range_lastModifiedBy_35f0a21b_fk_User_email` FOREIGN KEY (`lastModifiedBy`) REFERENCES `User` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Range`
--

LOCK TABLES `Range` WRITE;
/*!40000 ALTER TABLE `Range` DISABLE KEYS */;
INSERT INTO `Range` VALUES (23,'Cyber Range #1','karlkwan@gmail.com','2018-07-11','2019-08-12','2018-07-12',0,'karlkwan@gmail.com','2018-07-12',50,1,998658,'testrange',NULL,'11:59:00.000000','10:49:00.000000',1),(24,'testrange','karlkwan@gmail.com','2018-07-12',NULL,NULL,0,NULL,NULL,NULL,1,682327,'newnewrange',NULL,NULL,NULL,1);
/*!40000 ALTER TABLE `Range` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RangeQuestions`
--

DROP TABLE IF EXISTS `RangeQuestions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `RangeQuestions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `answer` varchar(255) DEFAULT NULL,
  `questionID` int(11) NOT NULL,
  `rangeID` int(11) NOT NULL,
  `isDisabled` tinyint(1) NOT NULL,
  `points` int(11) NOT NULL,
  `registryID` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `RangeQuestions_questionID_b51c40c3_fk_Questions_questionID` (`questionID`),
  KEY `RangeQuestions_rangeID_4ec72b4b_fk_Range_rangeID` (`rangeID`),
  CONSTRAINT `RangeQuestions_questionID_b51c40c3_fk_Questions_questionID` FOREIGN KEY (`questionID`) REFERENCES `Questions` (`questionID`),
  CONSTRAINT `RangeQuestions_rangeID_4ec72b4b_fk_Range_rangeID` FOREIGN KEY (`rangeID`) REFERENCES `Range` (`rangeID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RangeQuestions`
--

LOCK TABLES `RangeQuestions` WRITE;
/*!40000 ALTER TABLE `RangeQuestions` DISABLE KEYS */;
INSERT INTO `RangeQuestions` VALUES (2,'flag',2,23,0,10,'flag'),(3,'mcq',3,23,0,10,''),(4,'this is a short answer',4,23,0,10,'short'),(5,'open',5,23,0,10,''),(6,'True',6,23,0,10,'tf');
/*!40000 ALTER TABLE `RangeQuestions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RangeStudents`
--

DROP TABLE IF EXISTS `RangeStudents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `RangeStudents` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dateJoined` datetime(6) DEFAULT NULL,
  `progress` int(11) DEFAULT NULL,
  `points` int(11) NOT NULL,
  `dateCompleted` date DEFAULT NULL,
  `timeCompleted` time(6) DEFAULT NULL,
  `lastaccess` datetime(6) DEFAULT NULL,
  `rangeID` int(11) NOT NULL,
  `email` varchar(254) NOT NULL,
  `groupid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `RangeStudents_rangeID_bc51c70c_fk_Range_rangeID` (`rangeID`),
  KEY `RangeStudents_email_af1dd9e3_fk_User_email` (`email`),
  KEY `RangeStudents_groupid_f7d179b4_fk_Group_groupID` (`groupid`),
  CONSTRAINT `RangeStudents_email_af1dd9e3_fk_User_email` FOREIGN KEY (`email`) REFERENCES `User` (`email`),
  CONSTRAINT `RangeStudents_groupid_f7d179b4_fk_Group_groupID` FOREIGN KEY (`groupid`) REFERENCES `Group` (`groupID`),
  CONSTRAINT `RangeStudents_rangeID_bc51c70c_fk_Range_rangeID` FOREIGN KEY (`rangeID`) REFERENCES `Range` (`rangeID`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RangeStudents`
--

LOCK TABLES `RangeStudents` WRITE;
/*!40000 ALTER TABLE `RangeStudents` DISABLE KEYS */;
INSERT INTO `RangeStudents` VALUES (17,'2018-07-10 16:00:00.000000',NULL,0,NULL,NULL,NULL,23,'dextergui@gmail.com',NULL),(18,'2018-07-10 16:00:00.000000',NULL,0,NULL,NULL,NULL,23,'dextergui@gmail.com',1),(19,'2018-07-10 16:00:00.000000',NULL,40,NULL,NULL,NULL,23,'joshualee@gmail.com',1);
/*!40000 ALTER TABLE `RangeStudents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudentGroup`
--

DROP TABLE IF EXISTS `StudentGroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `StudentGroup` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `groupID` int(11) NOT NULL,
  `studentID` varchar(254) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `StudentGroup_groupID_45126783_fk_Group_groupID` (`groupID`),
  KEY `StudentGroup_studentID_0165a6d1_fk_User_email` (`studentID`),
  CONSTRAINT `StudentGroup_groupID_45126783_fk_Group_groupID` FOREIGN KEY (`groupID`) REFERENCES `Group` (`groupID`),
  CONSTRAINT `StudentGroup_studentID_0165a6d1_fk_User_email` FOREIGN KEY (`studentID`) REFERENCES `User` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentGroup`
--

LOCK TABLES `StudentGroup` WRITE;
/*!40000 ALTER TABLE `StudentGroup` DISABLE KEYS */;
INSERT INTO `StudentGroup` VALUES (1,1,'dextergui@gmail.com'),(2,1,'joshualee@gmail.com');
/*!40000 ALTER TABLE `StudentGroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudentQuestions`
--

DROP TABLE IF EXISTS `StudentQuestions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `StudentQuestions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `answergiven` varchar(100) NOT NULL,
  `right/wrong` tinyint(1) NOT NULL,
  `marksawarded` int(11) NOT NULL,
  `questionid` int(11) NOT NULL,
  `rangeID` int(11) NOT NULL,
  `email` varchar(254) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `StudentQuestions_questionid_a35630ff_fk_Questions_questionID` (`questionid`),
  KEY `StudentQuestions_rangeID_828774ff_fk_Range_rangeID` (`rangeID`),
  KEY `StudentQuestions_email_18d1090a_fk_User_email` (`email`),
  CONSTRAINT `StudentQuestions_email_18d1090a_fk_User_email` FOREIGN KEY (`email`) REFERENCES `User` (`email`),
  CONSTRAINT `StudentQuestions_questionid_a35630ff_fk_Questions_questionID` FOREIGN KEY (`questionid`) REFERENCES `Questions` (`questionID`),
  CONSTRAINT `StudentQuestions_rangeID_828774ff_fk_Range_rangeID` FOREIGN KEY (`rangeID`) REFERENCES `Range` (`rangeID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentQuestions`
--

LOCK TABLES `StudentQuestions` WRITE;
/*!40000 ALTER TABLE `StudentQuestions` DISABLE KEYS */;
INSERT INTO `StudentQuestions` VALUES (1,'flag',1,10,2,23,'joshualee@gmail.com'),(2,'mcq',1,10,3,23,'joshualee@gmail.com'),(3,'this is short answer',1,10,4,23,'joshualee@gmail.com'),(4,'True',1,10,6,23,'joshualee@gmail.com'),(5,'asdfdsagads',0,10,5,23,'joshualee@gmail.com');
/*!40000 ALTER TABLE `StudentQuestions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UnavailablePorts`
--

DROP TABLE IF EXISTS `UnavailablePorts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UnavailablePorts` (
  `portNumber` int(11) NOT NULL,
  `containerName` longtext,
  `dateTimeCreated` datetime(6) DEFAULT NULL,
  `studentid` varchar(254) NOT NULL,
  PRIMARY KEY (`portNumber`),
  KEY `UnavailablePorts_studentid_6dc5be5e_fk_User_email` (`studentid`),
  CONSTRAINT `UnavailablePorts_studentid_6dc5be5e_fk_User_email` FOREIGN KEY (`studentid`) REFERENCES `User` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UnavailablePorts`
--

LOCK TABLES `UnavailablePorts` WRITE;
/*!40000 ALTER TABLE `UnavailablePorts` DISABLE KEYS */;
/*!40000 ALTER TABLE `UnavailablePorts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User` (
  `email` varchar(254) NOT NULL,
  `username` varchar(45) NOT NULL,
  `password` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `dateJoined` date DEFAULT NULL,
  `lastModifiedDate` date DEFAULT NULL,
  `lastlogin` datetime(6) DEFAULT NULL,
  `teacher` tinyint(1) NOT NULL,
  `acceptedBy` varchar(254) DEFAULT NULL,
  `admin` tinyint(1) NOT NULL,
  `lastModifiedBy` varchar(254) DEFAULT NULL,
  `lastModifiedTime` time(6) DEFAULT NULL,
  `userclass` varchar(45),
  `isdisabled` tinyint(1) NOT NULL,
  `isaccepted` tinyint(1) NOT NULL,
  PRIMARY KEY (`email`),
  UNIQUE KEY `username` (`username`),
  KEY `User_acceptedBy_5736f442_fk_User_email` (`acceptedBy`),
  KEY `User_lastModifiedBy_44c68aab_fk_User_email` (`lastModifiedBy`),
  CONSTRAINT `User_acceptedBy_5736f442_fk_User_email` FOREIGN KEY (`acceptedBy`) REFERENCES `User` (`email`),
  CONSTRAINT `User_lastModifiedBy_44c68aab_fk_User_email` FOREIGN KEY (`lastModifiedBy`) REFERENCES `User` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES ('dextergui@gmail.com','dextergui','pbkdf2_sha256$100000$MfS05tzi2e5j$gTrK2GYr5vyuZrZkoBnz4bYqM7qfqVlhhzf20Xl7o4s=','Dexter Gui Zhang Yan','2018-07-06','2018-07-06','2018-07-06 05:14:14.756719',0,'karlkwan@gmail.com',0,'karlkwan@gmail.com','13:23:10.090459','Public',0,1),('joshualee@gmail.com','joshualee','pbkdf2_sha256$100000$iBTzRCRhCNKa$IoWGcT6HHNeWkIhyT/XQCMWLxLM0YbEwpzTDXsllOYg=','Joshua Lee','2018-07-05','2018-07-05','2018-07-12 07:07:56.392067',0,'karlkwan@gmail.com',0,'karlkwan@gmail.com','22:51:15.857256','Public',0,1),('karlkwan@gmail.com','karlkwan','pbkdf2_sha256$100000$DSALuUqOXFXz$rThfj7tZp3t+TjZCFjoHwZyfsGpMoNTNSygpQaf1Qis=','Karl Kwan','2018-07-05',NULL,'2018-07-12 06:44:45.735514',1,NULL,1,NULL,NULL,'Public',0,1),('wesleychiau@gmail.com','wesleychiau','pbkdf2_sha256$100000$rwohe0hLTBlZ$rH412j2Z3xtEAkvCGQELP9XgOLbUV4ZUFUkfwmfWX3I=','Wesley Chiau','2018-07-06','2018-07-06',NULL,0,'karlkwan@gmail.com',0,'karlkwan@gmail.com','12:37:42.278187','Public',0,1);
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UserClass`
--

DROP TABLE IF EXISTS `UserClass`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UserClass` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `class` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UserClass`
--

LOCK TABLES `UserClass` WRITE;
/*!40000 ALTER TABLE `UserClass` DISABLE KEYS */;
INSERT INTO `UserClass` VALUES (1,'Public');
/*!40000 ALTER TABLE `UserClass` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User_groups`
--

DROP TABLE IF EXISTS `User_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(254) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `User_groups_user_id_group_id_d63e199e_uniq` (`user_id`,`group_id`),
  KEY `User_groups_group_id_328392a3_fk_auth_group_id` (`group_id`),
  CONSTRAINT `User_groups_group_id_328392a3_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `User_groups_user_id_8f675f72_fk_User_email` FOREIGN KEY (`user_id`) REFERENCES `User` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User_groups`
--

LOCK TABLES `User_groups` WRITE;
/*!40000 ALTER TABLE `User_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `User_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User_user_permissions`
--

DROP TABLE IF EXISTS `User_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(254) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `User_user_permissions_user_id_permission_id_af0f54ec_uniq` (`user_id`,`permission_id`),
  KEY `User_user_permission_permission_id_8e998ba4_fk_auth_perm` (`permission_id`),
  CONSTRAINT `User_user_permission_permission_id_8e998ba4_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `User_user_permissions_user_id_2c6da4d4_fk_User_email` FOREIGN KEY (`user_id`) REFERENCES `User` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User_user_permissions`
--

LOCK TABLES `User_user_permissions` WRITE;
/*!40000 ALTER TABLE `User_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `User_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add group',1,'add_group'),(2,'Can change group',1,'change_group'),(3,'Can delete group',1,'delete_group'),(4,'Can add user class',2,'add_userclass'),(5,'Can change user class',2,'change_userclass'),(6,'Can delete user class',2,'delete_userclass'),(7,'Can add group range',3,'add_grouprange'),(8,'Can change group range',3,'change_grouprange'),(9,'Can delete group range',3,'delete_grouprange'),(10,'Can add student group',4,'add_studentgroup'),(11,'Can change student group',4,'change_studentgroup'),(12,'Can delete student group',4,'delete_studentgroup'),(13,'Can add user',5,'add_user'),(14,'Can change user',5,'change_user'),(15,'Can delete user',5,'delete_user'),(16,'Can add student questions',6,'add_studentquestions'),(17,'Can change student questions',6,'change_studentquestions'),(18,'Can delete student questions',6,'delete_studentquestions'),(19,'Can add mcq options',7,'add_mcqoptions'),(20,'Can change mcq options',7,'change_mcqoptions'),(21,'Can delete mcq options',7,'delete_mcqoptions'),(22,'Can add range students',8,'add_rangestudents'),(23,'Can change range students',8,'change_rangestudents'),(24,'Can delete range students',8,'delete_rangestudents'),(25,'Can add questions',9,'add_questions'),(26,'Can change questions',9,'change_questions'),(27,'Can delete questions',9,'delete_questions'),(28,'Can add range',10,'add_range'),(29,'Can change range',10,'change_range'),(30,'Can delete range',10,'delete_range'),(31,'Can add question topic',11,'add_questiontopic'),(32,'Can change question topic',11,'change_questiontopic'),(33,'Can delete question topic',11,'delete_questiontopic'),(34,'Can add unavailable ports',12,'add_unavailableports'),(35,'Can change unavailable ports',12,'change_unavailableports'),(36,'Can delete unavailable ports',12,'delete_unavailableports'),(37,'Can add range questions',13,'add_rangequestions'),(38,'Can change range questions',13,'change_rangequestions'),(39,'Can delete range questions',13,'delete_rangequestions'),(40,'Can add log entry',14,'add_logentry'),(41,'Can change log entry',14,'change_logentry'),(42,'Can delete log entry',14,'delete_logentry'),(43,'Can add permission',15,'add_permission'),(44,'Can change permission',15,'change_permission'),(45,'Can delete permission',15,'delete_permission'),(46,'Can add group',16,'add_group'),(47,'Can change group',16,'change_group'),(48,'Can delete group',16,'delete_group'),(49,'Can add content type',17,'add_contenttype'),(50,'Can change content type',17,'change_contenttype'),(51,'Can delete content type',17,'delete_contenttype'),(52,'Can add session',18,'add_session'),(53,'Can change session',18,'change_session'),(54,'Can delete session',18,'delete_session'),(55,'Can add fake student group',19,'add_fakestudentgroup'),(56,'Can change fake student group',19,'change_fakestudentgroup'),(57,'Can delete fake student group',19,'delete_fakestudentgroup'),(58,'Can add fake range',20,'add_fakerange'),(59,'Can change fake range',20,'change_fakerange'),(60,'Can delete fake range',20,'delete_fakerange');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` varchar(254) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_User_email` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_User_email` FOREIGN KEY (`user_id`) REFERENCES `User` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (19,'accounts','fakestudentgroup'),(1,'accounts','group'),(3,'accounts','grouprange'),(4,'accounts','studentgroup'),(5,'accounts','user'),(2,'accounts','userclass'),(14,'admin','logentry'),(16,'auth','group'),(15,'auth','permission'),(17,'contenttypes','contenttype'),(20,'ranges','fakerange'),(7,'ranges','mcqoptions'),(9,'ranges','questions'),(11,'ranges','questiontopic'),(10,'ranges','range'),(13,'ranges','rangequestions'),(8,'ranges','rangestudents'),(6,'ranges','studentquestions'),(12,'ranges','unavailableports'),(18,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'ranges','0001_initial','2018-07-05 14:45:02.594428'),(2,'accounts','0001_initial','2018-07-05 14:45:03.050258'),(3,'ranges','0002_auto_20180705_2244','2018-07-05 14:45:08.151200'),(4,'contenttypes','0001_initial','2018-07-05 14:45:08.281130'),(5,'contenttypes','0002_remove_content_type_name','2018-07-05 14:45:08.530976'),(6,'auth','0001_initial','2018-07-05 14:45:09.383131'),(7,'auth','0002_alter_permission_name_max_length','2018-07-05 14:45:09.411344'),(8,'auth','0003_alter_user_email_max_length','2018-07-05 14:45:09.425036'),(9,'auth','0004_alter_user_username_opts','2018-07-05 14:45:09.433132'),(10,'auth','0005_alter_user_last_login_null','2018-07-05 14:45:09.442356'),(11,'auth','0006_require_contenttypes_0002','2018-07-05 14:45:09.447065'),(12,'auth','0007_alter_validators_add_error_messages','2018-07-05 14:45:09.462764'),(13,'auth','0008_alter_user_username_max_length','2018-07-05 14:45:09.470970'),(14,'auth','0009_alter_user_last_name_max_length','2018-07-05 14:45:09.479321'),(15,'accounts','0002_auto_20180705_2244','2018-07-05 14:45:13.987903'),(16,'admin','0001_initial','2018-07-05 14:45:14.412967'),(17,'admin','0002_logentry_remove_auto_add','2018-07-05 14:45:14.433704'),(18,'sessions','0001_initial','2018-07-05 14:45:14.555054'),(19,'accounts','0003_fakestudentgroup','2018-07-05 15:22:34.206076'),(20,'ranges','0003_auto_20180705_2322','2018-07-05 15:22:34.386395'),(21,'accounts','0004_user_archived','2018-07-05 15:31:47.121887'),(22,'accounts','0005_auto_20180705_2332','2018-07-05 15:32:22.468573'),(23,'accounts','0006_auto_20180706_1147','2018-07-06 03:47:37.060231'),(24,'accounts','0007_user_isaccepted','2018-07-06 04:25:45.944440'),(25,'ranges','0004_rangequestions_isdisabled','2018-07-08 08:27:46.725975'),(26,'ranges','0005_auto_20180709_1154','2018-07-09 03:54:48.351614'),(27,'ranges','0006_auto_20180709_1209','2018-07-09 04:09:23.598867'),(28,'ranges','0007_auto_20180710_1410','2018-07-10 06:10:45.008643'),(29,'ranges','0008_auto_20180710_1517','2018-07-10 07:17:45.953089'),(30,'ranges','0009_rangequestions_registryid','2018-07-10 07:36:09.578222'),(31,'ranges','0010_auto_20180710_1809','2018-07-10 10:09:34.677136'),(32,'ranges','0011_fakerange','2018-07-11 05:48:00.292468'),(33,'ranges','0012_auto_20180711_1524','2018-07-11 07:24:15.692338'),(34,'ranges','0013_auto_20180711_1637','2018-07-11 08:38:01.214427'),(35,'ranges','0014_auto_20180711_1644','2018-07-11 08:44:37.161629'),(36,'ranges','0015_auto_20180712_1442','2018-07-12 06:42:32.260040');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('aug5h2klzoqq5o826huteuzsdp2mawjo','N2RmMDFkZmM3YjI1MGMwMjRlNzY4NmI3N2MzNDQ3ZjQ3NmM1NzE5NDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImFjY291bnRzLmZvcm1zLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiJrYXJsa3dhbkBnbWFpbC5jb20iLCJfYXV0aF91c2VyX2hhc2giOiI1NWYwMDE1ZTJhM2E2MjA3ODFiNjlkMjczMWUyYzEyZTVmOTAxMzI3In0=','2018-07-22 09:16:33.353898'),('bfyt98q3755lffwaa27mm8v3g0n2a58o','Y2I4MmQzOGY1YjZhMTI2NzQxMDc5NTQ0YTM5OTk3OGZiMmU4YzE5ZDp7Il9hdXRoX3VzZXJfaGFzaCI6IjU1ZjAwMTVlMmEzYTYyMDc4MWI2OWQyNzMxZTJjMTJlNWY5MDEzMjciLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJhY2NvdW50cy5mb3Jtcy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoia2FybGt3YW5AZ21haWwuY29tIn0=','2018-07-20 09:12:42.878602'),('h0rfg21o99cxa6sio64qw1nltcg2i7b0','NDZjY2UzNmY2NmNmMWI3MzUyYTkyMzIyZmIwMTVmZTEyZjE5M2QwYjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImFjY291bnRzLmZvcm1zLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjYwYzA1YTZiY2ViOTUwYzBjN2FkNGRlYWI4MjJlMGY1NzcwNjk3YjYiLCJfYXV0aF91c2VyX2lkIjoiam9zaHVhbGVlQGdtYWlsLmNvbSJ9','2018-07-20 08:16:58.751493');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-07-12 15:22:26
