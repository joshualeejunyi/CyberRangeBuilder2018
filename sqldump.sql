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
INSERT INTO `Group` VALUES (1,'testgroup','2018-07-30','15:23:35.923608',0,NULL,NULL,'karlkwan@gmail.com','dextergui@gmail.com',NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `QuestionTopic`
--

LOCK TABLES `QuestionTopic` WRITE;
/*!40000 ALTER TABLE `QuestionTopic` DISABLE KEYS */;
INSERT INTO `QuestionTopic` VALUES (1,'firsttopic'),(2,'secondtopic');
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Questions`
--

LOCK TABLES `Questions` WRITE;
/*!40000 ALTER TABLE `Questions` DISABLE KEYS */;
INSERT INTO `Questions` VALUES (1,'FL','firstquestion','<p>This is the first question.</p>','This is a hint',5,'2018-07-29 16:00:00.000000',10,'firstanswer',0,'',0,'karlkwan@gmail.com',1,1),(2,'SA','secondquestion','<p>This is the second question.</p>','This is the second hint',10,'2018-07-29 16:00:00.000000',20,'second answer',0,'',0,'karlkwan@gmail.com',1,2),(3,'FL','thirdquestion','<p>this is the thirdquestion</p>','this is the third hint',10,'2018-07-29 16:00:00.000000',30,'thirdanswer',0,'',0,'karlkwan@gmail.com',2,1),(8,'FL','firstquestion','<p>This is the first question.</p>','This is a hint',5,'2018-07-29 16:00:00.000000',10,'firstanswer',0,'',0,'karlkwan@gmail.com',2,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Range`
--

LOCK TABLES `Range` WRITE;
/*!40000 ALTER TABLE `Range` DISABLE KEYS */;
INSERT INTO `Range` VALUES (1,'Cyber Range #1',0,'karlkwan@gmail.com','2018-07-30',NULL,NULL,0,1,NULL,NULL,0,0,30,0,797066,'<p>Hello, this is cyber range #1.</p>','cyberrange1',0,NULL,NULL),(2,'Cyber Range #2',3,'karlkwan@gmail.com','2018-07-30',NULL,NULL,0,0,'karlkwan@gmail.com','2018-07-30',0,1,30,0,497481,'<p>This is the second cyber range.</p>','cyberrange2',0,NULL,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RangeStudents`
--

LOCK TABLES `RangeStudents` WRITE;
/*!40000 ALTER TABLE `RangeStudents` DISABLE KEYS */;
INSERT INTO `RangeStudents` VALUES (1,'2018-07-29 16:00:00.000000',NULL,0,NULL,NULL,NULL,1,1,'jonau@gmail.com'),(2,'2018-07-29 16:00:00.000000',NULL,0,NULL,NULL,NULL,1,1,'dextergui@gmail.com'),(3,'2018-07-29 16:00:00.000000',NULL,0,NULL,NULL,NULL,1,1,'joshualee@gmail.com'),(4,'2018-07-29 16:00:00.000000',NULL,0,NULL,NULL,NULL,1,1,'marcuskho@gmail.com'),(5,'2018-07-29 16:00:00.000000',NULL,0,NULL,NULL,NULL,1,1,'wesleychiau@gmail.com'),(11,'2018-07-29 16:00:00.000000',NULL,0,NULL,NULL,NULL,1,2,'jonau@gmail.com'),(12,'2018-07-29 16:00:00.000000',NULL,0,NULL,NULL,NULL,1,2,'dextergui@gmail.com'),(13,'2018-07-29 16:00:00.000000',NULL,0,NULL,NULL,NULL,1,2,'joshualee@gmail.com'),(14,'2018-07-29 16:00:00.000000',NULL,0,NULL,NULL,NULL,1,2,'marcuskho@gmail.com'),(15,'2018-07-29 16:00:00.000000',NULL,0,NULL,NULL,NULL,1,2,'wesleychiau@gmail.com');
/*!40000 ALTER TABLE `RangeStudents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SDLComment`
--

DROP TABLE IF EXISTS `SDLComment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SDLComment` (
  `commentID` int(11) NOT NULL AUTO_INCREMENT,
  `comment` varchar(255) DEFAULT NULL,
  `datePosted` date DEFAULT NULL,
  `timePosted` time(6) DEFAULT NULL,
  `commenter` varchar(254) DEFAULT NULL,
  `postid` int(11) DEFAULT NULL,
  PRIMARY KEY (`commentID`),
  KEY `SDLComment_commenter_4080eedc_fk_User_email` (`commenter`),
  KEY `SDLComment_postid_9b5517e8_fk_SDLPost_postID` (`postid`),
  CONSTRAINT `SDLComment_commenter_4080eedc_fk_User_email` FOREIGN KEY (`commenter`) REFERENCES `User` (`email`),
  CONSTRAINT `SDLComment_postid_9b5517e8_fk_SDLPost_postID` FOREIGN KEY (`postid`) REFERENCES `SDLPost` (`postID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SDLComment`
--

LOCK TABLES `SDLComment` WRITE;
/*!40000 ALTER TABLE `SDLComment` DISABLE KEYS */;
/*!40000 ALTER TABLE `SDLComment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SDLPost`
--

DROP TABLE IF EXISTS `SDLPost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SDLPost` (
  `postID` int(11) NOT NULL AUTO_INCREMENT,
  `posttitle` varchar(255) DEFAULT NULL,
  `posttext` longtext NOT NULL,
  `dateCreated` date DEFAULT NULL,
  `timeCreated` time(6) DEFAULT NULL,
  `datePosted` date DEFAULT NULL,
  `timePosted` time(6) DEFAULT NULL,
  `LastModifiedDate` date DEFAULT NULL,
  `LastModifiedTime` time(6) DEFAULT NULL,
  `createdby` varchar(254) DEFAULT NULL,
  `postActive` tinyint(1) NOT NULL,
  PRIMARY KEY (`postID`),
  KEY `SDLPost_createdby_2c88ac0e_fk_User_email` (`createdby`),
  CONSTRAINT `SDLPost_createdby_2c88ac0e_fk_User_email` FOREIGN KEY (`createdby`) REFERENCES `User` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SDLPost`
--

LOCK TABLES `SDLPost` WRITE;
/*!40000 ALTER TABLE `SDLPost` DISABLE KEYS */;
/*!40000 ALTER TABLE `SDLPost` ENABLE KEYS */;
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
INSERT INTO `StudentGroup` VALUES (1,1,'jonau@gmail.com'),(2,1,'dextergui@gmail.com'),(3,1,'joshualee@gmail.com'),(4,1,'marcuskho@gmail.com'),(5,1,'wesleychiau@gmail.com');
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
  `UserClass` int(11) DEFAULT NULL,
  PRIMARY KEY (`email`),
  UNIQUE KEY `username` (`username`),
  KEY `User_acceptedBy_5736f442_fk_User_email` (`acceptedBy`),
  KEY `User_lastModifiedBy_44c68aab_fk_User_email` (`lastModifiedBy`),
  KEY `User_UserClass_0adc9374_fk_UserClass_id` (`UserClass`),
  CONSTRAINT `User_UserClass_0adc9374_fk_UserClass_id` FOREIGN KEY (`UserClass`) REFERENCES `UserClass` (`id`),
  CONSTRAINT `User_acceptedBy_5736f442_fk_User_email` FOREIGN KEY (`acceptedBy`) REFERENCES `User` (`email`),
  CONSTRAINT `User_lastModifiedBy_44c68aab_fk_User_email` FOREIGN KEY (`lastModifiedBy`) REFERENCES `User` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES ('calvinsiak@gmail.com','calvinsiak','pbkdf2_sha256$100000$YQCNDFRDfaoZ$Hqam0KOUPfPdFNUkr24tqUUqXv1dJY7g86IFjIoAtNY=','Calvin Siak','2018-07-30','2018-07-30',NULL,1,NULL,0,1,0,NULL,'15:08:09.220286',NULL),('dextergui@gmail.com','dextergui','pbkdf2_sha256$100000$i7cHiS0d3d3N$h3yd4osIlhMpzBo8pvPkdaeFLdzpvYBGSqjHfrHQyU8=','Dexter Gui Zhang Yan','2018-07-30','2018-07-30',NULL,0,'karlkwan@gmail.com',0,1,0,'karlkwan@gmail.com','15:06:36.765291',1),('hubertus@gmail.com','hubertus','pbkdf2_sha256$100000$dNAzwqxhT8sX$4/jzXmkiHvL94OyQXkuWp6/uX0hT/f92Unui4DTJjF8=','Hubertus','2018-07-30','2018-07-30',NULL,1,NULL,0,1,0,NULL,'15:07:52.294998',NULL),('jonau@gmail.com','jonau','pbkdf2_sha256$100000$UFZnCKdzn27t$hdi3qmZugBXvGQgjOQsSglRodLyZ5GO9ZaRuyuXS+Ok=','Jonathan Au','2018-07-30','2018-07-30',NULL,0,'karlkwan@gmail.com',0,1,0,'karlkwan@gmail.com','15:06:16.557937',1),('joshualee@gmail.com','joshualee','pbkdf2_sha256$100000$r3lyAX0jG0rq$q+0z9w89eXGLIycfHH8uB7E0837XkRe7db9bbTa06eQ=','Joshua Lee','2018-07-30','2018-07-30',NULL,0,'karlkwan@gmail.com',0,1,0,'karlkwan@gmail.com','15:05:15.181086',1),('junietan@gmail.com','junietan','pbkdf2_sha256$100000$ICazH8jB13MF$Xkw3XMulazS5yZP8vsvKa+KnBK7NKL1TbwVpUEVDU84=','Junie Tan','2018-07-30','2018-07-30',NULL,1,NULL,0,1,0,NULL,'15:07:34.130879',NULL),('karlkwan@gmail.com','karlkwan','pbkdf2_sha256$100000$XgUor61qLNBn$QWlVuwXDD4fhmpm72s/FrRSI/RLkavk2Z6MNvrQf4jc=','',NULL,NULL,'2018-07-30 05:54:44.386537',1,NULL,1,0,0,NULL,NULL,NULL),('marcuskho@gmail.com','marcuskho','pbkdf2_sha256$100000$9ukwjQwIkQYQ$BX/YemQusy8DiUiXaSiKm0/M/MVAaS1eIdN4mQl9gwc=','Marcus Kho Han Kiat','2018-07-30','2018-07-30',NULL,0,'karlkwan@gmail.com',0,1,0,'karlkwan@gmail.com','15:06:50.440879',1),('wesleychiau@gmail.com','wesleychiau','pbkdf2_sha256$100000$CSz3XdOZsIyZ$WC9iVw5fzhlrAnwDRrflmlwOSdv/9N88thKhKIsfemA=','Wesley Chiau','2018-07-30','2018-07-30',NULL,0,'karlkwan@gmail.com',0,1,0,'karlkwan@gmail.com','15:07:06.751242',1);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UserClass`
--

LOCK TABLES `UserClass` WRITE;
/*!40000 ALTER TABLE `UserClass` DISABLE KEYS */;
INSERT INTO `UserClass` VALUES (1,'DISM/FT/3A/64');
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
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add sdl post',1,'add_sdlpost'),(2,'Can change sdl post',1,'change_sdlpost'),(3,'Can delete sdl post',1,'delete_sdlpost'),(4,'Can add sdl comment',2,'add_sdlcomment'),(5,'Can change sdl comment',2,'change_sdlcomment'),(6,'Can delete sdl comment',2,'delete_sdlcomment'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add fake user class',4,'add_fakeuserclass'),(11,'Can change fake user class',4,'change_fakeuserclass'),(12,'Can delete fake user class',4,'delete_fakeuserclass'),(13,'Can add user class',5,'add_userclass'),(14,'Can change user class',5,'change_userclass'),(15,'Can delete user class',5,'delete_userclass'),(16,'Can add group range',6,'add_grouprange'),(17,'Can change group range',6,'change_grouprange'),(18,'Can delete group range',6,'delete_grouprange'),(19,'Can add student group',7,'add_studentgroup'),(20,'Can change student group',7,'change_studentgroup'),(21,'Can delete student group',7,'delete_studentgroup'),(22,'Can add group',8,'add_group'),(23,'Can change group',8,'change_group'),(24,'Can delete group',8,'delete_group'),(25,'Can add fake student group',9,'add_fakestudentgroup'),(26,'Can change fake student group',9,'change_fakestudentgroup'),(27,'Can delete fake student group',9,'delete_fakestudentgroup'),(28,'Can add range students',10,'add_rangestudents'),(29,'Can change range students',10,'change_rangestudents'),(30,'Can delete range students',10,'delete_rangestudents'),(31,'Can add unavailable ports',11,'add_unavailableports'),(32,'Can change unavailable ports',11,'change_unavailableports'),(33,'Can delete unavailable ports',11,'delete_unavailableports'),(34,'Can add mcq options',12,'add_mcqoptions'),(35,'Can change mcq options',12,'change_mcqoptions'),(36,'Can delete mcq options',12,'delete_mcqoptions'),(37,'Can add student questions',13,'add_studentquestions'),(38,'Can change student questions',13,'change_studentquestions'),(39,'Can delete student questions',13,'delete_studentquestions'),(40,'Can add range',14,'add_range'),(41,'Can change range',14,'change_range'),(42,'Can delete range',14,'delete_range'),(43,'Can add question topic',15,'add_questiontopic'),(44,'Can change question topic',15,'change_questiontopic'),(45,'Can delete question topic',15,'delete_questiontopic'),(46,'Can add fake range',16,'add_fakerange'),(47,'Can change fake range',16,'change_fakerange'),(48,'Can delete fake range',16,'delete_fakerange'),(49,'Can add questions',17,'add_questions'),(50,'Can change questions',17,'change_questions'),(51,'Can delete questions',17,'delete_questions'),(52,'Can add student hints',18,'add_studenthints'),(53,'Can change student hints',18,'change_studenthints'),(54,'Can delete student hints',18,'delete_studenthints'),(55,'Can add log entry',19,'add_logentry'),(56,'Can change log entry',19,'change_logentry'),(57,'Can delete log entry',19,'delete_logentry'),(58,'Can add permission',20,'add_permission'),(59,'Can change permission',20,'change_permission'),(60,'Can delete permission',20,'delete_permission'),(61,'Can add group',21,'add_group'),(62,'Can change group',21,'change_group'),(63,'Can delete group',21,'delete_group'),(64,'Can add content type',22,'add_contenttype'),(65,'Can change content type',22,'change_contenttype'),(66,'Can delete content type',22,'delete_contenttype'),(67,'Can add session',23,'add_session'),(68,'Can change session',23,'change_session'),(69,'Can delete session',23,'delete_session'),(70,'Can add fake user',24,'add_fakeuser'),(71,'Can change fake user',24,'change_fakeuser'),(72,'Can delete fake user',24,'delete_fakeuser');
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
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (9,'accounts','fakestudentgroup'),(24,'accounts','fakeuser'),(4,'accounts','fakeuserclass'),(8,'accounts','group'),(6,'accounts','grouprange'),(7,'accounts','studentgroup'),(3,'accounts','user'),(5,'accounts','userclass'),(19,'admin','logentry'),(21,'auth','group'),(20,'auth','permission'),(22,'contenttypes','contenttype'),(16,'ranges','fakerange'),(12,'ranges','mcqoptions'),(17,'ranges','questions'),(15,'ranges','questiontopic'),(14,'ranges','range'),(10,'ranges','rangestudents'),(18,'ranges','studenthints'),(13,'ranges','studentquestions'),(11,'ranges','unavailableports'),(2,'SDL','sdlcomment'),(1,'SDL','sdlpost'),(23,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'accounts','0001_initial','2018-07-30 05:53:09.937939'),(2,'SDL','0001_initial','2018-07-30 05:53:10.054251'),(3,'SDL','0002_auto_20180730_1351','2018-07-30 05:53:11.377660'),(4,'ranges','0001_initial','2018-07-30 05:53:11.479352'),(5,'contenttypes','0001_initial','2018-07-30 05:53:11.661072'),(6,'contenttypes','0002_remove_content_type_name','2018-07-30 05:53:12.054599'),(7,'auth','0001_initial','2018-07-30 05:53:13.368965'),(8,'auth','0002_alter_permission_name_max_length','2018-07-30 05:53:13.432524'),(9,'auth','0003_alter_user_email_max_length','2018-07-30 05:53:13.494514'),(10,'auth','0004_alter_user_username_opts','2018-07-30 05:53:13.557150'),(11,'auth','0005_alter_user_last_login_null','2018-07-30 05:53:13.619361'),(12,'auth','0006_require_contenttypes_0002','2018-07-30 05:53:13.638761'),(13,'auth','0007_alter_validators_add_error_messages','2018-07-30 05:53:13.711804'),(14,'auth','0008_alter_user_username_max_length','2018-07-30 05:53:13.761924'),(15,'auth','0009_alter_user_last_name_max_length','2018-07-30 05:53:13.828195'),(16,'accounts','0002_auto_20180730_1351','2018-07-30 05:53:20.608748'),(17,'admin','0001_initial','2018-07-30 05:53:21.214129'),(18,'admin','0002_logentry_remove_auto_add','2018-07-30 05:53:21.316298'),(19,'ranges','0002_auto_20180730_1351','2018-07-30 05:53:32.550423'),(20,'sessions','0001_initial','2018-07-30 05:53:32.755790'),(21,'accounts','0003_auto_20180730_1502','2018-07-30 07:03:03.754699');
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
INSERT INTO `django_session` VALUES ('28lgqjqzhwkp1ocrm1uz1eabgv3xuyof','NmZmMmYzOGJmZDVlYzFlNDA4OTk5NzFiOWVjNDQ1ZTQzNGZjYmM3MDp7IlRGIjpmYWxzZSwiX2F1dGhfdXNlcl9pZCI6Imthcmxrd2FuQGdtYWlsLmNvbSIsInF1ZXN0aW9uc2NhcnQiOltdLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJhY2NvdW50cy5mb3Jtcy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwNmUyZDk5NTI3YWEzNDEwYjA4YTk2NTE3NTc3ZmYzZDFkMWRjNzY2IiwicXVlc3Rpb25pZCI6M30=','2018-08-13 08:19:01.306624');
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

-- Dump completed on 2018-07-30 16:20:35
