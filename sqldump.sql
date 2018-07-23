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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Group`
--

LOCK TABLES `Group` WRITE;
/*!40000 ALTER TABLE `Group` DISABLE KEYS */;
INSERT INTO `Group` VALUES (1,'FYP','2018-07-23','15:24:29.520283',0,NULL,NULL,'karlkwan@gmail.com','joshualee@gmail.com',NULL);
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
  KEY `GroupRange_rangeID_834b66ea_fk` (`rangeID`),
  CONSTRAINT `GroupRange_addedBy_3485f07a_fk_User_email` FOREIGN KEY (`addedBy`) REFERENCES `User` (`email`),
  CONSTRAINT `GroupRange_groupID_1897bfba_fk_Group_groupID` FOREIGN KEY (`groupID`) REFERENCES `Group` (`groupID`),
  CONSTRAINT `GroupRange_rangeID_834b66ea_fk` FOREIGN KEY (`rangeID`) REFERENCES `Range` (`rangeID`)
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
  UNIQUE KEY `questionid` (`questionid`),
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `QuestionTopic`
--

LOCK TABLES `QuestionTopic` WRITE;
/*!40000 ALTER TABLE `QuestionTopic` DISABLE KEYS */;
INSERT INTO `QuestionTopic` VALUES (1,'firsttopic'),(2,'secondtopic'),(3,'thirdtopic'),(4,'fourthtopic');
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
  `hintpenalty` int(10) unsigned NOT NULL,
  `dateCreated` datetime(6) DEFAULT NULL,
  `points` int(10) unsigned NOT NULL,
  `answer` longtext,
  `usedocker` tinyint(1) NOT NULL,
  `registryID` varchar(255) DEFAULT NULL,
  `isArchived` tinyint(1) NOT NULL,
  `createdby` varchar(254) DEFAULT NULL,
  `rangeid` int(11) DEFAULT NULL,
  `topicid` int(11) DEFAULT NULL,
  PRIMARY KEY (`questionID`),
  KEY `Questions_createdby_43a92c1c_fk_User_email` (`createdby`),
  KEY `Questions_rangeid_f2763797_fk_Range_rangeID` (`rangeid`),
  KEY `Questions_topicid_f463268f_fk_QuestionTopic_topicid` (`topicid`),
  CONSTRAINT `Questions_createdby_43a92c1c_fk_User_email` FOREIGN KEY (`createdby`) REFERENCES `User` (`email`),
  CONSTRAINT `Questions_rangeid_f2763797_fk_Range_rangeID` FOREIGN KEY (`rangeid`) REFERENCES `Range` (`rangeID`),
  CONSTRAINT `Questions_topicid_f463268f_fk_QuestionTopic_topicid` FOREIGN KEY (`topicid`) REFERENCES `QuestionTopic` (`topicid`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Questions`
--

LOCK TABLES `Questions` WRITE;
/*!40000 ALTER TABLE `Questions` DISABLE KEYS */;
INSERT INTO `Questions` VALUES (1,'FL','first question','<p>first question</p>','no',0,'2018-07-22 16:00:00.000000',10,'no',0,NULL,0,'karlkwan@gmail.com',1,1),(2,'SA','second','<p>second</p>','second',3,'2018-07-22 16:00:00.000000',10,'answer',0,NULL,0,'karlkwan@gmail.com',1,2),(9,'FL','test','<p>test</p>','test',10,'2018-07-22 16:00:00.000000',20,'test',1,'test',0,'karlkwan@gmail.com',3,1);
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
  `attempts` int(10) unsigned NOT NULL,
  `createdby` varchar(254) NOT NULL,
  `dateCreated` date DEFAULT NULL,
  `dateEnd` date DEFAULT NULL,
  `dateStart` date DEFAULT NULL,
  `isDisabled` tinyint(1) NOT NULL,
  `isOpen` tinyint(1) NOT NULL,
  `lastModifiedBy` varchar(254) DEFAULT NULL,
  `lastModifiedDate` date DEFAULT NULL,
  `manualactive` tinyint(1) NOT NULL,
  `manualdeactive` tinyint(1) NOT NULL,
  `maxScore` int(10) unsigned,
  `rangeActive` tinyint(1) NOT NULL,
  `rangeCode` int(11) DEFAULT NULL,
  `rangeInfo` longtext NOT NULL,
  `rangeURL` varchar(50) DEFAULT NULL,
  `studentsInRange` int(10) unsigned,
  `timeEnd` time(6) DEFAULT NULL,
  `timeStart` time(6) DEFAULT NULL,
  PRIMARY KEY (`rangeID`),
  UNIQUE KEY `rangeCode` (`rangeCode`),
  UNIQUE KEY `rangeURL` (`rangeURL`),
  KEY `Range_createdby_4d2f29e0_fk_User_email` (`createdby`),
  KEY `Range_lastModifiedBy_35f0a21b_fk_User_email` (`lastModifiedBy`),
  CONSTRAINT `Range_createdby_4d2f29e0_fk_User_email` FOREIGN KEY (`createdby`) REFERENCES `User` (`email`),
  CONSTRAINT `Range_lastModifiedBy_35f0a21b_fk_User_email` FOREIGN KEY (`lastModifiedBy`) REFERENCES `User` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Range`
--

LOCK TABLES `Range` WRITE;
/*!40000 ALTER TABLE `Range` DISABLE KEYS */;
INSERT INTO `Range` VALUES (1,'range',0,'karlkwan@gmail.com','2018-07-23',NULL,NULL,0,0,NULL,NULL,0,0,20,0,354200,'<p>cyberrange</p>','range',0,NULL,NULL),(3,'time',0,'karlkwan@gmail.com','2018-07-23','2018-07-31','2018-07-23',0,0,NULL,NULL,0,0,10,0,435045,'<p>time</p>','time',0,'11:59:00.000000','08:30:00.000000');
/*!40000 ALTER TABLE `Range` ENABLE KEYS */;
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
  `groupid` int(11) DEFAULT NULL,
  `rangeID` int(11) NOT NULL,
  `email` varchar(254) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `RangeStudents_groupid_f7d179b4_fk_Group_groupID` (`groupid`),
  KEY `RangeStudents_rangeID_bc51c70c_fk_Range_rangeID` (`rangeID`),
  KEY `RangeStudents_email_af1dd9e3_fk_User_email` (`email`),
  CONSTRAINT `RangeStudents_email_af1dd9e3_fk_User_email` FOREIGN KEY (`email`) REFERENCES `User` (`email`),
  CONSTRAINT `RangeStudents_groupid_f7d179b4_fk_Group_groupID` FOREIGN KEY (`groupid`) REFERENCES `Group` (`groupID`),
  CONSTRAINT `RangeStudents_rangeID_bc51c70c_fk_Range_rangeID` FOREIGN KEY (`rangeID`) REFERENCES `Range` (`rangeID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RangeStudents`
--

LOCK TABLES `RangeStudents` WRITE;
/*!40000 ALTER TABLE `RangeStudents` DISABLE KEYS */;
INSERT INTO `RangeStudents` VALUES (1,'2018-07-22 16:00:00.000000',NULL,0,NULL,NULL,NULL,1,1,'dextergui@gmail.com'),(2,'2018-07-22 16:00:00.000000',NULL,0,NULL,NULL,NULL,1,1,'joshualee@gmail.com'),(3,'2018-07-22 16:00:00.000000',NULL,0,NULL,NULL,NULL,1,1,'marcuskho@gmail.com'),(4,'2018-07-22 16:00:00.000000',NULL,0,NULL,NULL,NULL,1,1,'jonathanau@gmail.com'),(5,'2018-07-22 16:00:00.000000',NULL,0,NULL,NULL,NULL,1,1,'wesleychiau@gmail.com');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentGroup`
--

LOCK TABLES `StudentGroup` WRITE;
/*!40000 ALTER TABLE `StudentGroup` DISABLE KEYS */;
INSERT INTO `StudentGroup` VALUES (1,1,'dextergui@gmail.com'),(2,1,'joshualee@gmail.com'),(3,1,'marcuskho@gmail.com'),(4,1,'jonathanau@gmail.com'),(5,1,'wesleychiau@gmail.com');
/*!40000 ALTER TABLE `StudentGroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudentHints`
--

DROP TABLE IF EXISTS `StudentHints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `StudentHints` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hintactivated` tinyint(1) NOT NULL,
  `questionid` int(11) NOT NULL,
  `rangeid` int(11) NOT NULL,
  `studentid` varchar(254) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `StudentHints_questionid_0154d770_fk_Questions_questionID` (`questionid`),
  KEY `StudentHints_rangeid_f8ed50c9_fk_Range_rangeID` (`rangeid`),
  KEY `StudentHints_studentid_231b4111_fk_User_email` (`studentid`),
  CONSTRAINT `StudentHints_questionid_0154d770_fk_Questions_questionID` FOREIGN KEY (`questionid`) REFERENCES `Questions` (`questionID`),
  CONSTRAINT `StudentHints_rangeid_f8ed50c9_fk_Range_rangeID` FOREIGN KEY (`rangeid`) REFERENCES `Range` (`rangeID`),
  CONSTRAINT `StudentHints_studentid_231b4111_fk_User_email` FOREIGN KEY (`studentid`) REFERENCES `User` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentHints`
--

LOCK TABLES `StudentHints` WRITE;
/*!40000 ALTER TABLE `StudentHints` DISABLE KEYS */;
/*!40000 ALTER TABLE `StudentHints` ENABLE KEYS */;
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
  `marksawarded` int(10) unsigned NOT NULL,
  `attempts` int(10) unsigned NOT NULL,
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentQuestions`
--

LOCK TABLES `StudentQuestions` WRITE;
/*!40000 ALTER TABLE `StudentQuestions` DISABLE KEYS */;
/*!40000 ALTER TABLE `StudentQuestions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UnavailablePorts`
--

DROP TABLE IF EXISTS `UnavailablePorts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UnavailablePorts` (
  `portNumber` int(10) unsigned NOT NULL,
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
  `isaccepted` tinyint(1) NOT NULL,
  `isdisabled` tinyint(1) NOT NULL,
  `lastModifiedBy` varchar(254) DEFAULT NULL,
  `lastModifiedTime` time(6) DEFAULT NULL,
  `userclass` varchar(45),
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
INSERT INTO `User` VALUES ('calvinsiak@gmail.com','calvinsiak','pbkdf2_sha256$100000$QdfntYTHo2Xm$iQIYwTFaADvfcyOzgMk6CCGdc9NPFrPmNZUUoYLKbX8=','',NULL,NULL,'2018-07-23 04:32:51.675793',1,NULL,1,0,0,NULL,NULL,'Public'),('dextergui@gmail.com','dextergui','pbkdf2_sha256$100000$JUHU1bWaqnUW$dEwl1mtZn0v8xQ62WV1Yun28mk5jw2Bkpx8z52tq6Co=','Dexter Gui','2018-07-23','2018-07-23',NULL,0,'karlkwan@gmail.com',0,1,0,'karlkwan@gmail.com','15:24:09.777316','DISM/FT/3A/01'),('hubertus@gmail.com','hubertus','pbkdf2_sha256$100000$mLDciQZdgCtR$LvKkPvbTfqfk8/GUhzj07YD/n9be6NRsUufrkZWZQXY=','',NULL,NULL,'2018-07-23 04:30:34.876096',1,NULL,1,1,0,NULL,NULL,'Public'),('jonathanau@gmail.com','jonau','pbkdf2_sha256$100000$PVouwe2olTqr$n4LttrhUurU25VUMNo5R2VmcVgV2t87HDDcIU/Hyczg=','Jonathan Au','2018-07-23','2018-07-23',NULL,0,'karlkwan@gmail.com',0,1,0,'karlkwan@gmail.com','12:18:57.814236','DISM/FT/3A/01'),('joshualee@gmail.com','joshualee','pbkdf2_sha256$100000$OJRwGc44i0T8$Ex9Z0Rg1a6+AoARj3qVhxDoVxU5IE8i0vZ8AvRZTj0w=','Joshua Lee','2018-07-23','2018-07-23',NULL,0,'karlkwan@gmail.com',0,1,0,'karlkwan@gmail.com','12:18:18.909414','DISM/FT/3A/01'),('karlkwan@gmail.com','karlkwan','pbkdf2_sha256$100000$edkEGYQfOWwt$noGaSiFHCNuFBARYu1qqTutYyTS/tK6237X0+dNIPF0=','',NULL,NULL,'2018-07-23 10:49:59.264396',1,NULL,1,1,0,NULL,NULL,'Public'),('marcuskho@gmail.com','marcuskho','pbkdf2_sha256$100000$dCIROHYNi0gl$ZSRcH5eOjs6f6HDUTEwhwIH461KeHPc1ZNbifLoDphw=','Marcus Kho','2018-07-23','2018-07-23',NULL,0,'karlkwan@gmail.com',0,1,0,'karlkwan@gmail.com','12:19:14.024170','DISM/FT/3A/01'),('wesleychiau@gmail.com','wesleychiau','pbkdf2_sha256$100000$kUEGUNUZLU7K$EFip/ELdlUuoyxnvj0DgS9AcU3nOPLDlmtKSGQ26qiE=','Wesley Chiau','2018-07-23','2018-07-23',NULL,0,'karlkwan@gmail.com',0,1,0,'karlkwan@gmail.com','12:18:38.422900','DISM/FT/3A/01');
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
INSERT INTO `UserClass` VALUES (1,'DISM/FT/3A/01');
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
INSERT INTO `auth_permission` VALUES (1,'Can add group',1,'add_group'),(2,'Can change group',1,'change_group'),(3,'Can delete group',1,'delete_group'),(4,'Can add student group',2,'add_studentgroup'),(5,'Can change student group',2,'change_studentgroup'),(6,'Can delete student group',2,'delete_studentgroup'),(7,'Can add group range',3,'add_grouprange'),(8,'Can change group range',3,'change_grouprange'),(9,'Can delete group range',3,'delete_grouprange'),(10,'Can add fake student group',4,'add_fakestudentgroup'),(11,'Can change fake student group',4,'change_fakestudentgroup'),(12,'Can delete fake student group',4,'delete_fakestudentgroup'),(13,'Can add user class',5,'add_userclass'),(14,'Can change user class',5,'change_userclass'),(15,'Can delete user class',5,'delete_userclass'),(16,'Can add user',6,'add_user'),(17,'Can change user',6,'change_user'),(18,'Can delete user',6,'delete_user'),(19,'Can add unavailable ports',7,'add_unavailableports'),(20,'Can change unavailable ports',7,'change_unavailableports'),(21,'Can delete unavailable ports',7,'delete_unavailableports'),(22,'Can add student hints',8,'add_studenthints'),(23,'Can change student hints',8,'change_studenthints'),(24,'Can delete student hints',8,'delete_studenthints'),(25,'Can add fake range',9,'add_fakerange'),(26,'Can change fake range',9,'change_fakerange'),(27,'Can delete fake range',9,'delete_fakerange'),(28,'Can add student questions',10,'add_studentquestions'),(29,'Can change student questions',10,'change_studentquestions'),(30,'Can delete student questions',10,'delete_studentquestions'),(31,'Can add range students',11,'add_rangestudents'),(32,'Can change range students',11,'change_rangestudents'),(33,'Can delete range students',11,'delete_rangestudents'),(34,'Can add mcq options',12,'add_mcqoptions'),(35,'Can change mcq options',12,'change_mcqoptions'),(36,'Can delete mcq options',12,'delete_mcqoptions'),(37,'Can add question topic',13,'add_questiontopic'),(38,'Can change question topic',13,'change_questiontopic'),(39,'Can delete question topic',13,'delete_questiontopic'),(40,'Can add range',14,'add_range'),(41,'Can change range',14,'change_range'),(42,'Can delete range',14,'delete_range'),(43,'Can add questions',15,'add_questions'),(44,'Can change questions',15,'change_questions'),(45,'Can delete questions',15,'delete_questions'),(46,'Can add log entry',16,'add_logentry'),(47,'Can change log entry',16,'change_logentry'),(48,'Can delete log entry',16,'delete_logentry'),(49,'Can add group',17,'add_group'),(50,'Can change group',17,'change_group'),(51,'Can delete group',17,'delete_group'),(52,'Can add permission',18,'add_permission'),(53,'Can change permission',18,'change_permission'),(54,'Can delete permission',18,'delete_permission'),(55,'Can add content type',19,'add_contenttype'),(56,'Can change content type',19,'change_contenttype'),(57,'Can delete content type',19,'delete_contenttype'),(58,'Can add session',20,'add_session'),(59,'Can change session',20,'change_session'),(60,'Can delete session',20,'delete_session');
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
INSERT INTO `django_content_type` VALUES (4,'accounts','fakestudentgroup'),(1,'accounts','group'),(3,'accounts','grouprange'),(2,'accounts','studentgroup'),(6,'accounts','user'),(5,'accounts','userclass'),(16,'admin','logentry'),(17,'auth','group'),(18,'auth','permission'),(19,'contenttypes','contenttype'),(9,'ranges','fakerange'),(12,'ranges','mcqoptions'),(15,'ranges','questions'),(13,'ranges','questiontopic'),(14,'ranges','range'),(11,'ranges','rangestudents'),(8,'ranges','studenthints'),(10,'ranges','studentquestions'),(7,'ranges','unavailableports'),(20,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'ranges','0001_initial','2018-07-23 04:11:06.562327'),(2,'contenttypes','0001_initial','2018-07-23 04:11:06.697934'),(3,'contenttypes','0002_remove_content_type_name','2018-07-23 04:11:06.985465'),(4,'auth','0001_initial','2018-07-23 04:11:07.932364'),(5,'auth','0002_alter_permission_name_max_length','2018-07-23 04:11:07.966024'),(6,'auth','0003_alter_user_email_max_length','2018-07-23 04:11:07.984695'),(7,'auth','0004_alter_user_username_opts','2018-07-23 04:11:07.998457'),(8,'auth','0005_alter_user_last_login_null','2018-07-23 04:11:08.017038'),(9,'auth','0006_require_contenttypes_0002','2018-07-23 04:11:08.020464'),(10,'auth','0007_alter_validators_add_error_messages','2018-07-23 04:11:08.037140'),(11,'auth','0008_alter_user_username_max_length','2018-07-23 04:11:08.051274'),(12,'auth','0009_alter_user_last_name_max_length','2018-07-23 04:11:08.062010'),(13,'accounts','0001_initial','2018-07-23 04:11:08.541559'),(14,'accounts','0002_auto_20180723_1017','2018-07-23 04:11:13.479316'),(15,'admin','0001_initial','2018-07-23 04:11:13.931732'),(16,'admin','0002_logentry_remove_auto_add','2018-07-23 04:11:13.954541'),(17,'ranges','0002_auto_20180723_1017','2018-07-23 04:11:21.554272'),(18,'sessions','0001_initial','2018-07-23 04:11:21.696736');
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
INSERT INTO `django_session` VALUES ('wh09mldq4153vbhiknyx3utq616usbqw','YTA3MzI3OTZkNzY3NDE5YWZkZjgzNmE1MzAxYjA4ZDQyMWNiYzBhZTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImFjY291bnRzLmZvcm1zLkVtYWlsQmFja2VuZCIsIlRGIjpmYWxzZSwicXVlc3Rpb25pZCI6OSwicXVlc3Rpb25zY2FydCI6W10sIl9hdXRoX3VzZXJfaWQiOiJrYXJsa3dhbkBnbWFpbC5jb20iLCJfYXV0aF91c2VyX2hhc2giOiJhMGY1ODMyMjhkNjdhNzBiM2MwZTNiYjMxNDJlZGM5NGUzZDRhYjM1In0=','2018-08-06 10:49:59.313749');
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

-- Dump completed on 2018-07-23 18:58:34
