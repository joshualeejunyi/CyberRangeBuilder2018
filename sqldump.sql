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
  `createdBy` varchar(254) DEFAULT NULL,
  `dateCreated` date DEFAULT NULL,
  `groupLeader` varchar(254) DEFAULT NULL,
  `groupPoints` int(11),
  `lastModifiedBy` varchar(254) DEFAULT NULL,
  `lastModifiedDate` date DEFAULT NULL,
  `lastModifiedTime` time(6) DEFAULT NULL,
  `timeCreated` time(6) DEFAULT NULL,
  PRIMARY KEY (`groupID`),
  UNIQUE KEY `groupname` (`groupName`),
  KEY `Group_createdBy_e8a86322_fk_User_email` (`createdBy`),
  KEY `Group_groupLeader_dda63499_fk_User_email` (`groupLeader`),
  KEY `Group_lastModifiedBy_2b8379dc_fk_User_email` (`lastModifiedBy`),
  CONSTRAINT `Group_createdBy_e8a86322_fk_User_email` FOREIGN KEY (`createdBy`) REFERENCES `User` (`email`),
  CONSTRAINT `Group_groupLeader_dda63499_fk_User_email` FOREIGN KEY (`groupLeader`) REFERENCES `User` (`email`),
  CONSTRAINT `Group_lastModifiedBy_2b8379dc_fk_User_email` FOREIGN KEY (`lastModifiedBy`) REFERENCES `User` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Group`
--

LOCK TABLES `Group` WRITE;
/*!40000 ALTER TABLE `Group` DISABLE KEYS */;
INSERT INTO `Group` VALUES (1,'bestgroup','teacher@email.com','2018-06-28','useraccount@account.com',0,'teacher@email.com','2018-06-28','17:14:20.013263','17:14:20.013263'),(4,'spacecadets','teacher@email.com','2018-06-30',NULL,0,NULL,NULL,NULL,'22:31:28.864714');
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
  `groupID` int(11) NOT NULL,
  `rangeID` int(11) NOT NULL,
  `addedBy` varchar(254) DEFAULT NULL,
  `dateCreated` date DEFAULT NULL,
  `groupRangePoints` int(11),
  `timeCreated` time(6) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `GroupRange_groupID_1897bfba_fk_Group_groupID` (`groupID`),
  KEY `GroupRange_rangeID_834b66ea_fk_Range_rangeID` (`rangeID`),
  KEY `GroupRange_addedBy_3485f07a_fk_User_email` (`addedBy`),
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
  KEY `MCQOptions_questionid_3371087c_fk_Questions_questionID` (`questionid`),
  CONSTRAINT `MCQOptions_questionid_3371087c_fk_Questions_questionID` FOREIGN KEY (`questionid`) REFERENCES `Questions` (`questionID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MCQOptions`
--

LOCK TABLES `MCQOptions` WRITE;
/*!40000 ALTER TABLE `MCQOptions` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `QuestionTopic`
--

LOCK TABLES `QuestionTopic` WRITE;
/*!40000 ALTER TABLE `QuestionTopic` DISABLE KEYS */;
INSERT INTO `QuestionTopic` VALUES (1,'Port Scanning'),(2,'Cryptography'),(3,'Man In The Middle');
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
  `questiontitle` varchar(100) DEFAULT NULL,
  `questiontext` varchar(100) NOT NULL,
  `hint` varchar(100) NOT NULL,
  `marks` int(11) NOT NULL,
  `topicid` int(11) DEFAULT NULL,
  PRIMARY KEY (`questionID`),
  KEY `Questions_topicid_f463268f_fk_QuestionTopic_topicid` (`topicid`),
  CONSTRAINT `Questions_topicid_f463268f_fk_QuestionTopic_topicid` FOREIGN KEY (`topicid`) REFERENCES `QuestionTopic` (`topicid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Questions`
--

LOCK TABLES `Questions` WRITE;
/*!40000 ALTER TABLE `Questions` DISABLE KEYS */;
INSERT INTO `Questions` VALUES (1,'FL','this is a question','please answer','hi',10,1),(2,'FL','test','test','test',10,2);
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
  `dateTimeCreated` datetime(6) DEFAULT NULL,
  `dateTimeEnd` datetime(6) DEFAULT NULL,
  `dateTimeStart` datetime(6) DEFAULT NULL,
  `lastModifiedDate` date DEFAULT NULL,
  `maxScore` int(11) DEFAULT NULL,
  `rangeActive` tinyint(1) NOT NULL,
  `rangeCode` int(11) DEFAULT NULL,
  `rangeURL` varchar(50) DEFAULT NULL,
  `studentsInRange` int(11) DEFAULT NULL,
  `createdby` varchar(254) NOT NULL,
  PRIMARY KEY (`rangeID`),
  UNIQUE KEY `rangeCode` (`rangeCode`),
  KEY `Range_createdby_4d2f29e0_fk_User_email` (`createdby`),
  CONSTRAINT `Range_createdby_4d2f29e0_fk_User_email` FOREIGN KEY (`createdby`) REFERENCES `User` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Range`
--

LOCK TABLES `Range` WRITE;
/*!40000 ALTER TABLE `Range` DISABLE KEYS */;
INSERT INTO `Range` VALUES (1,'range',NULL,NULL,NULL,NULL,100,1,1924,'range',1,'teacher@email.com'),(2,'CTF #1',NULL,NULL,NULL,NULL,100,1,918234,'CTF1',1,'teacher@email.com'),(3,'completedrange',NULL,NULL,NULL,NULL,100,0,NULL,'completedrange',NULL,'teacher@email.com');
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
  `answer` varchar(100) DEFAULT NULL,
  `questionID` int(11) NOT NULL,
  `rangeID` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `RangeQuestions_questionID_b51c40c3_fk_Questions_questionID` (`questionID`),
  KEY `RangeQuestions_rangeID_4ec72b4b_fk_Range_rangeID` (`rangeID`),
  CONSTRAINT `RangeQuestions_questionID_b51c40c3_fk_Questions_questionID` FOREIGN KEY (`questionID`) REFERENCES `Questions` (`questionID`),
  CONSTRAINT `RangeQuestions_rangeID_4ec72b4b_fk_Range_rangeID` FOREIGN KEY (`rangeID`) REFERENCES `Range` (`rangeID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RangeQuestions`
--

LOCK TABLES `RangeQuestions` WRITE;
/*!40000 ALTER TABLE `RangeQuestions` DISABLE KEYS */;
INSERT INTO `RangeQuestions` VALUES (1,'hello',1,1),(2,'test',2,1);
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
  `progress` varchar(45) DEFAULT NULL,
  `teamID` varchar(45) DEFAULT NULL,
  `teamName` varchar(45) DEFAULT NULL,
  `points` int(11) NOT NULL,
  `rangeID` int(11) NOT NULL,
  `email` varchar(254) NOT NULL,
  `dateCompleted` date DEFAULT NULL,
  `timeCompleted` time(6) DEFAULT NULL,
  `lastaccess` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `RangeStudents_rangeID_bc51c70c_fk_Range_rangeID` (`rangeID`),
  KEY `RangeStudents_email_af1dd9e3_fk_User_email` (`email`),
  CONSTRAINT `RangeStudents_email_af1dd9e3_fk_User_email` FOREIGN KEY (`email`) REFERENCES `User` (`email`),
  CONSTRAINT `RangeStudents_rangeID_bc51c70c_fk_Range_rangeID` FOREIGN KEY (`rangeID`) REFERENCES `Range` (`rangeID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RangeStudents`
--

LOCK TABLES `RangeStudents` WRITE;
/*!40000 ALTER TABLE `RangeStudents` DISABLE KEYS */;
INSERT INTO `RangeStudents` VALUES (1,NULL,NULL,NULL,NULL,10,1,'joshua@gmail.com',NULL,NULL,NULL),(2,NULL,NULL,NULL,NULL,0,2,'joshua@gmail.com',NULL,NULL,NULL),(3,NULL,NULL,NULL,NULL,95,3,'joshua@gmail.com','2018-07-01',NULL,NULL),(4,NULL,NULL,NULL,NULL,60,3,'useraccount@account.com','2018-07-01',NULL,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentGroup`
--

LOCK TABLES `StudentGroup` WRITE;
/*!40000 ALTER TABLE `StudentGroup` DISABLE KEYS */;
INSERT INTO `StudentGroup` VALUES (1,1,'joshua@gmail.com'),(6,4,'joshua@gmail.com'),(7,1,'test@test.com'),(8,1,'useraccount@account.com');
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentQuestions`
--

LOCK TABLES `StudentQuestions` WRITE;
/*!40000 ALTER TABLE `StudentQuestions` DISABLE KEYS */;
INSERT INTO `StudentQuestions` VALUES (2,'hello',1,10,1,1,'joshua@gmail.com');
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
INSERT INTO `UnavailablePorts` VALUES (8052,'joshua@gmail.com');
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
  `lastModifiedBy` varchar(254) DEFAULT NULL,
  `admin` tinyint(1) NOT NULL,
  `userclass` varchar(45) DEFAULT NULL,
  `lastModifiedTime` time(6) DEFAULT NULL,
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
INSERT INTO `User` VALUES ('admin@admin.com','admin','pbkdf2_sha256$100000$xeZtvFVWjx8h$/syBeE1Kyhv/rOSDKkMxP30RLCksrYi/uoNY6l7iQ1Q=','',NULL,NULL,NULL,1,NULL,NULL,1,'Public',NULL),('joshua@gmail.com','joshualee','pbkdf2_sha256$100000$f9m76xdKzonO$cNhOjyU8BW6C4tNDFvngLQjbcDO8hlUc54v3lLFdr+E=','Joshua Lee','2018-06-27','2018-06-27','2018-07-01 13:47:54.867339',0,'teacher@email.com','teacher@email.com',0,'DISM/FT/2B/22','17:14:20.013263'),('teacher@email.com','teacher','pbkdf2_sha256$100000$R5cofRozx4JS$qnC9InHt16YMEUgm6e0c9oVx+HYJe3uHHwk5RuMF/Ys=','teacher','2018-06-27',NULL,'2018-07-01 14:26:47.421330',1,NULL,NULL,0,'',NULL),('test@test.com','test','pbkdf2_sha256$100000$yqzyywlNmwg2$CbiBPXFIbmDUrJHMhgA/bJR3GYCrW1DbY+s2DYI+ZuQ=','test','2018-07-01','2018-07-01','2018-06-30 16:52:28.134881',0,'teacher@email.com','teacher@email.com',0,'DISM/FT/1B/21','18:22:58.792222'),('useraccount@account.com','useraccount','pbkdf2_sha256$100000$yqzyywlNmwg2$CbiBPXFIbmDUrJHMhgA/bJR3GYCrW1DbY+s2DYI+ZuQ=','useraccount','2018-06-29','2018-07-01','2018-06-30 16:52:28.134881',0,'teacher@email.com','teacher@email.com',0,'DISM/FT/1B/21','18:22:58.792222');
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
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UserClass`
--

LOCK TABLES `UserClass` WRITE;
/*!40000 ALTER TABLE `UserClass` DISABLE KEYS */;
INSERT INTO `UserClass` VALUES (1,'DISM/FT/1A/01'),(2,'DISM/FT/1A/02'),(3,'DISM/FT/1A/03'),(4,'DISM/FT/1B/21'),(5,'DISM/FT/1B/22'),(6,'DISM/FT/2A/01'),(7,'DISM/FT/2A/02'),(8,'DISM/FT/2A/03'),(9,'DISM/FT/2B/21'),(10,'DISM/FT/2B/22'),(11,'DISM/FT/3A/01'),(12,'DISM/FT/3A/02'),(13,'DISM/FT/3A/03'),(14,'DISM/FT/3B/21'),(15,'DISM/FT/3A/22'),(16,'Public');
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
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add user',1,'add_user'),(2,'Can change user',1,'change_user'),(3,'Can delete user',1,'delete_user'),(4,'Can add user class',2,'add_userclass'),(5,'Can change user class',2,'change_userclass'),(6,'Can delete user class',2,'delete_userclass'),(7,'Can add question topic',3,'add_questiontopic'),(8,'Can change question topic',3,'change_questiontopic'),(9,'Can delete question topic',3,'delete_questiontopic'),(10,'Can add range questions',4,'add_rangequestions'),(11,'Can change range questions',4,'change_rangequestions'),(12,'Can delete range questions',4,'delete_rangequestions'),(13,'Can add student questions',5,'add_studentquestions'),(14,'Can change student questions',5,'change_studentquestions'),(15,'Can delete student questions',5,'delete_studentquestions'),(16,'Can add questions',6,'add_questions'),(17,'Can change questions',6,'change_questions'),(18,'Can delete questions',6,'delete_questions'),(19,'Can add range',7,'add_range'),(20,'Can change range',7,'change_range'),(21,'Can delete range',7,'delete_range'),(22,'Can add range students',8,'add_rangestudents'),(23,'Can change range students',8,'change_rangestudents'),(24,'Can delete range students',8,'delete_rangestudents'),(25,'Can add mcq options',9,'add_mcqoptions'),(26,'Can change mcq options',9,'change_mcqoptions'),(27,'Can delete mcq options',9,'delete_mcqoptions'),(28,'Can add log entry',10,'add_logentry'),(29,'Can change log entry',10,'change_logentry'),(30,'Can delete log entry',10,'delete_logentry'),(31,'Can add group',11,'add_group'),(32,'Can change group',11,'change_group'),(33,'Can delete group',11,'delete_group'),(34,'Can add permission',12,'add_permission'),(35,'Can change permission',12,'change_permission'),(36,'Can delete permission',12,'delete_permission'),(37,'Can add content type',13,'add_contenttype'),(38,'Can change content type',13,'change_contenttype'),(39,'Can delete content type',13,'delete_contenttype'),(40,'Can add session',14,'add_session'),(41,'Can change session',14,'change_session'),(42,'Can delete session',14,'delete_session'),(43,'Can add group range',15,'add_grouprange'),(44,'Can change group range',15,'change_grouprange'),(45,'Can delete group range',15,'delete_grouprange'),(46,'Can add group',16,'add_group'),(47,'Can change group',16,'change_group'),(48,'Can delete group',16,'delete_group'),(49,'Can add student group',17,'add_studentgroup'),(50,'Can change student group',17,'change_studentgroup'),(51,'Can delete student group',17,'delete_studentgroup'),(52,'Can add unavailable ports',18,'add_unavailableports'),(53,'Can change unavailable ports',18,'change_unavailableports'),(54,'Can delete unavailable ports',18,'delete_unavailableports');
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
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (16,'accounts','group'),(15,'accounts','grouprange'),(17,'accounts','studentgroup'),(1,'accounts','user'),(2,'accounts','userclass'),(10,'admin','logentry'),(11,'auth','group'),(12,'auth','permission'),(13,'contenttypes','contenttype'),(9,'ranges','mcqoptions'),(6,'ranges','questions'),(3,'ranges','questiontopic'),(7,'ranges','range'),(4,'ranges','rangequestions'),(8,'ranges','rangestudents'),(5,'ranges','studentquestions'),(18,'ranges','unavailableports'),(14,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2018-06-26 06:41:26.272743'),(2,'contenttypes','0002_remove_content_type_name','2018-06-26 06:41:26.351242'),(3,'auth','0001_initial','2018-06-26 06:41:26.532061'),(4,'auth','0002_alter_permission_name_max_length','2018-06-26 06:41:26.550658'),(5,'auth','0003_alter_user_email_max_length','2018-06-26 06:41:26.564077'),(6,'auth','0004_alter_user_username_opts','2018-06-26 06:41:26.583176'),(7,'auth','0005_alter_user_last_login_null','2018-06-26 06:41:26.598737'),(8,'auth','0006_require_contenttypes_0002','2018-06-26 06:41:26.609914'),(9,'auth','0007_alter_validators_add_error_messages','2018-06-26 06:41:26.624355'),(10,'auth','0008_alter_user_username_max_length','2018-06-26 06:41:26.645624'),(11,'auth','0009_alter_user_last_name_max_length','2018-06-26 06:41:26.659039'),(12,'accounts','0001_initial','2018-06-26 06:41:26.777059'),(13,'accounts','0002_auto_20180626_0640','2018-06-26 06:41:27.140527'),(14,'admin','0001_initial','2018-06-26 06:41:27.239556'),(15,'admin','0002_logentry_remove_auto_add','2018-06-26 06:41:27.260260'),(16,'ranges','0001_initial','2018-06-26 06:41:27.289395'),(17,'ranges','0002_auto_20180626_0640','2018-06-26 06:41:28.255808'),(18,'sessions','0001_initial','2018-06-26 06:41:28.285238'),(19,'accounts','0003_auto_20180626_1400','2018-06-26 14:00:46.338401'),(20,'accounts','0004_auto_20180626_1516','2018-06-26 15:16:35.115431'),(21,'accounts','0005_auto_20180627_0301','2018-06-27 03:01:42.654916'),(22,'accounts','0006_auto_20180627_0547','2018-06-27 05:47:37.012610'),(23,'accounts','0007_user_lastmodifiedtime','2018-06-27 08:37:16.543775'),(24,'accounts','0008_group_grouprange_studentgroup','2018-06-27 16:29:44.189283'),(25,'accounts','0009_auto_20180628_0043','2018-06-27 16:43:35.465692'),(26,'ranges','0003_unavailableports','2018-06-28 09:42:44.132268'),(27,'ranges','0004_auto_20180629_1534','2018-06-29 07:34:10.717254'),(28,'ranges','0005_rangequestions_lastaccess','2018-06-29 07:42:39.689750'),(29,'ranges','0006_auto_20180629_1543','2018-06-29 07:43:52.118209'),(30,'ranges','0007_auto_20180629_2135','2018-06-29 13:35:34.608924'),(31,'ranges','0008_auto_20180701_2144','2018-07-01 13:44:50.930852');
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
INSERT INTO `django_session` VALUES ('0gw6zluf70mij9xpb68ev7bp4j67ions','MDgyNDBiMTNhOWUyN2I2MjljMjQ2OTgxODA3ZjE3YTRmOTBhZDhiMTp7fQ==','2018-07-10 14:01:12.483905'),('6bzslmd4z1kt54ew34r57yrw6nytyp8k','OWFjY2NmZGUzNzkxYmQyMDdmMTM0NDk1YzEwZGE1MTQ2MzJjMWE1Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzE2NWU3ZTk0MDI0YWRmZWI2YjFlZjYxZDlkZTNiM2I1ZTlkNTFhMiIsIl9hdXRoX3VzZXJfaWQiOiJ0ZWFjaGVyQGVtYWlsLmNvbSJ9','2018-07-15 14:26:47.430905'),('7jqh69d5xohti53rhfe7jmspxi2k1r9w','MDgyNDBiMTNhOWUyN2I2MjljMjQ2OTgxODA3ZjE3YTRmOTBhZDhiMTp7fQ==','2018-07-10 14:07:09.773926');
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

-- Dump completed on 2018-07-02  0:03:39
