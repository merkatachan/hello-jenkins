-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: dev
-- ------------------------------------------------------
-- Server version	5.7.17-log

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add tbl project type list',1,'add_tblprojecttypelist'),(2,'Can change tbl project type list',1,'change_tblprojecttypelist'),(3,'Can delete tbl project type list',1,'delete_tblprojecttypelist'),(4,'Can add tbl capex',2,'add_tblcapex'),(5,'Can change tbl capex',2,'change_tblcapex'),(6,'Can delete tbl capex',2,'delete_tblcapex'),(7,'Can add tbl opex',3,'add_tblopex'),(8,'Can change tbl opex',3,'change_tblopex'),(9,'Can delete tbl opex',3,'delete_tblopex'),(10,'Can add tbl mine product list',4,'add_tblmineproductlist'),(11,'Can change tbl mine product list',4,'change_tblmineproductlist'),(12,'Can delete tbl mine product list',4,'delete_tblmineproductlist'),(13,'Can add tbl mine',5,'add_tblmine'),(14,'Can change tbl mine',5,'change_tblmine'),(15,'Can delete tbl mine',5,'delete_tblmine'),(16,'Can add tbl commodity',6,'add_tblcommodity'),(17,'Can change tbl commodity',6,'change_tblcommodity'),(18,'Can delete tbl commodity',6,'delete_tblcommodity'),(19,'Can add tbl plant product list',7,'add_tblplantproductlist'),(20,'Can change tbl plant product list',7,'change_tblplantproductlist'),(21,'Can delete tbl plant product list',7,'delete_tblplantproductlist'),(22,'Can add tbl mine product',8,'add_tblmineproduct'),(23,'Can change tbl mine product',8,'change_tblmineproduct'),(24,'Can delete tbl mine product',8,'delete_tblmineproduct'),(25,'Can add tbl commodity list',9,'add_tblcommoditylist'),(26,'Can change tbl commodity list',9,'change_tblcommoditylist'),(27,'Can delete tbl commodity list',9,'delete_tblcommoditylist'),(28,'Can add tbl project',10,'add_tblproject'),(29,'Can change tbl project',10,'change_tblproject'),(30,'Can delete tbl project',10,'delete_tblproject'),(31,'Can add tbl plant product',11,'add_tblplantproduct'),(32,'Can change tbl plant product',11,'change_tblplantproduct'),(33,'Can delete tbl plant product',11,'delete_tblplantproduct'),(34,'Can add log entry',12,'add_logentry'),(35,'Can change log entry',12,'change_logentry'),(36,'Can delete log entry',12,'delete_logentry'),(37,'Can add permission',13,'add_permission'),(38,'Can change permission',13,'change_permission'),(39,'Can delete permission',13,'delete_permission'),(40,'Can add group',14,'add_group'),(41,'Can change group',14,'change_group'),(42,'Can delete group',14,'delete_group'),(43,'Can add user',15,'add_user'),(44,'Can change user',15,'change_user'),(45,'Can delete user',15,'delete_user'),(46,'Can add content type',16,'add_contenttype'),(47,'Can change content type',16,'change_contenttype'),(48,'Can delete content type',16,'delete_contenttype'),(49,'Can add session',17,'add_session'),(50,'Can change session',17,'change_session'),(51,'Can delete session',17,'delete_session'),(52,'Can add tbl users',18,'add_tblusers'),(53,'Can change tbl users',18,'change_tblusers'),(54,'Can delete tbl users',18,'delete_tblusers'),(55,'Can add tbl mine',19,'add_tblmine'),(56,'Can change tbl mine',19,'change_tblmine'),(57,'Can delete tbl mine',19,'delete_tblmine'),(58,'Can add tbl company',20,'add_tblcompany'),(59,'Can change tbl company',20,'change_tblcompany'),(60,'Can delete tbl company',20,'delete_tblcompany');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
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
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (12,'admin','logentry'),(14,'auth','group'),(13,'auth','permission'),(15,'auth','user'),(16,'contenttypes','contenttype'),(17,'sessions','session'),(2,'setup','tblcapex'),(6,'setup','tblcommodity'),(9,'setup','tblcommoditylist'),(5,'setup','tblmine'),(8,'setup','tblmineproduct'),(4,'setup','tblmineproductlist'),(3,'setup','tblopex'),(11,'setup','tblplantproduct'),(7,'setup','tblplantproductlist'),(10,'setup','tblproject'),(1,'setup','tblprojecttypelist'),(20,'signup','tblcompany'),(19,'signup','tblmine'),(18,'signup','tblusers');
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
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'setup','0001_initial','2017-02-26 14:56:54.241503'),(2,'setup','0002_auto_20170226_0819','2017-02-26 14:56:54.919550'),(3,'setup','0003_tblcapex','2017-02-26 14:56:56.265074'),(4,'contenttypes','0001_initial','2017-02-26 15:06:43.310301'),(5,'auth','0001_initial','2017-02-26 15:06:52.832853'),(6,'admin','0001_initial','2017-02-26 15:06:54.845309'),(7,'admin','0002_logentry_remove_auto_add','2017-02-26 15:06:54.912734'),(8,'contenttypes','0002_remove_content_type_name','2017-02-26 15:06:56.231049'),(9,'auth','0002_alter_permission_name_max_length','2017-02-26 15:06:57.098762'),(10,'auth','0003_alter_user_email_max_length','2017-02-26 15:06:57.897679'),(11,'auth','0004_alter_user_username_opts','2017-02-26 15:06:58.113984'),(12,'auth','0005_alter_user_last_login_null','2017-02-26 15:06:58.989764'),(13,'auth','0006_require_contenttypes_0002','2017-02-26 15:06:59.022593'),(14,'auth','0007_alter_validators_add_error_messages','2017-02-26 15:06:59.068849'),(15,'auth','0008_alter_user_username_max_length','2017-02-26 15:06:59.676217'),(16,'sessions','0001_initial','2017-02-26 15:07:22.576117'),(17,'signup','0001_initial','2017-02-26 15:40:56.181529'),(18,'signup','0002_auto_20170218_1455','2017-02-26 15:40:56.314577'),(19,'signup','0003_auto_20170218_1503','2017-02-26 15:40:56.493213'),(20,'signup','0004_auto_20170218_1508','2017-02-26 15:40:56.579943'),(21,'signup','0005_auto_20170226_0736','2017-02-26 15:40:56.617395'),(22,'login','0001_initial','2017-02-26 15:41:04.273192');
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
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('0e2zwhde9o87p1dl2z4obm28fvkoqx69','N2RjYTc3NDgxYTQxMDllMTJhMmRlMDdlNGEzMWRlZWY0M2QwMGQxMDp7Il9zZXNzaW9uX2V4cGlyeSI6MCwidXNlcm5hbWUiOiJrcmlzdGFmdW5nIiwidXNlcklEIjoiMSIsImZpcnN0bmFtZSI6IktyaXN0YSIsIm1pbmVJRCI6IjEifQ==','2017-07-06 05:48:32.599051'),('0paz1tpe29c9kpbi3xljouww03rlq6qe','ZjM2NTA3MWQxMDc0MWE4MWIxMjI2NTU3NmRiODVjNDE5YzcwMzRkMjp7Il9zZXNzaW9uX2V4cGlyeSI6MCwidXNlcm5hbWUiOiJrcmlzdGFmdW5nIiwiZmlyc3RuYW1lIjoiS3Jpc3RhIiwidXNlcklEIjoiMSIsIm1pbmVJRCI6IjEifQ==','2017-06-07 21:26:40.063630'),('1cirhuc1b7fpe6hzrp1mtte50be5alf6','ODk5YTg2YjViNTQ3ZGMxMWY0YWIxNmUzZmMzNDEwNjFiNWY1M2I5Yzp7ImNvbXBhbnlQcm92aW5jZSI6ImNjIiwiY29tcGFueU5hbWUiOiJjYyIsImNvbXBhbnlQaG9uZSI6ImNjIiwibWluZUNvdW50cnkiOiJjYyIsIm1pbmVBZGRyZXNzIjoiY2MiLCJtaW5lUG9zdGFsQ29kZSI6ImNjIiwiY29tcGFueUNpdHkiOiJjYyIsImNvbXBhbnlQb3N0YWxDb2RlIjoiY2MiLCJtaW5lTmFtZSI6ImNjIiwibWluZVBob25lIjoiY2MiLCJjb21wYW55QWRkcmVzcyI6ImNjIiwibWluZUNpdHkiOiJjYyIsIm1pbmVQcm92aW5jZSI6ImNjIiwiY29tcGFueUNvdW50cnkiOiJjYyJ9','2017-07-29 23:33:55.551184'),('1ipw857d1wz1uarlsfsss5ec7ztapdxh','ODI1NzBmNTFjNjJhODJkM2E5ZjEzYWU3ZDUyNjEwOWRlYjMxZmUwNjp7InVzZXJJRCI6IjEiLCJfc2Vzc2lvbl9leHBpcnkiOjAsInVzZXJuYW1lIjoia3Jpc3RhZnVuZyIsImZpcnN0bmFtZSI6IktyaXN0YSIsIm1pbmVJRCI6IjEifQ==','2017-07-05 20:41:14.393144'),('1r9l5zr2tbiejux1bbfqy3jnd8rhtno4','YTMzZTJiMzc0NmJkNzM1MTkxMmZmYmMwOGE5Mjg0YTNiNDJjMTljZjp7Im1pbmVJRCI6IjE0IiwidXNlcklEIjoiOSIsInVzZXJuYW1lIjoiY2MiLCJmaXJzdG5hbWUiOiJjYyIsIl9zZXNzaW9uX2V4cGlyeSI6MH0=','2017-08-02 18:41:05.890731'),('21fxxbsubgdfiz6dwao9yf9v3wxzzc86','N2RjYTc3NDgxYTQxMDllMTJhMmRlMDdlNGEzMWRlZWY0M2QwMGQxMDp7Il9zZXNzaW9uX2V4cGlyeSI6MCwidXNlcm5hbWUiOiJrcmlzdGFmdW5nIiwidXNlcklEIjoiMSIsImZpcnN0bmFtZSI6IktyaXN0YSIsIm1pbmVJRCI6IjEifQ==','2017-07-06 02:25:29.991799'),('28l22elz41uju4pyi2g49mc90k6tnwy5','ZWViOGUwODRlODJjZmU2MGQyZDdmODllYzM5NmI5ODRlZWE4MjNjMDp7Im1pbmVJRCI6IjEiLCJ1c2VySUQiOiIxIiwidXNlcm5hbWUiOiJrcmlzdGFmdW5nIiwiX3Nlc3Npb25fZXhwaXJ5IjowLCJmaXJzdG5hbWUiOiJLcmlzdGEifQ==','2017-06-17 17:56:51.160861'),('2a7usacocmjfyedowgs8vkh2jo6yrghn','ZGJhMWRkMjc2OWQ1MDhjNWNiNzhjMDQ1NzRmOTlhMmE2NWRmZWZiNjp7ImZpcnN0bmFtZSI6IktyaXN0YSIsIm1pbmVJRCI6IjEiLCJ1c2VybmFtZSI6ImtyaXN0YWZ1bmciLCJ1c2VySUQiOiIxIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2017-03-12 15:59:12.351224'),('2gqhlwa3reoirmyp0w1qs37aa1oczgjd','ODI1NzBmNTFjNjJhODJkM2E5ZjEzYWU3ZDUyNjEwOWRlYjMxZmUwNjp7InVzZXJJRCI6IjEiLCJfc2Vzc2lvbl9leHBpcnkiOjAsInVzZXJuYW1lIjoia3Jpc3RhZnVuZyIsImZpcnN0bmFtZSI6IktyaXN0YSIsIm1pbmVJRCI6IjEifQ==','2017-07-06 00:01:15.640178'),('54z6p1048xw1mzt7rz9z5uulb6xwmt6w','MGE4NjcyMzEyOGYzMDViMzU4ZTA3ZmQ3M2U0NmY0ZThiMTgzMGU5Nzp7Il9zZXNzaW9uX2V4cGlyeSI6MCwibWluZUlEIjoiMTQiLCJ1c2VybmFtZSI6ImNjIiwidXNlcklEIjoiOSIsImZpcnN0bmFtZSI6ImNjIn0=','2018-02-03 05:56:47.716573'),('6pq5dm9ew2yad6lujt44fw2b2civ4k9i','OGEyOTJjNDA4ZGY5YzMzMWM0MmExMWU1ZmI1OGQyYWI0YzQyZWZjYTp7ImRlbENvbW1vZGl0aWVzIjpbIjMiLCIzMyIsIjUwIl0sInByb2plY3RTdGFydE1vbnRoIjoxLCJ1c2VybmFtZSI6ImNjIiwidXNlcklEIjoiOSIsInByb2plY3RTdGFydERheSI6MSwiTE9NIjoyLCJwcm9qZWN0U3RhcnRZZWFyIjoyMDE3LCJmaXJzdG5hbWUiOiJjYyIsIm1pbmVJRCI6IjE0IiwibWFpbkNvbW1vZGl0aWVzIjpbIjIyIl0sInByb2plY3RQbGFudFByb2R1Y3RzIjpbIjEiLCIyIl0sIl9zZXNzaW9uX2V4cGlyeSI6MCwicHJvamVjdE1pbmVQcm9kdWN0cyI6WyIxIiwiMiJdLCJ5ZWFyQ291bnQiOjIsInByb2plY3RUeXBlIjoiMSJ9','2017-08-01 01:45:35.487797'),('7tg6mxhy42lyvsw3084v06d85oit53z9','NDE4MTdhYTg5Zjk3MjM2MmRlNWNhYWM3NzM4NTM3NjA5MmE2MTVkODp7InVzZXJuYW1lIjoia3Jpc3RhZnVuZyIsIm1pbmVJRCI6IjEiLCJfc2Vzc2lvbl9leHBpcnkiOjAsInVzZXJJRCI6IjEiLCJmaXJzdG5hbWUiOiJLcmlzdGEifQ==','2017-03-23 01:11:44.680249'),('8pn1x9nc7ngo5gfo2u3hs5nko5j9t172','M2Q1ZmEwNzMyNmEzMTA2NjQ1NDkyYzJlM2RmMTA3ZDZlM2M2NzZjNDp7Il9zZXNzaW9uX2V4cGlyeSI6MCwiZmlyc3RuYW1lIjoiYWJjIiwidXNlcm5hbWUiOiJhYmMiLCJ1c2VySUQiOiIyIiwibWluZUlEIjoiMiJ9','2017-05-25 20:10:08.050274'),('98ks3wp84l4qx5zftzz9wvzqhmfn06h4','YTEwMzExYzlkMDI3YjU5MDFkN2IyMWY1NjI0YjMxYmE3YzVlYzI2MDp7Im1pbmVJRCI6IjE1IiwidXNlcm5hbWUiOiJ3ZXMiLCJmaXJzdG5hbWUiOiJ3ZXMiLCJfc2Vzc2lvbl9leHBpcnkiOjAsInVzZXJJRCI6IjEwIn0=','2017-09-05 19:46:49.803304'),('aib3hxlaux7up9pyrgg1wbe0mrp8tm2f','NmM5Mzc5Zjg4OTlkZjZmNGM5OTFiMGE5MjY4YjBiZWYzYTdjZDcwNTp7Im1haW5Db21tb2RpdGllcyI6WyIyMiJdLCJmaXJzdG5hbWUiOiJjYyIsImRlbENvbW1vZGl0aWVzIjpbIjMiLCIzMyIsIjUwIl0sInByb2plY3RUeXBlIjoiMSIsImNvbW1OYW1lTGlzdCI6WyJGZSIsIkFsIiwiTW4iLCJTaSJdLCJwcm9qZWN0U3RhcnRZZWFyIjoyMDE3LCJ5ZWFyQ291bnQiOjEsInVzZXJJRCI6IjkiLCJtaW5lSUQiOiIxNCIsImlkTGlzdCI6WzIyLDMsMzMsNTBdLCJ1c2VybmFtZSI6ImNjIiwicHJvamVjdFN0YXJ0RGF5IjoxLCJfc2Vzc2lvbl9leHBpcnkiOjAsInByb2plY3RTdGFydE1vbnRoIjoxLCJMT00iOjEsInByb2plY3RNaW5lUHJvZHVjdHMiOlsiMSIsIjIiXSwicHJvamVjdFBsYW50UHJvZHVjdHMiOlsiMSIsIjIiXX0=','2017-08-07 16:30:47.170370'),('b9p1k17fm2qmgejfad9oujlkv74pubjq','NDNjZGNhNzYzZjhhMmE3YzU2Mjg3NjBjODI1MGU5OWU2MjdhYzRhOTp7Il9zZXNzaW9uX2V4cGlyeSI6MCwibWluZUlEIjoiMSIsImZpcnN0bmFtZSI6IktyaXN0YSIsInVzZXJuYW1lIjoia3Jpc3RhZnVuZyIsInVzZXJJRCI6IjEifQ==','2017-05-01 16:03:55.553960'),('ba6jb4tbschjke53tvfox4mr0avejkwy','MzY0ZjM2ZmFlYmI3OTVmNjIwNjY2NmUwMzI5OWY3ZTY5MjRjZjc0Nzp7Im1pbmVJRCI6IjE1IiwidXNlcklEIjoiMTAiLCJ1c2VybmFtZSI6IndlcyIsIl9zZXNzaW9uX2V4cGlyeSI6MCwiZmlyc3RuYW1lIjoid2VzIn0=','2017-12-27 14:32:04.396067'),('bmcc9x1gtq96mfvuag1exn9orp6i5qo8','YmZkZDEwZDMyZmUxNzNkMzM2NzQzZWM1ZWE0Njg0M2U0N2FlOTMwMjp7Im1pbmVJRCI6IjE0IiwiX3Nlc3Npb25fZXhwaXJ5IjowLCJmaXJzdG5hbWUiOiJjYyIsInVzZXJuYW1lIjoiY2MiLCJ1c2VySUQiOiI5In0=','2017-09-30 19:25:09.361921'),('bmoasoi2dcj2n5jmpvrra4s2s0eq77u4','MjQwYjkxMTIzY2Y0NGM1Mjk5NDViOGNlN2EzZGE2MTdiZjVlZjVmNDp7ImZpcnN0bmFtZSI6ImFiYyIsIl9zZXNzaW9uX2V4cGlyeSI6MCwidXNlcm5hbWUiOiJhYmMiLCJtaW5lSUQiOiIyIiwidXNlcklEIjoiMiJ9','2017-05-23 23:44:08.857354'),('chxueaaj8pjhae0q6klxo3zpnpcmg473','YTMzZTJiMzc0NmJkNzM1MTkxMmZmYmMwOGE5Mjg0YTNiNDJjMTljZjp7Im1pbmVJRCI6IjE0IiwidXNlcklEIjoiOSIsInVzZXJuYW1lIjoiY2MiLCJmaXJzdG5hbWUiOiJjYyIsIl9zZXNzaW9uX2V4cGlyeSI6MH0=','2017-08-01 19:39:23.483014'),('czd8hhtqu5k2mielrb8vdndiaai158ps','MDg4ZTliMmZkMDI0NmU4ZTVmYjM0MmUxNTBhNjQwN2IyMzQ0ZTdkNzp7IndpemFyZF9zaWdudXBfd2l6YXJkIjp7InN0ZXBfZGF0YSI6e30sInN0ZXAiOiJjb21wYW55Iiwic3RlcF9maWxlcyI6e30sImV4dHJhX2RhdGEiOnt9fSwiY29tcGFueUNvdW50cnkiOiJhMSIsImNvbXBhbnlBZGRyZXNzIjoiYTEiLCJtaW5lUG9zdGFsQ29kZSI6ImExIiwiY29tcGFueVByb3ZpbmNlIjoiYTEiLCJjb21wYW55UG9zdGFsQ29kZSI6ImExIiwibWluZVByb3ZpbmNlIjoiYTEiLCJtaW5lQ291bnRyeSI6ImExIiwibWluZUNpdHkiOiJhMSIsIm1pbmVQaG9uZSI6ImExIiwiY29tcGFueU5hbWUiOiJhMSIsIm1pbmVBZGRyZXNzIjoiYTEiLCJjb21wYW55UGhvbmUiOiJhMSIsIm1pbmVOYW1lIjoiYTEiLCJjb21wYW55Q2l0eSI6ImExIn0=','2017-07-21 16:34:39.646147'),('dqj91hkkw4otncvfu8lh0iz7unqrxwp1','MmZiMjU0NzFmMjg1NjAzMGRjOGVkNTAxZmRiNjA0M2ZkNzJkZmFjMzp7Im1pbmVJRCI6IjEiLCJfc2Vzc2lvbl9leHBpcnkiOjAsImZpcnN0bmFtZSI6IktyaXN0YSIsInVzZXJuYW1lIjoia3Jpc3RhZnVuZyIsInVzZXJJRCI6IjEifQ==','2017-04-27 16:27:59.703111'),('ea9lcvj8vt14os29apd9tnxkgy0i6325','NjQ1YTNmOGJkYmRjNzY4OTlmYWJhNjNhM2RhYzM0NWE3NmI4MWFkNTp7Il9zZXNzaW9uX2V4cGlyeSI6MCwiZmlyc3RuYW1lIjoiY2MiLCJtaW5lSUQiOiIxNCIsInVzZXJJRCI6IjkiLCJ1c2VybmFtZSI6ImNjIn0=','2017-12-11 06:12:23.151254'),('etky3lr9nlzjue7rftbojzr7zt7vdkth','Mjg4ZTE4N2M5ZDBhYzQyYzk4M2E1ZDhhY2I0MGRkNzRhY2I3MzA2ZDp7InVzZXJuYW1lIjoia3Jpc3RhZnVuZyIsInVzZXJJRCI6IjEiLCJfc2Vzc2lvbl9leHBpcnkiOjAsIm1pbmVJRCI6IjEiLCJmaXJzdG5hbWUiOiJLcmlzdGEifQ==','2017-07-05 16:17:03.942906'),('ev4laqpfz30s1amip9qna3k39mn2fs56','N2RjYTc3NDgxYTQxMDllMTJhMmRlMDdlNGEzMWRlZWY0M2QwMGQxMDp7Il9zZXNzaW9uX2V4cGlyeSI6MCwidXNlcm5hbWUiOiJrcmlzdGFmdW5nIiwidXNlcklEIjoiMSIsImZpcnN0bmFtZSI6IktyaXN0YSIsIm1pbmVJRCI6IjEifQ==','2017-07-09 16:53:09.682009'),('hhv16op8ifhtubulps7mu5patlok6g9i','MzQ5YTE0MjRlMTIyMTdlZGYxMTZlNjc1ZTA5ZTQ5NDQyN2ZkMzYzNjp7Im1pbmVJRCI6IjEiLCJ1c2VybmFtZSI6ImtyaXN0YWZ1bmciLCJmaXJzdG5hbWUiOiJLcmlzdGEiLCJ1c2VySUQiOiIxIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2017-05-04 10:10:00.851208'),('hsqb417on7gdfp7irbz4mztyb4bmeu3x','Mjg3MzliZDQ2MzA5ZjM3NzRhYWQ5OTJmMzM1MTU3MmM4NjE4NTVmZDp7Il9zZXNzaW9uX2V4cGlyeSI6MCwidXNlcm5hbWUiOiJrcmlzdGFmdW5nIiwidXNlcklEIjoiMSIsIm1pbmVJRCI6IjEiLCJmaXJzdG5hbWUiOiJLcmlzdGEifQ==','2017-05-10 14:28:02.265804'),('hy9g97i5l63dpvytdyo1codbilywh6b2','OGQ1YWU0YzMyNjNjNDgxZGFlODAwYWFkNjRlMTk1MzZkODJjNGVjMjp7ImZpcnN0bmFtZSI6ImIxIiwiX3Nlc3Npb25fZXhwaXJ5IjowLCJtaW5lSUQiOiIxMyIsInVzZXJuYW1lIjoiYjEiLCJ1c2VySUQiOiI4In0=','2017-07-28 17:19:40.517536'),('i86fjb9njrj0dsv72e8gt93wj3mnin4i','YjA4Nzk3MWEzYTk1MzgwOTI5OGJkYWZmOWE1Nzc0NjU2N2FkYTIwMjp7ImZpcnN0bmFtZSI6IktyaXN0YSIsIl9zZXNzaW9uX2V4cGlyeSI6MCwibWluZUlEIjoiMSIsInVzZXJJRCI6IjEiLCJ1c2VybmFtZSI6ImtyaXN0YWZ1bmcifQ==','2017-06-28 16:27:39.438685'),('iwmd14yy1ucfxpfesj8uqyl8ii1smidd','ZTI1NWU4MmY1YTU4NjU3ZGJhYmU4YjViOTYyZWM5ZjgzODViYWQwODp7ImZpcnN0bmFtZSI6IndlcyIsInVzZXJJRCI6IjEwIiwibWluZUlEIjoiMTUiLCJfc2Vzc2lvbl9leHBpcnkiOjAsInVzZXJuYW1lIjoid2VzIn0=','2017-09-06 19:37:11.279667'),('j4eea6jc8vtqkdxym3rt731s0at4xkl4','YTNmYmU3ZjQwMzRlNTgzOGIwZDA3ZWMwZGVjZjRjZDgyNzdiMGM4NDp7InByZVN0cmlwIjpbMTUuMzEsMC4wXSwiR0EiOlswLjAsMC4wXSwiU3RvY2twaWxlMk1pbk1heFBlbmFsdHkzMyI6MC4wLCJTdG9ja3BpbGUxTWluR3JhZGU1MCI6NC41LCJTdG9ja3BpbGUyUHJlbWl1bTMzIjowLjAsIlN0b2NrcGlsZTFNaW5HcmFkZTMiOjEuMCwiU3RvY2twaWxlMkluY3JlbWVudHMzIjoxMDAuMCwiU3RvY2twaWxlMk1heFBlbmFsdHkzIjowLjIsInJveWFsdGllcyI6WzMuODYsMS43NV0sIlN0b2NrcGlsZTFNaW5HcmFkZTIyIjo2MC4wLCJtaW5pbmciOlszNC42OCw0NS4xOV0sIlN0b2NrcGlsZTJQcmVtaXVtMyI6MC4wLCJTdG9ja3BpbGUxTWluR3JhZGUzMyI6MC4wLCJTdG9ja3BpbGUyUHJlbWl1bTUwIjowLjAsIkdBU2l0ZSI6WzQuNjYsNi4yMV0sIlN0b2NrcGlsZTFNaW5NYXhQZW5hbHR5MyI6MC4yLCJjbG9zdXJlUmVoYWJBc3N1cmUiOlswLjAsMC4wXSwiU3RvY2twaWxlMU1heFBlbmFsdHk1MCI6MC4wLCJTdG9ja3BpbGUyUHJlbWl1bTIyIjowLjAsIlN0b2NrcGlsZTFNYXhQZW5hbHR5MzMiOjAuMCwiU3RvY2twaWxlMU1heFBlbmFsdHkyMiI6MC4wLCJwcm9qZWN0UGxhbnRQcm9kdWN0cyI6WyIxIiwiMiJdLCJTdG9ja3BpbGUxTWF4UGVuYWx0eTMiOjAuMCwiZGV3YXRlcmluZyI6WzAuOTQsMS4yNV0sIlN0b2NrcGlsZTFNYXhHcmFkZTMiOjEuMCwiU3RvY2twaWxlMUluY3JlbWVudHMyMiI6MS4wLCJTdG9ja3BpbGUyTWluTWF4UGVuYWx0eTIyIjoyLjAsIlN0b2NrcGlsZTFNaW5QZW5hbHR5MyI6MC4yLCJTdG9ja3BpbGUyTWF4UGVuYWx0eTMzIjowLjAsIm51bVN0b2NrcGlsZXMiOjIsIlN0b2NrcGlsZTFJbmNyZW1lbnRzNTAiOjEuMCwiU3RvY2twaWxlMk1heEdyYWRlMzMiOjAuMCwiaW5mcmFzdHJ1Y3R1cmUiOlswLjAsMC4wXSwiR0FSb29tQm9hcmRGSUZPIjpbNC4yNiw1LjA5XSwiY29tbU5hbWVMaXN0IjpbIkZlIiwiQWwiLCJNbiIsIlNpIl0sImluZnJhRGlyZWN0Q29zdCI6WzExMS44MiwwLjBdLCJTdG9ja3BpbGUxTWluTWF4UGVuYWx0eTIyIjoxLjUsInByb2plY3RTdGFydERheSI6MSwiU3RvY2twaWxlMUluY3JlbWVudHMzMyI6MS4wLCJpZExpc3QiOlsyMiwzLDMzLDUwXSwiTE9NIjoyLCJ5ZWFyQ291bnQiOjIsIndvcmtDYXBDdXJyZW50UHJvZCI6WzE0LjgxLDAuMF0sIlN0b2NrcGlsZTFJbmNyZW1lbnRzMyI6MTAwLjAsIlN0b2NrcGlsZTFQcmVtaXVtNTAiOi0wLjc1LCJwcm9qZWN0U3RhcnRZZWFyIjoyMDE4LCJTdG9ja3BpbGUxTWluUGVuYWx0eTMzIjowLjAsIlN0b2NrcGlsZTJNaW5HcmFkZTIyIjo1Ni4wLCJTdG9ja3BpbGUyTWluTWF4UGVuYWx0eTUwIjowLjc1LCJoYXVsaW5nIjpbOC4xNSw4LjY3XSwiU3RvY2twaWxlMk1pbkdyYWRlMyI6MS4wLCJkZWxDb21tb2RpdGllcyI6WyIzIiwiMzMiLCI1MCJdLCJfc2Vzc2lvbl9leHBpcnkiOjAsIlN0b2NrcGlsZTFNYXhHcmFkZTUwIjo0LjUsInVzZXJuYW1lIjoiY2MiLCJtaW5lUGxhblRvbm5hZ2VzIjp7IjEiOlsyMDAwLjAsMjAwMC4wXSwiMiI6WzIwMDAuMCwyMDAwLjBdfSwiU3RvY2twaWxlMkluY3JlbWVudHMyMiI6MS4wLCJTdG9ja3BpbGUySW5jcmVtZW50czUwIjoxLjAsIlN0b2NrcGlsZTFQcmVtaXVtMjIiOjEuNSwiZGVwb1Byb3Zpc2lvblBheSI6WzQuMCw0LjBdLCJTdG9ja3BpbGUyTWluR3JhZGU1MCI6MTAuMCwiU3RvY2twaWxlMU1heEdyYWRlMjIiOjYyLjAsIm90aGVyTW9iRXF1aXAiOlsyNS45LDEuMV0sInN0b2NrcGlsZUxHIjpbMC4wLDAuMF0sInJhaWxjYXJzIjpbNDIuMCwwLjBdLCJ3b3JrQ2FwQ29zdHNMRyI6WzExLjYxLDE2Ljc1XSwicHJvamVjdFN0YXJ0TW9udGgiOjEsIlN0b2NrcGlsZTJNYXhHcmFkZTMiOjEuMCwidHJhbnNwb3J0YXRpb24iOlswLjAsMC4wXSwibG9hZE91dFJhaWxMb29wIjpbMi41MywyLjc0XSwiaW5mcmFJbmRpcmVjdENvc3QiOlsyOC42NiwwLjBdLCJtaW5lSUQiOiIxNCIsIlN0b2NrcGlsZTJNaW5HcmFkZTMzIjowLjAsInVzZXJJRCI6IjkiLCJTdG9ja3BpbGUxTWF4R3JhZGUzMyI6MC4wLCJTdG9ja3BpbGUxTWluTWF4UGVuYWx0eTUwIjowLjc1LCJTdG9ja3BpbGUxTWluUGVuYWx0eTIyIjozLjAsIm9wZXhQVCI6WzYuNzgsNi43OF0sIkVQQ00iOlswLjAsMC4wXSwib3duZXJDb3N0IjpbMC4wLDAuMF0sImZpcnN0bmFtZSI6ImNjIiwiU3RvY2twaWxlMk1heFBlbmFsdHk1MCI6MC43NSwibWluZUVxdWlwU3VzdGFpbiI6WzEwLjQ0LDQuNTJdLCJTdG9ja3BpbGUxUHJlbWl1bTMzIjowLjAsIlN0b2NrcGlsZTFQcmVtaXVtMyI6LTAuMiwiY29udGluZ2VuY3kiOlsxMy45MSwwLjBdLCJzaGlwcGluZyI6WzE1LjYzLDE1LjYzXSwiU3RvY2twaWxlMk1heEdyYWRlMjIiOjU4LjAsIm1pbmVFcXVpcEluaXRpYWwiOlsyMy4zMywwLjBdLCJTdG9ja3BpbGUyTWluTWF4UGVuYWx0eTMiOjAuMiwicmFpbFRyYW5zcG9ydCI6WzcxLjM5LDc5LjQ5XSwiU3RvY2twaWxlMU1pbk1heFBlbmFsdHkzMyI6MC4wLCJHQUNvcnAiOlsxLjkzLDIuNTddLCJtYWluQ29tbW9kaXRpZXMiOlsiMjIiXSwiU3RvY2twaWxlMk1pblBlbmFsdHk1MCI6MC43NSwiU3RvY2twaWxlMU1pblBlbmFsdHk1MCI6MC43NSwiU3RvY2twaWxlMk1heFBlbmFsdHkyMiI6MS41LCJTdG9ja3BpbGUyTWluUGVuYWx0eTMzIjowLjAsIlN0b2NrcGlsZTJNaW5QZW5hbHR5MyI6MC4yLCJwcm9qZWN0VHlwZSI6IjEiLCJtaW5lUGxhbkdyYWRlcyI6eyIxIjp7Ik1uIjpbMS4wNSwxLjA1XSwiRmUiOlsxLjA1LDEuMDVdLCJTaSI6WzEuMDUsMS4wNV0sIkFsIjpbMS4wNSwxLjA1XX0sIjIiOnsiTW4iOlsxLjA1LDEuMDVdLCJGZSI6WzEuMDUsMS4wNV0sIlNpIjpbMS4wNSwxLjA1XSwiQWwiOlsxLjA1LDEuMDVdfX0sIlN0b2NrcGlsZTJJbmNyZW1lbnRzMzMiOjEuMCwiU3RvY2twaWxlMk1heEdyYWRlNTAiOjEwLjAsInByb2Nlc3NpbmciOls1LjA4LDUuNjFdLCJTdG9ja3BpbGUyTWluUGVuYWx0eTIyIjo0LjB9','2017-11-19 20:19:37.437629'),('jmaxpg1zjjq45bex2mo2p6dojnn955yt','MWQ4ZWQ0NTQwNjQ2MWQ0NjFjMjE0MmE3ZTY1YmZmMmFiNWZmYjRmMTp7Im1pbmVJRCI6IjEiLCJfc2Vzc2lvbl9leHBpcnkiOjAsInVzZXJuYW1lIjoia3Jpc3RhZnVuZyIsImZpcnN0bmFtZSI6IktyaXN0YSIsInVzZXJJRCI6IjEifQ==','2017-06-29 17:23:30.313310'),('lwnwdwz6dtifedd72l9ozgzbbaebchpw','MWY3NTQ3ZTdjMTcyZGQ1YmFiYTExNDc2Nzg2ZWJjZGQ0OWVkMGM4MDp7Il9zZXNzaW9uX2V4cGlyeSI6MCwidXNlcklEIjoiMSIsImZpcnN0bmFtZSI6IktyaXN0YSIsInVzZXJuYW1lIjoia3Jpc3RhZnVuZyIsIm1pbmVJRCI6IjEifQ==','2017-09-07 06:13:56.592533'),('mg0cqvomt8skd7htgzfe5t3omth6s2xd','ZDg1NzE4NTA1OTE5ZGQzYmRhNGI0MGNkOTY1NjcxZWEwMDk0ZmE2YTp7InVzZXJuYW1lIjoiY2MiLCJfc2Vzc2lvbl9leHBpcnkiOjAsInVzZXJJRCI6IjkiLCJtaW5lSUQiOiIxNCIsImZpcnN0bmFtZSI6ImNjIn0=','2017-12-15 16:11:05.729752'),('nn7giustl3ijdkb3y5zgwe3p3mvgzaas','YjJkMmUyODlhOGRjNDBlNDUyMzg1MDZhZTIwOTk1YzFiZWI3NzhiMTp7InVzZXJuYW1lIjoiY2MiLCJfc2Vzc2lvbl9leHBpcnkiOjAsImZpcnN0bmFtZSI6ImNjIiwidXNlcklEIjoiOSIsIm1pbmVJRCI6IjE0In0=','2017-10-07 22:51:03.221987'),('nwchvk5xwcq6v2nh9w2mnsxafnk2l582','NjZhNWU2MTU4NGJiOTdhZWE0YTQyZDhiNDlkYmY3YjllNWQyMzI2OTp7ImZpcnN0bmFtZSI6IktyaXN0YSIsIm1pbmVJRCI6IjEiLCJfc2Vzc2lvbl9leHBpcnkiOjAsInVzZXJJRCI6IjEiLCJ1c2VybmFtZSI6ImtyaXN0YWZ1bmcifQ==','2017-07-16 18:11:44.220748'),('oecutp6exl4u1rzrahcawxn58j44tf0f','ZWI3MzYxYmM3NDM1ZDFmNmI5ZWVmNzQ0OGI1Yjc5NGZhMjI2YjY2Mjp7InVzZXJJRCI6IjEiLCJtaW5lSUQiOiIxIiwiX3Nlc3Npb25fZXhwaXJ5IjowLCJ1c2VybmFtZSI6ImtyaXN0YWZ1bmciLCJmaXJzdG5hbWUiOiJLcmlzdGEifQ==','2017-04-13 15:14:43.583925'),('oohqpd1wgvi9osk075tsbkfszik7k56p','NTM2M2IyZTk2YjYyOTkzMTMyM2M4OTQ4YmM3MmZjOTYwYjNiZTNlOTp7Il9zZXNzaW9uX2V4cGlyeSI6MCwibWluZUlEIjoiMSIsImZpcnN0bmFtZSI6IktyaXN0YSIsInVzZXJJRCI6IjEiLCJ1c2VybmFtZSI6ImtyaXN0YWZ1bmcifQ==','2017-03-26 23:54:14.615061'),('opw3xfduhiids0jn9v47emfw0l7n4i1h','NjRiMWVhNDc2MWIwYmU4OWZmY2YxODBjMTkxMDYwYjNlMGZjOWQ4NTp7Im1pbmVJRCI6IjEiLCJmaXJzdG5hbWUiOiJLcmlzdGEiLCJ1c2VybmFtZSI6ImtyaXN0YWZ1bmciLCJfc2Vzc2lvbl9leHBpcnkiOjAsInVzZXJJRCI6IjEifQ==','2017-06-27 19:16:36.868631'),('plta2ptcr6xyofnii668rvkgot1oiiuv','MDFkYzA0YmVkYzNkNjc2N2MyNDlmOTdhMWE4Y2RmNjU3NGUwMzE5MDp7Il9zZXNzaW9uX2V4cGlyeSI6MCwidXNlcklEIjoiMiIsInVzZXJuYW1lIjoiYWJjIiwiZmlyc3RuYW1lIjoiYWJjIiwibWluZUlEIjoiMiJ9','2017-05-24 19:42:01.469866'),('q9tcq9ehf0q8nkmmph2w7j9oxeibvn8o','ZGZhNDY1NzhkYWY1YjU1NWNlMmE4ZWZhODAxMDdiY2I2ZGU5OWFmZTp7Il9zZXNzaW9uX2V4cGlyeSI6MCwibWluZUlEIjoiMSIsIm1haW5Db21tb2RpdGllcyI6WyI0MiJdLCJ1c2VySUQiOiIxIiwidXNlcm5hbWUiOiJrcmlzdGFmdW5nIiwiZGVsQ29tbW9kaXRpZXMiOlsiMjEiXSwiZmlyc3RuYW1lIjoiS3Jpc3RhIn0=','2017-09-22 19:55:16.689295'),('qpkapvn0x1il5l068jvk28xdm6dkyola','ZTg1NDkxNjUwNjdmODliNzExZWRlNmViNzI1MjdhNDNmMzdiOTQ1MTp7Il9zZXNzaW9uX2V4cGlyeSI6MCwibWluZUlEIjoiMSIsInVzZXJuYW1lIjoia3Jpc3RhZnVuZyIsImZpcnN0bmFtZSI6IktyaXN0YSIsInVzZXJJRCI6IjEifQ==','2017-04-10 00:05:11.901923'),('r2akvuwqtpq45jz8nqynxwj21ubiy10d','Mjk5YTk1N2M1ZjMyM2FjYjc4ZGFkNThhMDM1MTgwNzcxNzdkMjc5ZTp7InVzZXJJRCI6IjEwIiwiX3Nlc3Npb25fZXhwaXJ5IjowLCJ1c2VybmFtZSI6IndlcyIsIm1pbmVJRCI6IjE1IiwiZmlyc3RuYW1lIjoid2VzIn0=','2018-01-13 21:07:07.474918'),('sbiaahkup37ulet6bkz63huux0ofxj22','ODI1NzBmNTFjNjJhODJkM2E5ZjEzYWU3ZDUyNjEwOWRlYjMxZmUwNjp7InVzZXJJRCI6IjEiLCJfc2Vzc2lvbl9leHBpcnkiOjAsInVzZXJuYW1lIjoia3Jpc3RhZnVuZyIsImZpcnN0bmFtZSI6IktyaXN0YSIsIm1pbmVJRCI6IjEifQ==','2017-09-04 19:03:37.980435'),('shm74weub633h0c07x6cqe4ldals8o9i','YjJkMmUyODlhOGRjNDBlNDUyMzg1MDZhZTIwOTk1YzFiZWI3NzhiMTp7InVzZXJuYW1lIjoiY2MiLCJfc2Vzc2lvbl9leHBpcnkiOjAsImZpcnN0bmFtZSI6ImNjIiwidXNlcklEIjoiOSIsIm1pbmVJRCI6IjE0In0=','2017-10-05 15:38:35.413274'),('stkif7lsxgfv9rhpzgfdm0vp03ul4yzs','ZjU5MmFkZWE4MTMyOTI5MjdkY2RjMDBiN2Y4ZGY3ZWJkOTc0MTQzMjp7Im1pbmVJRCI6IjEiLCJmaXJzdG5hbWUiOiJLcmlzdGEiLCJ1c2VySUQiOiIxIiwidXNlcm5hbWUiOiJrcmlzdGFmdW5nIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2017-06-19 17:18:21.954308'),('tefgct51m82t9xbufe1b83l3ljec2yip','Zjg4ZmYwNDgyM2U0MTFmYWYzMTc0NDcxZDkwN2NiMWQ2N2U2NzdmYTp7ImZpcnN0bmFtZSI6IktyaXN0YSIsInVzZXJJRCI6IjEiLCJfc2Vzc2lvbl9leHBpcnkiOjAsIm1pbmVJRCI6IjEiLCJ1c2VybmFtZSI6ImtyaXN0YWZ1bmcifQ==','2017-05-04 04:27:41.210125'),('x3wzqz05tptownarns5geaohqqf7i27u','Zjg3ZTA0ZjRkOTQ0ZjM0NjA3YmQwZDdmZDhhNzgyNTk2OTQ3MWRlOTp7Il9zZXNzaW9uX2V4cGlyeSI6MCwiZmlyc3RuYW1lIjoiS3Jpc3RhIiwidXNlcm5hbWUiOiJrcmlzdGFmdW5nIiwibWluZUlEIjoiMSIsInVzZXJJRCI6IjEifQ==','2017-07-06 00:09:59.087075'),('y0wuvx4zn2jxnagp9sydcrsu1kti1geq','ODUxYWZkYzc4YWJhZjUzZTFlMDQ3M2IzMTVlNGRkMTAzNTJhMWI1ZDp7InVzZXJJRCI6IjkiLCJfc2Vzc2lvbl9leHBpcnkiOjAsImZpcnN0bmFtZSI6ImNjIiwibWluZUlEIjoiMTQiLCJ1c2VybmFtZSI6ImNjIn0=','2018-02-05 18:23:52.999292'),('z2rb33vtfsanh0x3z4u97tnbn6278fpx','ZmExMDI2MTlhYWE1NzdmNzQ3NDBmM2RmOGY0YjNlYzY4Njc3NWU5Mzp7Im1pbmVJRCI6IjE0IiwiZmlyc3RuYW1lIjoiY2MiLCJ1c2VySUQiOiI5IiwiX3Nlc3Npb25fZXhwaXJ5IjowLCJ1c2VybmFtZSI6ImNjIn0=','2018-01-31 05:06:24.964899'),('zpkwdd3wfayivmhf4ekr29pen0h3xsmk','NWQzOGU2MGE3MmYxNDcxNTczYWRlM2IwYTE1MjM4MWRlOWQ2MWU0Mjp7ImZpcnN0bmFtZSI6IktyaXN0YSIsInVzZXJuYW1lIjoia3Jpc3RhZnVuZyIsInVzZXJJRCI6IjEiLCJfc2Vzc2lvbl9leHBpcnkiOjAsIm1pbmVJRCI6IjEifQ==','2017-03-21 15:24:03.501422'),('zvj7xmdk4t5st9g4q1zv51dm6s2lred2','MjIwMTM0NTQ4N2E0OTcxOWIyZDc1NWUwZGIzMTQ1MmZmODc4ZWVlNjp7ImZpcnN0bmFtZSI6IktyaXN0YSIsIm1pbmVJRCI6IjEiLCJ1c2VybmFtZSI6ImtyaXN0YWZ1bmciLCJfc2Vzc2lvbl9leHBpcnkiOjAsInVzZXJJRCI6IjEifQ==','2017-06-13 20:30:37.957751');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblCAPEX`
--

DROP TABLE IF EXISTS `tblCAPEX`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblCAPEX` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `year` int(11) NOT NULL,
  `preStrip` decimal(20,2) NOT NULL,
  `mineEquipInitial` decimal(20,2) NOT NULL,
  `mineEquipSustain` decimal(20,2) NOT NULL,
  `infraDirectCost` decimal(20,2) NOT NULL,
  `infraIndirectCost` decimal(20,2) NOT NULL,
  `contingency` decimal(20,2) NOT NULL,
  `railcars` decimal(20,2) NOT NULL,
  `otherMobEquip` decimal(20,2) NOT NULL,
  `closureRehabAssure` decimal(20,2) NOT NULL,
  `depoProvisionPay` decimal(20,2) NOT NULL,
  `workCapCurrentProd` decimal(20,2) NOT NULL,
  `workCapCostsLG` decimal(20,2) NOT NULL,
  `EPCM` decimal(20,2) NOT NULL,
  `ownerCost` decimal(20,2) NOT NULL,
  `dateAdded` datetime(6) NOT NULL,
  `mineID` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tblCAPEX_mineID_e9d741a3_fk_tblMine_mineID` (`mineID`),
  CONSTRAINT `tblCAPEX_mineID_e9d741a3_fk_tblMine_mineID` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblCAPEX`
--

LOCK TABLES `tblCAPEX` WRITE;
/*!40000 ALTER TABLE `tblCAPEX` DISABLE KEYS */;
INSERT INTO `tblCAPEX` VALUES (1,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 16:15:27.224582',1),(2,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 16:15:27.224582',1),(3,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:02:53.845432',1),(4,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:02:53.845432',1),(5,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-28 10:34:58.191984',1),(6,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-28 10:34:58.191984',1),(7,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-28 18:40:30.717969',1),(8,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-28 18:40:30.717969',1),(9,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-01 20:47:34.771306',1),(10,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-01 20:47:34.771306',1),(11,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-02 01:04:43.627072',1),(12,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-02 01:04:43.627072',1),(13,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-07 15:25:22.176933',1),(14,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-07 15:25:22.176933',1),(15,1,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,'2017-03-09 12:23:28.718527',1),(16,2,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,'2017-03-09 12:23:28.718527',1),(17,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-12 19:45:23.650485',1),(18,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-12 19:45:23.650485',1),(19,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-13 00:34:19.299934',1),(20,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-13 00:34:19.299934',1),(21,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-13 23:20:39.176767',1),(22,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-13 23:20:39.176767',1),(23,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-14 04:16:31.073968',1),(24,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-14 04:16:31.073968',1),(25,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-14 22:35:29.397483',1),(26,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-14 22:35:29.397483',1),(27,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-21 16:49:10.603993',1),(28,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-21 16:49:10.603993',1),(29,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-23 05:54:51.341845',1),(30,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-23 05:54:51.341845',1),(31,1,15.31,23.33,10.44,111.82,28.66,13.91,42.00,25.90,0.00,4.00,14.81,11.61,0.00,0.00,'2017-03-26 22:40:02.858192',1),(32,2,15.31,23.33,10.44,111.82,28.66,13.91,42.00,25.90,0.00,4.00,14.81,11.61,0.00,0.00,'2017-03-26 22:40:02.858192',1),(33,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-04-07 16:27:50.288181',1),(34,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-04-07 18:56:21.465181',1),(35,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-04-07 19:17:48.119162',1),(36,1,15.31,23.33,10.44,111.82,28.66,13.91,42.00,25.90,0.00,4.00,14.81,11.61,0.00,0.00,'2017-04-11 16:48:51.132766',1),(37,1,15.31,23.33,10.44,28.66,111.82,13.91,42.00,25.90,0.00,4.00,14.81,11.61,0.00,0.00,'2017-04-13 21:07:05.242448',1),(38,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-04-22 15:32:27.670415',1),(39,1,15.31,23.33,10.44,111.82,28.66,13.91,42.00,25.90,0.00,4.00,14.81,11.61,0.00,0.00,'2017-04-26 14:31:31.121581',1),(40,1,15.31,23.33,10.44,111.82,28.66,13.91,42.00,25.90,0.00,4.00,14.81,11.61,0.00,0.00,'2017-05-11 21:06:01.794829',2),(41,2,0.00,0.00,4.52,0.00,0.00,0.00,0.00,1.10,0.00,4.00,0.00,16.75,0.00,0.00,'2017-05-11 21:06:01.794829',2),(42,1,15.31,23.33,10.44,111.82,28.66,13.91,42.00,25.90,0.00,4.00,14.81,11.61,0.00,0.00,'2017-05-12 03:43:35.083025',2),(43,2,0.00,0.00,4.52,0.00,0.00,0.00,0.00,1.10,0.00,4.00,0.00,16.75,0.00,0.00,'2017-05-12 03:43:35.083025',2),(44,1,15.31,23.33,10.44,111.82,28.66,13.91,42.00,25.90,0.00,4.00,14.81,11.61,0.00,0.00,'2017-05-13 16:46:18.585105',2),(45,2,0.00,0.00,4.52,0.00,0.00,0.00,0.00,1.10,0.00,4.00,0.00,16.75,0.00,0.00,'2017-05-13 16:46:18.585105',2),(46,1,15.31,23.33,10.44,111.82,28.66,13.91,42.00,25.90,0.00,4.00,14.81,11.61,0.00,0.00,'2017-05-24 21:31:26.838648',1),(47,2,0.00,0.00,4.52,0.00,0.00,0.00,0.00,1.10,0.00,4.00,0.00,0.00,0.00,0.00,'2017-05-24 21:31:26.838648',1),(48,1,15.31,23.33,10.44,111.82,28.66,13.91,42.00,25.90,0.00,4.00,14.81,11.61,0.00,0.00,'2017-05-24 21:54:31.493517',1),(49,2,0.00,0.00,4.52,0.00,0.00,0.00,0.00,1.10,0.00,4.00,0.00,16.75,0.00,0.00,'2017-05-24 21:54:31.493517',1),(50,1,15.31,23.33,10.44,111.82,28.66,13.91,42.00,25.90,0.00,4.00,14.81,11.61,0.00,0.00,'2017-05-28 21:21:50.448314',1),(51,2,0.00,0.00,4.52,0.00,0.00,0.00,0.00,1.10,0.00,4.00,0.00,16.75,0.00,0.00,'2017-05-28 21:21:50.448314',1),(52,1,15.31,23.33,10.44,111.82,28.66,13.91,42.00,25.90,0.00,4.00,14.81,11.61,0.00,0.00,'2017-05-30 21:38:46.711359',1),(53,2,0.00,0.00,4.52,0.00,0.00,0.00,0.00,1.10,0.00,4.00,0.00,16.75,0.00,0.00,'2017-05-30 21:38:46.711359',1),(54,1,15.31,23.33,10.44,111.82,28.66,13.91,42.00,25.90,0.00,4.00,14.81,11.61,0.00,0.00,'2017-06-06 07:17:46.660762',1),(55,2,0.00,0.00,4.52,0.00,0.00,0.00,0.00,1.10,0.00,4.00,0.00,16.75,0.00,0.00,'2017-06-06 07:17:46.660762',1),(56,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-07-14 17:19:38.379963',13),(57,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-07-14 17:19:38.379963',13),(58,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-07-18 01:32:08.899910',14),(59,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-07-18 01:32:08.899910',14),(60,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-07-18 19:39:21.342509',14),(61,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-07-18 19:39:21.342509',14),(62,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-11-27 05:58:34.236125',14),(63,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-11-27 05:58:34.236125',14),(64,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-11-27 06:12:20.970621',14),(65,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-11-27 06:12:20.970621',14),(66,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-12-01 16:11:03.772298',14),(67,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-12-01 16:11:03.772298',14),(68,1,15.31,23.33,10.44,111.82,28.66,13.91,42.00,25.90,0.00,4.00,14.81,11.61,0.00,0.00,'2017-12-13 14:32:01.423069',15),(69,2,0.00,0.00,4.52,0.00,0.00,0.00,0.00,1.10,0.00,4.00,0.00,16.75,0.00,0.00,'2017-12-13 14:32:01.423069',15),(70,1,15.31,23.33,10.44,111.82,28.66,13.91,42.00,25.90,0.00,4.00,14.81,11.61,0.00,0.00,'2018-01-17 05:06:22.706920',14),(71,2,0.00,0.00,4.52,0.00,0.00,0.00,0.00,1.10,0.00,4.00,0.00,16.75,0.00,0.00,'2018-01-17 05:06:22.706920',14);
/*!40000 ALTER TABLE `tblCAPEX` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblCashFlow`
--

DROP TABLE IF EXISTS `tblCashFlow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblCashFlow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mineID` int(11) NOT NULL,
  `cashFlowPreTax` float(20,2) DEFAULT NULL,
  `cashFlowPostTax` float(20,2) DEFAULT NULL,
  `cumulativeCashFlowPreTax` float(20,2) DEFAULT NULL,
  `cumulativeCashFlowPostTax` float(20,2) DEFAULT NULL,
  `paybackPreTax` float(20,2) DEFAULT NULL,
  `paybackPostTax` float(20,2) DEFAULT NULL,
  `dateAdded` datetime NOT NULL,
  `projectID` int(11) NOT NULL,
  `date` date NOT NULL,
  `processed` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_tblCashFlow_mineID` (`mineID`),
  KEY `tblcashflow_ibfk_2` (`projectID`),
  CONSTRAINT `tblcashflow_ibfk_1` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`) ON UPDATE CASCADE,
  CONSTRAINT `tblcashflow_ibfk_2` FOREIGN KEY (`projectID`) REFERENCES `tblProject` (`projectID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblCashFlow`
--

LOCK TABLES `tblCashFlow` WRITE;
/*!40000 ALTER TABLE `tblCashFlow` DISABLE KEYS */;
INSERT INTO `tblCashFlow` VALUES (1,1,1326077.50,1326077.50,1326077.50,1326077.50,NULL,NULL,'2017-06-03 18:23:19',100,'2017-05-01',1),(2,1,1768347.50,1768347.50,3094425.00,3094425.00,NULL,NULL,'2017-06-03 18:23:53',100,'2018-05-01',1),(3,1,183778.16,183778.16,3278203.00,3278203.00,NULL,NULL,'2017-06-03 18:24:27',100,'2018-06-01',1),(4,1,-183734.30,-183734.30,-183734.30,-183734.30,NULL,NULL,'2017-06-14 02:54:24',101,'2017-05-01',1),(5,1,117595.39,117595.39,-66138.90,-66138.90,NULL,NULL,'2017-06-07 17:58:14',101,'2018-05-01',1),(6,14,-35240.96,-38390.96,-35240.96,-38390.96,NULL,NULL,'2017-08-21 18:52:31',107,'2017-05-01',1),(7,15,NULL,NULL,NULL,NULL,NULL,NULL,'2017-12-13 19:47:01',112,'2018-01-15',0),(8,15,NULL,NULL,NULL,NULL,NULL,NULL,'2018-01-09 17:58:43',112,'2018-01-01',0),(9,14,-129274.36,-129274.36,-129274.36,-129274.36,NULL,NULL,'2018-01-22 05:05:52',113,'2018-01-01',1),(10,14,-68655.86,-68655.86,-197930.22,-197930.22,NULL,NULL,'2018-01-22 06:30:32',113,'2018-01-02',1);
/*!40000 ALTER TABLE `tblCashFlow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblCommodity`
--

DROP TABLE IF EXISTS `tblCommodity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblCommodity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dateAdded` datetime(6) NOT NULL,
  `commodityID` int(11) NOT NULL,
  `mineID` int(11) NOT NULL,
  `projectID` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tblCommodit_commodityID_18f1c7d1_fk_tblCommodityList_commodityID` (`commodityID`),
  KEY `tblCommodity_mineID_51e2866b_fk_tblMine_mineID` (`mineID`),
  KEY `tblcommodity_ibfk_1` (`projectID`),
  CONSTRAINT `tblCommodit_commodityID_18f1c7d1_fk_tblCommodityList_commodityID` FOREIGN KEY (`commodityID`) REFERENCES `tblCommodityList` (`commodityID`),
  CONSTRAINT `tblCommodity_mineID_51e2866b_fk_tblMine_mineID` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`),
  CONSTRAINT `tblcommodity_ibfk_1` FOREIGN KEY (`projectID`) REFERENCES `tblProject` (`projectID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=316 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblCommodity`
--

LOCK TABLES `tblCommodity` WRITE;
/*!40000 ALTER TABLE `tblCommodity` DISABLE KEYS */;
INSERT INTO `tblCommodity` VALUES (240,'2017-05-13 06:20:44.776491',22,2,95),(241,'2017-05-13 06:20:44.776491',3,2,95),(242,'2017-05-13 06:20:44.776491',33,2,95),(243,'2017-05-13 06:20:44.776491',50,2,95),(260,'2017-06-06 07:14:08.504146',22,1,101),(261,'2017-06-06 07:14:08.504146',3,1,101),(262,'2017-06-06 07:14:08.504146',33,1,101),(263,'2017-06-06 07:14:08.504146',50,1,101),(268,'2017-07-14 17:19:38.379963',22,13,102),(269,'2017-07-14 17:19:38.379963',3,13,102),(270,'2017-07-14 17:19:38.379963',33,13,102),(271,'2017-07-14 17:19:38.379963',50,13,102),(272,'2017-07-18 01:32:08.899910',22,14,103),(273,'2017-07-18 01:32:08.899910',3,14,103),(274,'2017-07-18 01:32:08.899910',33,14,103),(275,'2017-07-18 01:32:08.899910',50,14,103),(276,'2017-07-18 19:28:45.383178',22,14,104),(277,'2017-07-18 19:28:45.383178',3,14,104),(278,'2017-07-18 19:28:45.383178',33,14,104),(279,'2017-07-18 19:28:45.383178',50,14,104),(280,'2017-07-18 19:32:43.988200',22,14,105),(281,'2017-07-18 19:32:43.988200',3,14,105),(282,'2017-07-18 19:32:43.988200',33,14,105),(283,'2017-07-18 19:32:43.988200',50,14,105),(284,'2017-07-18 19:35:06.775799',22,14,106),(285,'2017-07-18 19:35:06.775799',3,14,106),(286,'2017-07-18 19:35:06.775799',33,14,106),(287,'2017-07-18 19:35:06.775799',50,14,106),(288,'2017-07-18 19:39:21.342509',22,14,107),(289,'2017-07-18 19:39:21.342509',3,14,107),(290,'2017-07-18 19:39:21.342509',33,14,107),(291,'2017-07-18 19:39:21.342509',50,14,107),(292,'2017-11-27 05:51:12.717978',22,14,108),(293,'2017-11-27 05:51:12.717978',3,14,108),(294,'2017-11-27 05:51:12.717978',33,14,108),(295,'2017-11-27 05:51:12.717978',50,14,108),(296,'2017-11-27 05:58:34.236125',22,14,109),(297,'2017-11-27 05:58:34.236125',3,14,109),(298,'2017-11-27 05:58:34.236125',33,14,109),(299,'2017-11-27 05:58:34.236125',50,14,109),(300,'2017-11-27 06:12:20.970621',22,14,110),(301,'2017-11-27 06:12:20.970621',3,14,110),(302,'2017-11-27 06:12:20.970621',33,14,110),(303,'2017-11-27 06:12:20.970621',50,14,110),(304,'2017-12-01 16:11:03.772298',22,14,111),(305,'2017-12-01 16:11:03.772298',3,14,111),(306,'2017-12-01 16:11:03.772298',33,14,111),(307,'2017-12-01 16:11:03.772298',50,14,111),(308,'2017-12-13 14:32:01.423069',22,15,112),(309,'2017-12-13 14:32:01.423069',3,15,112),(310,'2017-12-13 14:32:01.423069',33,15,112),(311,'2017-12-13 14:32:01.423069',50,15,112),(312,'2018-01-17 05:06:22.706920',22,14,113),(313,'2018-01-17 05:06:22.706920',3,14,113),(314,'2018-01-17 05:06:22.706920',33,14,113),(315,'2018-01-17 05:06:22.706920',50,14,113);
/*!40000 ALTER TABLE `tblCommodity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblCommodityList`
--

DROP TABLE IF EXISTS `tblCommodityList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblCommodityList` (
  `commodityID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(5) NOT NULL,
  `commodityType` int(11) NOT NULL,
  PRIMARY KEY (`commodityID`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblCommodityList`
--

LOCK TABLES `tblCommodityList` WRITE;
/*!40000 ALTER TABLE `tblCommodityList` DISABLE KEYS */;
INSERT INTO `tblCommodityList` VALUES (1,'Ag',1),(2,'Al',1),(3,'Al',2),(4,'As',2),(5,'Au',1),(6,'Be',1),(7,'Bi',1),(8,'Bi',2),(9,'Br',2),(10,'C',1),(11,'C',2),(12,'Ca',2),(13,'Cd',1),(14,'Cd',2),(15,'Cl',2),(16,'Co',1),(17,'Co',2),(18,'Cr',1),(19,'Cr',2),(20,'Cu',1),(21,'Cu',2),(22,'Fe',1),(23,'Fe',2),(24,'Fl',2),(25,'Hg',2),(26,'In',1),(27,'K',1),(28,'K',2),(29,'Li',1),(30,'Mg',1),(31,'Mg',2),(32,'Mn',1),(33,'Mn',2),(34,'Mo',1),(35,'Na',2),(36,'Ni',1),(37,'Ni',2),(38,'P',2),(39,'Pb',1),(40,'Pb',2),(41,'Pd',1),(42,'Pt',1),(43,'REO',1),(44,'S',1),(45,'S',2),(46,'Sb',2),(47,'Se',1),(48,'Se',2),(49,'Si',1),(50,'Si',2),(51,'Sn',1),(52,'Sn',2),(53,'Te',1),(54,'Ti',1),(55,'U',1),(56,'U',2),(57,'V',1),(58,'V',2),(59,'W',1),(60,'W',2),(61,'Zn',1),(62,'Zn',2);
/*!40000 ALTER TABLE `tblCommodityList` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblCompany`
--

DROP TABLE IF EXISTS `tblCompany`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblCompany` (
  `companyID` int(11) NOT NULL AUTO_INCREMENT,
  `company` varchar(250) NOT NULL,
  `address` varchar(250) NOT NULL,
  `city` varchar(100) NOT NULL,
  `province` varchar(50) NOT NULL,
  `country` varchar(50) NOT NULL,
  `postalCode` varchar(10) NOT NULL,
  `phone` varchar(32) NOT NULL,
  `dateAdded` datetime(6) NOT NULL,
  PRIMARY KEY (`companyID`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblCompany`
--

LOCK TABLES `tblCompany` WRITE;
/*!40000 ALTER TABLE `tblCompany` DISABLE KEYS */;
INSERT INTO `tblCompany` VALUES (1,'test','test','Toronto','ON','Canada','M2N 6H8','6478866585','2017-02-26 15:08:09.216328'),(2,'test','test','Toronto','ON','Canada','M2N 6H8','6478866585','2017-02-26 15:14:00.339748'),(3,'test','test','Toronto','ON','Canada','M2N 6H8','6478866585','2017-02-26 15:16:17.265104'),(4,'test','test','Toronto','ON','Canada','M2N 6H8','6478866585','2017-02-26 15:22:18.678744'),(5,'test','test','Toronto','ON','Canada','M2N 6H8','6478866585','2017-02-26 15:23:55.153586'),(6,'test','test','Toronto','ON','Canada','M2N 6H8','6478866585','2017-02-26 15:33:30.259013'),(7,'test','test','Toronto','ON','Canada','M2N 6H8','6478866585','2017-02-26 15:38:13.901199'),(8,'test','test','Toronto','ON','Canada','M2N 6H8','6478866585','2017-02-26 15:41:47.452284'),(9,'test','test','Toronto','ON','Canada','M2N 6H8','6478866585','2017-02-26 15:50:19.602923'),(10,'test','test','Toronto','ON','Canada','M2N 6H8','6478866585','2017-02-26 15:50:51.415043'),(11,'abc','abc','abc','abc','abc','abc','abc','2017-04-07 22:30:23.457103'),(12,'abc','abc','abc','abc','abc','abc','abc','2017-04-08 17:57:27.437933'),(13,'abc','abc','abc','abc','abc','abc','abc','2017-04-08 18:18:07.578011'),(14,'abc','abc','abc','abc','abc','abc','abc','2017-04-08 19:01:41.374895'),(15,'la','la','la','la','la','la','la','2017-04-13 15:58:35.294077'),(16,'bb','bb','bb','bb','bb','bb','bb','2017-04-13 15:59:59.187952'),(17,'111','111','111','111','111','111','111','2017-04-20 15:15:01.761200'),(18,'q11','11','11','11','11','11','11','2017-04-20 15:32:02.431863'),(19,'11','11','11','11','11','11','11','2017-04-20 15:32:32.424478'),(20,'123','123','123','123','123','123','123','2017-04-20 15:34:10.302867'),(21,'12','12','12','12','12','12','123','2017-04-20 15:42:40.952210'),(22,'a1','a1','a1','a1','a1','a1','a1','2017-07-07 16:34:49.676760'),(23,'b1','b1','b1','b1','b1','b1','b1','2017-07-07 18:09:22.724331'),(24,'cc','cc','cc','cc','cc','cc','cc','2017-07-15 18:55:36.182156'),(25,'wes','wes','wes','wes','wes','wes','wes','2017-08-22 19:24:09.221020');
/*!40000 ALTER TABLE `tblCompany` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblFinancials`
--

DROP TABLE IF EXISTS `tblFinancials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblFinancials` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mineID` int(11) NOT NULL,
  `discountRate` int(11) DEFAULT NULL,
  `NPVPreTax` float(20,2) DEFAULT NULL,
  `NPVPostTax` float(20,2) DEFAULT NULL,
  `IRRPreTax` float(20,2) DEFAULT NULL,
  `IRRPostTax` float(20,2) DEFAULT NULL,
  `dateAdded` datetime NOT NULL,
  `date` date NOT NULL,
  `projectID` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_tblFinancials_mineID` (`mineID`),
  KEY `tblfinancials_ibfk_2` (`projectID`),
  CONSTRAINT `tblfinancials_ibfk_1` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`) ON UPDATE CASCADE,
  CONSTRAINT `tblfinancials_ibfk_2` FOREIGN KEY (`projectID`) REFERENCES `tblProject` (`projectID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblFinancials`
--

LOCK TABLES `tblFinancials` WRITE;
/*!40000 ALTER TABLE `tblFinancials` DISABLE KEYS */;
INSERT INTO `tblFinancials` VALUES (19,1,0,1251016.50,1251016.50,NULL,NULL,'2017-06-05 17:20:03','2017-05-01',100),(20,1,0,1227849.50,1227849.50,NULL,NULL,'2017-06-05 17:20:03','2017-05-01',100),(21,1,0,1205525.00,1205525.00,NULL,NULL,'2017-06-05 17:20:03','2017-05-01',100),(22,1,0,1183997.75,1183997.75,NULL,NULL,'2017-06-05 17:20:03','2017-05-01',100),(23,1,0,1153110.88,1153110.88,NULL,NULL,'2017-06-05 17:20:03','2017-05-01',100),(24,1,0,1105064.50,1105064.50,NULL,NULL,'2017-06-05 17:20:03','2017-05-01',100),(25,1,0,1573822.88,1573822.88,NULL,NULL,'2017-06-05 17:20:03','2018-05-01',100),(26,1,0,1516072.88,1516072.88,NULL,NULL,'2017-06-05 17:20:03','2018-05-01',100),(27,1,0,1461444.12,1461444.12,NULL,NULL,'2017-06-05 17:20:03','2018-05-01',100),(28,1,0,1409715.75,1409715.75,NULL,NULL,'2017-06-05 17:20:03','2018-05-01',100),(29,1,0,1337124.75,1337124.75,NULL,NULL,'2017-06-05 17:20:03','2018-05-01',100),(30,1,0,1228019.00,1228019.00,NULL,NULL,'2017-06-05 17:20:03','2018-05-01',100),(31,1,0,163561.91,163561.91,NULL,NULL,'2017-06-05 17:20:04','2018-06-01',100),(32,1,0,157560.14,157560.14,NULL,NULL,'2017-06-05 17:20:04','2018-06-01',100),(33,1,0,151882.77,151882.77,NULL,NULL,'2017-06-05 17:20:04','2018-06-01',100),(34,1,0,146506.81,146506.81,NULL,NULL,'2017-06-05 17:20:04','2018-06-01',100),(35,1,0,138962.69,138962.69,NULL,NULL,'2017-06-05 17:20:04','2018-06-01',100),(36,1,0,127623.72,127623.72,NULL,NULL,'2017-06-05 17:20:04','2018-06-01',100),(61,1,6,-173334.23,-173334.23,NULL,NULL,'2017-06-14 16:27:45','2017-05-01',101),(62,1,8,-170124.34,-170124.34,NULL,NULL,'2017-06-14 16:27:45','2017-05-01',101),(63,1,10,-167031.17,-167031.17,NULL,NULL,'2017-06-14 16:27:45','2017-05-01',101),(64,1,12,-164048.47,-164048.47,NULL,NULL,'2017-06-14 16:27:45','2017-05-01',101),(65,1,15,-159768.95,-159768.95,NULL,NULL,'2017-06-14 16:27:45','2017-05-01',101),(66,1,20,-153111.91,-153111.91,NULL,NULL,'2017-06-14 16:27:45','2017-05-01',101),(67,1,6,104659.48,104659.48,NULL,NULL,'2017-06-14 16:27:45','2018-05-01',101),(68,1,8,100819.09,100819.09,NULL,NULL,'2017-06-14 16:27:45','2018-05-01',101),(69,1,10,97186.27,97186.27,NULL,NULL,'2017-06-14 16:27:45','2018-05-01',101),(70,1,12,93746.32,93746.32,NULL,NULL,'2017-06-14 16:27:45','2018-05-01',101),(71,1,15,88919.01,88919.01,NULL,NULL,'2017-06-14 16:27:45','2018-05-01',101),(72,1,20,81663.47,81663.47,NULL,NULL,'2017-06-14 16:27:45','2018-05-01',101),(73,14,6,-33246.19,-36217.89,NULL,NULL,'2017-08-21 18:52:37','2017-05-01',107),(74,14,8,-32630.52,-35547.19,NULL,NULL,'2017-08-21 18:52:37','2017-05-01',107),(75,14,10,-32037.24,-34900.87,NULL,NULL,'2017-08-21 18:52:37','2017-05-01',107),(76,14,12,-31465.14,-34277.64,NULL,NULL,'2017-08-21 18:52:37','2017-05-01',107),(77,14,15,-30644.31,-33383.44,NULL,NULL,'2017-08-21 18:52:37','2017-05-01',107),(78,14,20,-29367.47,-31992.47,NULL,NULL,'2017-08-21 18:52:37','2017-05-01',107),(79,14,6,-121956.94,-121956.94,NULL,NULL,'2018-01-22 05:51:09','2018-01-01',113),(80,14,8,-119698.48,-119698.48,NULL,NULL,'2018-01-22 05:51:09','2018-01-01',113),(81,14,10,-117522.15,-117522.15,NULL,NULL,'2018-01-22 05:51:09','2018-01-01',113),(82,14,12,-115423.54,-115423.54,NULL,NULL,'2018-01-22 05:51:09','2018-01-01',113),(83,14,15,-112412.49,-112412.49,NULL,NULL,'2018-01-22 05:51:09','2018-01-01',113),(84,14,20,-107728.63,-107728.63,NULL,NULL,'2018-01-22 05:51:09','2018-01-01',113),(85,14,5,-64769.68,-64769.68,NULL,NULL,'2018-01-22 06:30:37','2018-01-02',113),(86,14,8,-63570.24,-63570.24,NULL,NULL,'2018-01-22 06:30:37','2018-01-02',113),(87,14,10,-62414.42,-62414.42,NULL,NULL,'2018-01-22 06:30:37','2018-01-02',113),(88,14,11,-61299.88,-61299.88,NULL,NULL,'2018-01-22 06:30:37','2018-01-02',113),(89,14,14,-59700.75,-59700.75,NULL,NULL,'2018-01-22 06:30:37','2018-01-02',113),(90,14,20,-57213.22,-57213.22,NULL,NULL,'2018-01-22 06:30:37','2018-01-02',113);
/*!40000 ALTER TABLE `tblFinancials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblInputs`
--

DROP TABLE IF EXISTS `tblInputs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblInputs` (
  `inputID` int(11) NOT NULL AUTO_INCREMENT,
  `mineID` int(11) NOT NULL,
  `Fe2O3Iron` float(12,6) DEFAULT NULL,
  `totalGrade` float(12,6) DEFAULT NULL,
  `avgCommodity1Grade` float(12,6) DEFAULT NULL,
  `lumpRecovery` float(12,6) DEFAULT NULL,
  `finesRecovery` float(12,6) DEFAULT NULL,
  `lumpGrade` float(12,6) DEFAULT NULL,
  `finesGrade` float(12,6) DEFAULT NULL,
  `feedMoisture` float(12,6) DEFAULT NULL,
  `lumpMoisture` float(12,6) DEFAULT NULL,
  `finesMoisture` float(12,6) DEFAULT NULL,
  `ultraFinesMoisture` float(12,6) DEFAULT NULL,
  `rejectsMoisture` float(12,6) DEFAULT NULL,
  `mineOpsDays` int(11) DEFAULT NULL,
  `plantOpsDays` int(11) DEFAULT NULL,
  `mineCapacity` float(12,6) DEFAULT NULL,
  `plantCapacity` float(12,6) DEFAULT NULL,
  `discountRate1` float(12,4) DEFAULT NULL,
  `discountRate2` float(12,4) DEFAULT NULL,
  `discountRate3` float(12,4) DEFAULT NULL,
  `discountRate4` float(12,4) DEFAULT NULL,
  `discountRate5` float(12,4) DEFAULT NULL,
  `discountRate6` float(12,4) DEFAULT NULL,
  `dateAdded` datetime NOT NULL,
  `exchangeRate` float(12,4) DEFAULT NULL,
  `ultraFinesRecovery` float(12,6) DEFAULT NULL,
  `rejectsRecovery` float(12,6) DEFAULT NULL,
  `ultraFinesGrade` float(12,6) DEFAULT NULL,
  `rejectsGrade` float(12,6) DEFAULT NULL,
  PRIMARY KEY (`inputID`),
  KEY `fk_tblInputs_mineID` (`mineID`),
  CONSTRAINT `tblinputs_ibfk_1` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblInputs`
--

LOCK TABLES `tblInputs` WRITE;
/*!40000 ALTER TABLE `tblInputs` DISABLE KEYS */;
INSERT INTO `tblInputs` VALUES (1,1,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.051000,1.050000,1.050000,1.050000,1.050000,30,30,150.440002,150.440002,1.0500,1.0500,1.0500,1.0500,1.0500,1.0500,'2017-02-27 18:45:00',NULL,NULL,NULL,NULL,NULL),(2,1,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,180,180,1.050000,1.050000,1.0500,1.0500,1.0500,1.0500,1.0500,1.0500,'2017-03-02 05:48:28',NULL,NULL,NULL,NULL,NULL),(3,1,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,200,200,1.050000,1.050000,1.0500,1.0500,1.0500,1.0500,1.0500,1.0500,'2017-03-07 15:33:43',NULL,NULL,NULL,NULL,NULL),(4,1,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,200,200,1.050000,1.050000,1.0500,1.0500,1.0500,1.0500,1.0500,1.0500,'2017-03-12 19:46:37',NULL,NULL,NULL,NULL,NULL),(5,1,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,200,200,1.050000,1.050000,1.0500,1.0500,1.0500,1.0500,1.0500,1.0500,'2017-03-13 00:35:29',NULL,NULL,NULL,NULL,NULL),(6,1,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,200,200,1.050000,1.050000,1.0500,1.0500,1.0500,1.0500,1.0500,1.0500,'2017-03-13 23:21:49',1.0500,NULL,NULL,NULL,NULL),(7,1,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,200,200,1.050000,1.050000,1.0500,1.0500,1.0500,1.0500,1.0500,1.0500,'2017-03-14 22:37:12',1.0500,NULL,NULL,NULL,NULL),(8,1,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,300,300,1.050000,1.050000,1.0500,1.0500,1.0500,1.0500,1.0500,1.0500,'2017-03-22 23:57:52',1.0500,NULL,NULL,NULL,NULL),(9,1,1.050000,1.050000,60.000000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,300,300,25000.000000,25000.000000,1.0500,1.0500,1.0500,1.0500,1.0500,1.0500,'2017-03-23 05:58:01',1.0500,NULL,NULL,NULL,NULL),(10,1,69.900002,97.000000,62.000000,35.000000,65.000000,64.000000,61.000000,6.000000,4.000000,7.000000,0.000000,0.000000,365,240,17119.300781,0.000000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,'2017-03-26 22:53:09',0.8000,NULL,NULL,NULL,NULL),(11,1,1.050000,85.000000,55.000000,35.000000,35.000000,35.000000,35.000000,35.000000,35.000000,35.000000,35.000000,35.000000,200,200,30000.000000,25000.000000,1.0500,1.0500,1.0500,1.0500,1.0500,1.0500,'2017-04-07 19:31:52',1.0500,3.000000,35.000000,35.000000,35.000000),(12,1,69.900002,97.000000,0.620000,0.350000,0.650000,0.640000,0.610000,0.060000,0.040000,0.070000,NULL,NULL,365,240,17119.300781,15000.000000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,'2017-04-11 16:58:00',0.8000,NULL,NULL,NULL,NULL),(13,1,69.900002,97.000000,62.000000,35.000000,65.000000,64.000000,61.000000,6.000000,4.000000,7.000000,NULL,NULL,365,240,17119.300781,15000.000000,5.0000,0.0000,0.0000,0.0000,0.0000,0.0000,'2017-04-13 21:20:58',0.8000,NULL,NULL,NULL,NULL),(14,1,1.050000,33.000000,33.000000,33.000000,33.000000,33.000000,33.000000,33.000000,33.000000,33.000000,NULL,NULL,365,240,18000.000000,15000.000000,5.0000,0.0000,0.0000,0.0000,0.0000,0.0000,'2017-04-22 17:11:47',0.8000,NULL,NULL,NULL,NULL),(15,1,69.900002,97.000000,62.000000,35.000000,65.000000,64.000000,61.000000,6.000000,4.000000,7.000000,NULL,NULL,365,240,17119.300781,17119.300781,6.0000,8.0000,10.0000,12.0000,15.0000,20.0000,'2017-04-26 15:05:19',0.8000,NULL,NULL,NULL,NULL),(16,2,69.900002,97.000000,62.000000,35.000000,65.000000,64.000000,61.000000,6.000000,4.000000,7.000000,NULL,NULL,365,240,17119.300781,17119.300781,6.0000,8.0000,10.0000,12.0000,15.0000,20.0000,'2017-05-12 04:54:27',0.8000,NULL,NULL,NULL,NULL),(17,2,69.900002,97.000000,62.000000,35.000000,65.000000,64.000000,61.000000,6.000000,4.000000,7.000000,NULL,NULL,365,240,17119.300781,17119.300781,6.0000,8.0000,10.0000,12.0000,15.0000,20.0000,'2017-05-13 17:27:58',0.8000,NULL,NULL,NULL,NULL),(18,1,69.900002,97.000000,62.000000,35.000000,65.000000,64.000000,61.000000,6.000000,4.000000,7.000000,NULL,NULL,365,240,17119.300781,17119.300781,6.0000,8.0000,10.0000,12.0000,15.0000,20.0000,'2017-05-24 21:37:00',0.8000,NULL,NULL,NULL,NULL),(19,1,69.900002,97.000000,62.000000,35.000000,65.000000,64.000000,61.000000,6.000000,4.000000,7.000000,NULL,NULL,365,240,17119.300781,17119.300781,6.0000,8.0000,10.0000,12.0000,15.0000,18.0000,'2017-05-24 21:59:30',0.8000,NULL,NULL,NULL,NULL),(20,1,69.900002,97.000000,62.000000,35.000000,65.000000,64.000000,61.000000,6.000000,4.000000,7.000000,NULL,NULL,365,240,17119.300781,17119.300781,6.0000,8.0000,10.0000,12.0000,15.0000,20.0000,'2017-05-28 21:37:52',0.8000,NULL,NULL,NULL,NULL),(21,1,69.900002,97.000000,62.000000,35.000000,65.000000,64.000000,61.000000,6.000000,4.000000,7.000000,NULL,NULL,365,240,17119.300781,17119.300781,6.0000,8.0000,10.0000,12.0000,15.0000,20.0000,'2017-05-30 22:44:14',0.8000,NULL,NULL,NULL,NULL),(22,1,69.900002,97.000000,62.000000,35.000000,65.000000,64.000000,61.000000,6.000000,4.000000,7.000000,NULL,NULL,365,240,17199.300781,17199.300781,6.0000,8.0000,10.0000,12.0000,15.0000,20.0000,'2017-06-06 07:46:34',0.8000,NULL,NULL,NULL,NULL),(23,13,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,NULL,NULL,365,240,1.050000,1.050000,6.0000,8.0000,10.0000,12.0000,15.0000,20.0000,'2017-07-14 17:19:38',0.8000,NULL,NULL,NULL,NULL),(24,14,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,NULL,NULL,365,240,1.050000,1.050000,6.0000,8.0000,10.0000,12.0000,15.0000,20.0000,'2017-07-18 01:32:09',0.8000,NULL,NULL,NULL,NULL),(25,14,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,NULL,NULL,365,240,1.050000,1.050000,6.0000,8.0000,10.0000,12.0000,15.0000,20.0000,'2017-07-18 19:39:21',0.8000,NULL,NULL,NULL,NULL),(26,14,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,NULL,NULL,365,240,1.050000,1.050000,6.0000,8.0000,10.0000,12.0000,15.0000,20.0000,'2017-11-27 06:12:21',0.8000,NULL,NULL,NULL,NULL),(27,14,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,1.050000,NULL,NULL,365,240,1.050000,1.050000,6.0000,8.0000,10.0000,12.0000,15.0000,20.0000,'2017-12-01 16:11:04',0.8000,NULL,NULL,NULL,NULL),(28,15,69.900002,97.000000,62.000000,35.000000,65.000000,64.000000,61.000000,6.000000,4.000000,7.000000,NULL,NULL,365,240,17119.300781,17119.300781,6.0000,8.0000,10.0000,12.0000,15.0000,20.0000,'2017-12-13 14:32:01',0.8000,NULL,NULL,NULL,NULL),(29,14,69.900002,97.000000,62.000000,35.000000,65.000000,64.000000,61.000000,6.000000,4.000000,7.000000,NULL,NULL,365,240,17119.300781,17119.300781,6.0000,8.0000,10.0000,12.0000,15.0000,20.0000,'2018-01-17 05:06:23',0.8000,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `tblInputs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblMine`
--

DROP TABLE IF EXISTS `tblMine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblMine` (
  `mineID` int(11) NOT NULL AUTO_INCREMENT,
  `mine` varchar(100) NOT NULL,
  `address` varchar(250) NOT NULL,
  `city` varchar(100) NOT NULL,
  `province` varchar(50) NOT NULL,
  `country` varchar(50) NOT NULL,
  `postalCode` varchar(10) NOT NULL,
  `phone` varchar(32) NOT NULL,
  `dateAdded` datetime(6) NOT NULL,
  `fax` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`mineID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblMine`
--

LOCK TABLES `tblMine` WRITE;
/*!40000 ALTER TABLE `tblMine` DISABLE KEYS */;
INSERT INTO `tblMine` VALUES (1,'abc','abc','abc','abc','abc','abc','abc','2017-02-26 15:57:08.579185',NULL),(2,'abc','abc','abc','abc','abc','abc','abc','2017-04-07 22:30:32.026910',NULL),(3,'abc','abc','abc','abc','abc','abc','abc','2017-04-08 17:57:43.047861',NULL),(4,'abc','abc','abc','abc','abc','abc','abc','2017-04-08 18:18:16.935713',NULL),(5,'abc','abc','abc','abc','abc','abc','abc','2017-04-08 19:01:58.772211',NULL),(6,'la','la','la','la','la','la','la','2017-04-13 15:58:49.775598',NULL),(7,'bb','bb','bb','bb','bb','bb','bb','2017-04-13 16:00:17.815221',NULL),(8,'111','111','111','111','111','111','111','2017-04-20 15:17:51.518466',NULL),(9,'11','11111','11','11','1','1','1','2017-04-20 15:32:38.344672',NULL),(10,'123','123','123','123','12','123','123','2017-04-20 15:34:20.055207',NULL),(11,'12','12','12','12','12','12','12','2017-04-20 15:42:45.429671',NULL),(12,'a1','a1','a1','a1','a1','a1','a1','2017-07-07 16:34:49.676760',NULL),(13,'b1','b1','b1','b1','b1','b1','b1','2017-07-07 18:09:22.724331',NULL),(14,'cc','cc','cc','cc','cc','cc','cc','2017-07-15 18:55:36.182156',NULL),(15,'wes','wes','wes','wes','wes','wes','wes','2017-08-22 19:24:09.221020',NULL);
/*!40000 ALTER TABLE `tblMine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblMineProduct`
--

DROP TABLE IF EXISTS `tblMineProduct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblMineProduct` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mineID` int(11) NOT NULL,
  `mineProductID` int(11) NOT NULL,
  `dateAdded` datetime NOT NULL,
  `projectID` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `mineProductID` (`mineProductID`),
  KEY `fk_tblMineProduct_mineID` (`mineID`),
  KEY `tblmineproduct_ibfk_2` (`projectID`),
  CONSTRAINT `tblmineproduct_ibfk_1` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`) ON UPDATE CASCADE,
  CONSTRAINT `tblmineproduct_ibfk_2` FOREIGN KEY (`projectID`) REFERENCES `tblProject` (`projectID`) ON UPDATE CASCADE,
  CONSTRAINT `tblmineproduct_ibfk_3` FOREIGN KEY (`mineProductID`) REFERENCES `tblMineProductList` (`mineProductID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=225 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblMineProduct`
--

LOCK TABLES `tblMineProduct` WRITE;
/*!40000 ALTER TABLE `tblMineProduct` DISABLE KEYS */;
INSERT INTO `tblMineProduct` VALUES (201,1,1,'2017-05-24 21:30:04',87),(202,1,2,'2017-05-24 21:30:04',87),(203,1,1,'2017-05-24 21:53:27',97),(204,1,2,'2017-05-24 21:53:27',97),(205,1,1,'2017-05-28 21:16:28',98),(206,1,2,'2017-05-28 21:16:28',98),(207,1,1,'2017-05-30 21:33:58',99),(208,1,2,'2017-05-30 21:33:58',99),(209,1,1,'2017-05-30 21:34:41',100),(210,1,2,'2017-05-30 21:34:41',100),(211,1,1,'2017-06-06 07:14:26',101),(212,1,2,'2017-06-06 07:14:26',101),(213,13,1,'2017-07-14 17:19:38',102),(214,13,2,'2017-07-14 17:19:38',102),(215,14,1,'2017-07-18 01:32:09',103),(216,14,2,'2017-07-18 01:32:09',103),(217,14,1,'2017-07-18 19:28:45',104),(218,14,2,'2017-07-18 19:28:45',104),(219,14,1,'2017-07-18 19:32:44',105),(220,14,2,'2017-07-18 19:32:44',105),(221,14,1,'2017-07-18 19:35:07',106),(222,14,2,'2017-07-18 19:35:07',106),(223,14,1,'2017-07-18 19:39:21',107),(224,14,2,'2017-07-18 19:39:21',107);
/*!40000 ALTER TABLE `tblMineProduct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblMineProductGrade`
--

DROP TABLE IF EXISTS `tblMineProductGrade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblMineProductGrade` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mineID` int(11) NOT NULL,
  `projectID` int(11) NOT NULL,
  `commodityID` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `grade` float(12,6) DEFAULT NULL,
  `dateAdded` datetime NOT NULL,
  `stockpileID` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `projectID` (`projectID`),
  KEY `commodityID` (`commodityID`),
  KEY `fk_tblMineProductGrade_mineID` (`mineID`),
  CONSTRAINT `tblmineproductgrade_ibfk_1` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`) ON UPDATE CASCADE,
  CONSTRAINT `tblmineproductgrade_ibfk_2` FOREIGN KEY (`projectID`) REFERENCES `tblProject` (`projectID`) ON UPDATE CASCADE,
  CONSTRAINT `tblmineproductgrade_ibfk_4` FOREIGN KEY (`commodityID`) REFERENCES `tblCommodityList` (`commodityID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblMineProductGrade`
--

LOCK TABLES `tblMineProductGrade` WRITE;
/*!40000 ALTER TABLE `tblMineProductGrade` DISABLE KEYS */;
INSERT INTO `tblMineProductGrade` VALUES (1,14,107,22,1,3.050000,'2017-07-18 19:39:21',0),(2,14,107,22,2,1.050000,'2017-07-18 19:39:21',0),(3,14,107,3,1,1.050000,'2017-07-18 19:39:21',0),(4,14,107,3,2,1.050000,'2017-07-18 19:39:21',0),(5,14,107,33,1,1.050000,'2017-07-18 19:39:21',0),(6,14,107,33,2,1.050000,'2017-07-18 19:39:21',0),(7,14,107,50,1,1.050000,'2017-07-18 19:39:21',0),(8,14,107,50,2,1.050000,'2017-07-18 19:39:21',0),(9,14,107,22,1,1.050000,'2017-07-18 19:39:21',0),(10,14,107,22,2,1.050000,'2017-07-18 19:39:21',0),(11,14,107,3,1,1.050000,'2017-07-18 19:39:21',0),(12,14,107,3,2,1.050000,'2017-07-18 19:39:21',0),(13,14,107,33,1,1.050000,'2017-07-18 19:39:21',0),(14,14,107,33,2,1.050000,'2017-07-18 19:39:21',0),(15,14,107,50,1,1.050000,'2017-07-18 19:39:21',0),(16,14,107,50,2,1.050000,'2017-07-18 19:39:21',0),(17,14,109,22,1,1.050000,'2017-11-27 05:58:34',0),(18,14,109,22,2,1.050000,'2017-11-27 05:58:34',0),(19,14,109,3,1,1.050000,'2017-11-27 05:58:34',0),(20,14,109,3,2,1.050000,'2017-11-27 05:58:34',0),(21,14,109,33,1,1.050000,'2017-11-27 05:58:34',0),(22,14,109,33,2,1.050000,'2017-11-27 05:58:34',0),(23,14,109,50,1,1.050000,'2017-11-27 05:58:34',0),(24,14,109,50,2,1.050000,'2017-11-27 05:58:34',0),(25,14,109,22,1,1.050000,'2017-11-27 05:58:34',0),(26,14,109,22,2,1.050000,'2017-11-27 05:58:34',0),(27,14,109,3,1,1.050000,'2017-11-27 05:58:34',0),(28,14,109,3,2,1.050000,'2017-11-27 05:58:34',0),(29,14,109,33,1,1.050000,'2017-11-27 05:58:34',0),(30,14,109,33,2,1.050000,'2017-11-27 05:58:34',0),(31,14,109,50,1,1.050000,'2017-11-27 05:58:34',0),(32,14,109,50,2,1.050000,'2017-11-27 05:58:34',0),(33,14,110,22,1,1.050000,'2017-11-27 06:12:21',0),(34,14,110,22,2,1.050000,'2017-11-27 06:12:21',0),(35,14,110,3,1,1.050000,'2017-11-27 06:12:21',0),(36,14,110,3,2,1.050000,'2017-11-27 06:12:21',0),(37,14,110,33,1,1.050000,'2017-11-27 06:12:21',0),(38,14,110,33,2,1.050000,'2017-11-27 06:12:21',0),(39,14,110,50,1,1.050000,'2017-11-27 06:12:21',0),(40,14,110,50,2,1.050000,'2017-11-27 06:12:21',0),(41,14,110,22,1,1.050000,'2017-11-27 06:12:21',0),(42,14,110,22,2,1.050000,'2017-11-27 06:12:21',0),(43,14,110,3,1,1.050000,'2017-11-27 06:12:21',0),(44,14,110,3,2,1.050000,'2017-11-27 06:12:21',0),(45,14,110,33,1,1.050000,'2017-11-27 06:12:21',0),(46,14,110,33,2,1.050000,'2017-11-27 06:12:21',0),(47,14,110,50,1,1.050000,'2017-11-27 06:12:21',0),(48,14,110,50,2,1.050000,'2017-11-27 06:12:21',0),(49,14,111,22,1,1.050000,'2017-12-01 16:11:04',1),(50,14,111,22,2,1.050000,'2017-12-01 16:11:04',1),(51,14,111,3,1,1.050000,'2017-12-01 16:11:04',1),(52,14,111,3,2,1.050000,'2017-12-01 16:11:04',1),(53,14,111,33,1,1.050000,'2017-12-01 16:11:04',1),(54,14,111,33,2,1.050000,'2017-12-01 16:11:04',1),(55,14,111,50,1,1.050000,'2017-12-01 16:11:04',1),(56,14,111,50,2,1.050000,'2017-12-01 16:11:04',1),(57,14,111,22,1,1.050000,'2017-12-01 16:11:04',2),(58,14,111,22,2,1.050000,'2017-12-01 16:11:04',2),(59,14,111,3,1,1.050000,'2017-12-01 16:11:04',2),(60,14,111,3,2,1.050000,'2017-12-01 16:11:04',2),(61,14,111,33,1,1.050000,'2017-12-01 16:11:04',2),(62,14,111,33,2,1.050000,'2017-12-01 16:11:04',2),(63,14,111,50,1,1.050000,'2017-12-01 16:11:04',2),(64,14,111,50,2,1.050000,'2017-12-01 16:11:04',2),(65,15,112,22,1,60.500000,'2017-12-13 14:32:01',1),(66,15,112,22,2,60.000000,'2017-12-13 14:32:01',1),(67,15,112,3,1,0.700000,'2017-12-13 14:32:01',1),(68,15,112,3,2,0.600000,'2017-12-13 14:32:01',1),(69,15,112,33,1,1.300000,'2017-12-13 14:32:01',1),(70,15,112,33,2,0.800000,'2017-12-13 14:32:01',1),(71,15,112,50,1,8.800000,'2017-12-13 14:32:01',1),(72,15,112,50,2,10.800000,'2017-12-13 14:32:01',1),(73,15,112,22,1,53.299999,'2017-12-13 14:32:01',2),(74,15,112,22,2,53.299999,'2017-12-13 14:32:01',2),(75,15,112,3,1,0.600000,'2017-12-13 14:32:01',2),(76,15,112,3,2,0.600000,'2017-12-13 14:32:01',2),(77,15,112,33,1,0.600000,'2017-12-13 14:32:01',2),(78,15,112,33,2,0.600000,'2017-12-13 14:32:01',2),(79,15,112,50,1,20.900000,'2017-12-13 14:32:01',2),(80,15,112,50,2,20.900000,'2017-12-13 14:32:01',2),(81,14,113,22,1,60.500000,'2018-01-17 05:06:23',1),(82,14,113,22,2,60.000000,'2018-01-17 05:06:23',1),(83,14,113,3,1,0.700000,'2018-01-17 05:06:23',1),(84,14,113,3,2,0.600000,'2018-01-17 05:06:23',1),(85,14,113,33,1,1.300000,'2018-01-17 05:06:23',1),(86,14,113,33,2,0.800000,'2018-01-17 05:06:23',1),(87,14,113,50,1,8.800000,'2018-01-17 05:06:23',1),(88,14,113,50,2,10.800000,'2018-01-17 05:06:23',1),(89,14,113,22,1,53.299999,'2018-01-17 05:06:23',2),(90,14,113,22,2,53.299999,'2018-01-17 05:06:23',2),(91,14,113,3,1,0.600000,'2018-01-17 05:06:23',2),(92,14,113,3,2,0.600000,'2018-01-17 05:06:23',2),(93,14,113,33,1,0.600000,'2018-01-17 05:06:23',2),(94,14,113,33,2,0.600000,'2018-01-17 05:06:23',2),(95,14,113,50,1,20.900000,'2018-01-17 05:06:23',2),(96,14,113,50,2,20.900000,'2018-01-17 05:06:23',2);
/*!40000 ALTER TABLE `tblMineProductGrade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblMineProductGradeOptimized`
--

DROP TABLE IF EXISTS `tblMineProductGradeOptimized`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblMineProductGradeOptimized` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mineID` int(11) NOT NULL,
  `projectID` int(11) NOT NULL,
  `commodityID` int(11) NOT NULL,
  `grade` float(12,6) DEFAULT NULL,
  `date` date NOT NULL,
  `dateAdded` datetime NOT NULL,
  `optimized` tinyint(1) DEFAULT NULL,
  `stockpileID` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `mineID` (`mineID`),
  KEY `projectID` (`projectID`),
  KEY `commodityID` (`commodityID`),
  CONSTRAINT `tblmineproductgradeoptimized_ibfk_1` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`) ON UPDATE CASCADE,
  CONSTRAINT `tblmineproductgradeoptimized_ibfk_2` FOREIGN KEY (`projectID`) REFERENCES `tblProject` (`projectID`) ON UPDATE CASCADE,
  CONSTRAINT `tblmineproductgradeoptimized_ibfk_3` FOREIGN KEY (`commodityID`) REFERENCES `tblCommodityList` (`commodityID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblMineProductGradeOptimized`
--

LOCK TABLES `tblMineProductGradeOptimized` WRITE;
/*!40000 ALTER TABLE `tblMineProductGradeOptimized` DISABLE KEYS */;
INSERT INTO `tblMineProductGradeOptimized` VALUES (1,1,97,22,61.400002,'2017-05-01','2017-05-24 22:01:38',1,0),(2,1,97,22,53.299999,'2017-05-01','2017-05-24 22:01:38',1,0),(3,1,97,3,0.500000,'2017-05-01','2017-05-24 22:01:38',1,0),(4,1,97,3,0.600000,'2017-05-01','2017-05-24 22:01:38',1,0),(5,1,97,33,0.800000,'2017-05-01','2017-05-24 22:01:38',1,0),(6,1,97,33,0.600000,'2017-05-01','2017-05-24 22:01:38',1,0),(7,1,97,50,9.200000,'2017-05-01','2017-05-24 22:01:38',1,0),(8,1,97,50,20.900000,'2017-05-01','2017-05-24 22:01:38',1,0),(9,1,97,22,61.400002,'2017-05-01','2017-05-24 22:02:09',1,0),(10,1,97,22,53.299999,'2017-05-01','2017-05-24 22:02:09',1,0),(11,1,97,3,0.500000,'2017-05-01','2017-05-24 22:02:09',1,0),(12,1,97,3,0.600000,'2017-05-01','2017-05-24 22:02:09',1,0),(13,1,97,33,0.800000,'2017-05-01','2017-05-24 22:02:09',1,0),(14,1,97,33,0.600000,'2017-05-01','2017-05-24 22:02:09',1,0),(15,1,97,50,9.200000,'2017-05-01','2017-05-24 22:02:09',1,0),(16,1,97,50,20.900000,'2017-05-01','2017-05-24 22:02:09',1,0),(17,1,100,22,61.400002,'2017-05-01','2017-06-03 18:23:19',1,0),(18,1,100,22,53.299999,'2017-05-01','2017-06-03 18:23:19',1,0),(19,1,100,3,0.500000,'2017-05-01','2017-06-03 18:23:19',1,0),(20,1,100,3,0.600000,'2017-05-01','2017-06-03 18:23:19',1,0),(21,1,100,33,0.800000,'2017-05-01','2017-06-03 18:23:19',1,0),(22,1,100,33,0.600000,'2017-05-01','2017-06-03 18:23:19',1,0),(23,1,100,50,9.200000,'2017-05-01','2017-06-03 18:23:19',1,0),(24,1,100,50,20.900000,'2017-05-01','2017-06-03 18:23:19',1,0),(25,1,100,22,61.400002,'2018-05-01','2017-06-03 18:23:53',1,0),(26,1,100,22,53.299999,'2018-05-01','2017-06-03 18:23:53',1,0),(27,1,100,3,0.500000,'2018-05-01','2017-06-03 18:23:53',1,0),(28,1,100,3,0.600000,'2018-05-01','2017-06-03 18:23:53',1,0),(29,1,100,33,0.800000,'2018-05-01','2017-06-03 18:23:53',1,0),(30,1,100,33,0.600000,'2018-05-01','2017-06-03 18:23:53',1,0),(31,1,100,50,9.200000,'2018-05-01','2017-06-03 18:23:53',1,0),(32,1,100,50,20.900000,'2018-05-01','2017-06-03 18:23:53',1,0),(33,1,100,22,60.099998,'2018-06-01','2017-06-03 18:24:27',1,0),(34,1,100,22,53.200001,'2018-06-01','2017-06-03 18:24:27',1,0),(35,1,100,3,0.600000,'2018-06-01','2017-06-03 18:24:27',1,0),(36,1,100,3,0.600000,'2018-06-01','2017-06-03 18:24:27',1,0),(37,1,100,33,0.800000,'2018-06-01','2017-06-03 18:24:27',1,0),(38,1,100,33,0.500000,'2018-06-01','2017-06-03 18:24:27',1,0),(39,1,100,50,10.800000,'2018-06-01','2017-06-03 18:24:27',1,0),(40,1,100,50,21.200001,'2018-06-01','2017-06-03 18:24:27',1,0),(41,1,101,22,60.549999,'2017-05-01','2017-06-14 02:54:24',0,0),(42,1,101,22,53.259998,'2017-05-01','2017-06-14 02:54:24',0,0),(43,1,101,3,0.690000,'2017-05-01','2017-06-14 02:54:24',0,0),(44,1,101,3,0.600000,'2017-05-01','2017-06-14 02:54:24',0,0),(45,1,101,33,1.280000,'2017-05-01','2017-06-14 02:54:24',0,0),(46,1,101,33,0.620000,'2017-05-01','2017-06-14 02:54:24',0,0),(47,1,101,50,8.800000,'2017-05-01','2017-06-14 02:54:24',0,0),(48,1,101,50,20.950001,'2017-05-01','2017-06-14 02:54:24',0,0),(49,1,101,22,60.099998,'2018-05-01','2017-06-07 17:58:14',1,0),(50,1,101,22,53.200001,'2018-05-01','2017-06-07 17:58:14',1,0),(51,1,101,3,0.600000,'2018-05-01','2017-06-07 17:58:14',1,0),(52,1,101,3,0.600000,'2018-05-01','2017-06-07 17:58:14',1,0),(53,1,101,33,0.800000,'2018-05-01','2017-06-07 17:58:14',1,0),(54,1,101,33,0.500000,'2018-05-01','2017-06-07 17:58:14',1,0),(55,1,101,50,10.800000,'2018-05-01','2017-06-07 17:58:14',1,0),(56,1,101,50,21.200001,'2018-05-01','2017-06-07 17:58:14',1,0),(57,14,107,22,60.549999,'2017-05-01','2017-08-21 18:52:31',0,0),(58,14,107,22,53.259998,'2017-05-01','2017-08-21 18:52:31',0,0),(59,14,107,3,0.690000,'2017-05-01','2017-08-21 18:52:31',0,0),(60,14,107,3,0.600000,'2017-05-01','2017-08-21 18:52:31',0,0),(61,14,107,33,1.280000,'2017-05-01','2017-08-21 18:52:31',0,0),(62,14,107,33,0.620000,'2017-05-01','2017-08-21 18:52:31',0,0),(63,14,107,50,8.800000,'2017-05-01','2017-08-21 18:52:31',0,0),(64,14,107,50,20.950001,'2017-05-01','2017-08-21 18:52:31',0,0),(65,15,112,22,60.549999,'2018-01-15','2017-12-13 19:47:01',1,1),(66,15,112,3,0.690000,'2018-01-15','2017-12-13 19:47:01',1,1),(67,15,112,33,1.280000,'2018-01-15','2017-12-13 19:47:01',1,1),(68,15,112,50,8.800000,'2018-01-15','2017-12-13 19:47:01',1,1),(69,15,112,22,53.259998,'2018-01-15','2017-12-13 19:47:01',1,2),(70,15,112,3,0.600000,'2018-01-15','2017-12-13 19:47:01',1,2),(71,15,112,33,0.620000,'2018-01-15','2017-12-13 19:47:01',1,2),(72,15,112,50,20.950001,'2018-01-15','2017-12-13 19:47:01',1,2),(73,15,112,22,60.549999,'2018-01-01','2018-01-09 17:58:43',0,1),(74,15,112,3,0.690000,'2018-01-01','2018-01-09 17:58:43',0,1),(75,15,112,33,1.280000,'2018-01-01','2018-01-09 17:58:43',0,1),(76,15,112,50,8.800000,'2018-01-01','2018-01-09 17:58:43',0,1),(77,15,112,22,53.259998,'2018-01-01','2018-01-09 17:58:43',0,2),(78,15,112,3,0.600000,'2018-01-01','2018-01-09 17:58:43',0,2),(79,15,112,33,0.620000,'2018-01-01','2018-01-09 17:58:43',0,2),(80,15,112,50,20.950001,'2018-01-01','2018-01-09 17:58:43',0,2),(81,14,113,22,60.549999,'2018-01-01','2018-01-22 05:05:52',1,1),(82,14,113,3,0.690000,'2018-01-01','2018-01-22 05:05:52',1,1),(83,14,113,33,1.280000,'2018-01-01','2018-01-22 05:05:52',1,1),(84,14,113,50,8.800000,'2018-01-01','2018-01-22 05:05:52',1,1),(85,14,113,22,53.259998,'2018-01-01','2018-01-22 05:05:52',1,2),(86,14,113,3,0.600000,'2018-01-01','2018-01-22 05:05:52',1,2),(87,14,113,33,0.620000,'2018-01-01','2018-01-22 05:05:52',1,2),(88,14,113,50,20.950001,'2018-01-01','2018-01-22 05:05:52',1,2),(89,14,113,22,60.099998,'2018-01-02','2018-01-22 06:30:32',1,1),(90,14,113,3,0.600000,'2018-01-02','2018-01-22 06:30:32',1,1),(91,14,113,33,0.800000,'2018-01-02','2018-01-22 06:30:32',1,1),(92,14,113,50,10.800000,'2018-01-02','2018-01-22 06:30:32',1,1),(93,14,113,22,53.200001,'2018-01-02','2018-01-22 06:30:32',1,2),(94,14,113,3,0.600000,'2018-01-02','2018-01-22 06:30:32',1,2),(95,14,113,33,0.500000,'2018-01-02','2018-01-22 06:30:32',1,2),(96,14,113,50,21.200001,'2018-01-02','2018-01-22 06:30:32',1,2);
/*!40000 ALTER TABLE `tblMineProductGradeOptimized` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblMineProductList`
--

DROP TABLE IF EXISTS `tblMineProductList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblMineProductList` (
  `mineProductID` int(11) NOT NULL AUTO_INCREMENT,
  `mineProduct` varchar(30) NOT NULL,
  PRIMARY KEY (`mineProductID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblMineProductList`
--

LOCK TABLES `tblMineProductList` WRITE;
/*!40000 ALTER TABLE `tblMineProductList` DISABLE KEYS */;
INSERT INTO `tblMineProductList` VALUES (1,'High Grade Processed'),(2,'Low Grade Processed'),(3,'Waste'),(4,'Overburden');
/*!40000 ALTER TABLE `tblMineProductList` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblMineProductTonnage`
--

DROP TABLE IF EXISTS `tblMineProductTonnage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblMineProductTonnage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mineID` int(11) NOT NULL,
  `projectID` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `tonnage` float(20,2) DEFAULT NULL,
  `dateAdded` datetime NOT NULL,
  `stockpileID` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `projectID` (`projectID`),
  KEY `fk_tblMineProductTonnage_mineID` (`mineID`),
  CONSTRAINT `tblmineproducttonnage_ibfk_1` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`) ON UPDATE CASCADE,
  CONSTRAINT `tblmineproducttonnage_ibfk_2` FOREIGN KEY (`projectID`) REFERENCES `tblProject` (`projectID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblMineProductTonnage`
--

LOCK TABLES `tblMineProductTonnage` WRITE;
/*!40000 ALTER TABLE `tblMineProductTonnage` DISABLE KEYS */;
INSERT INTO `tblMineProductTonnage` VALUES (1,14,103,1,1.05,'2017-07-18 01:32:09',1),(2,14,103,2,1.05,'2017-07-18 01:32:09',1),(3,14,103,1,1.05,'2017-07-18 01:32:09',2),(4,14,103,2,1.05,'2017-07-18 01:32:09',2),(5,14,104,1,1.05,'2017-07-18 19:28:45',1),(6,14,104,2,1.05,'2017-07-18 19:28:45',1),(7,14,105,1,1.05,'2017-07-18 19:32:44',1),(8,14,105,2,1.05,'2017-07-18 19:32:44',1),(9,14,106,1,1.05,'2017-07-18 19:35:07',1),(10,14,106,2,1.05,'2017-07-18 19:35:07',1),(11,14,107,1,1.05,'2017-07-18 19:39:21',1),(12,14,107,2,1.05,'2017-07-18 19:39:21',1),(13,14,107,1,1.05,'2017-07-18 19:39:21',2),(14,14,107,2,1.05,'2017-07-18 19:39:21',2),(15,14,109,1,1.05,'2017-11-27 05:58:34',1),(16,14,109,2,1.05,'2017-11-27 05:58:34',1),(17,14,109,1,1.05,'2017-11-27 05:58:34',2),(18,14,109,2,1.05,'2017-11-27 05:58:34',2),(19,14,110,1,1.05,'2017-11-27 06:12:21',1),(20,14,110,2,1.05,'2017-11-27 06:12:21',1),(21,14,110,1,1.05,'2017-11-27 06:12:21',2),(22,14,110,2,1.05,'2017-11-27 06:12:21',2),(23,14,111,1,1.05,'2017-12-01 16:11:04',1),(24,14,111,2,1.05,'2017-12-01 16:11:04',1),(25,14,111,1,1.05,'2017-12-01 16:11:04',2),(26,14,111,2,1.05,'2017-12-01 16:11:04',2),(27,15,112,1,2238.40,'2017-12-13 14:32:01',1),(28,15,112,2,2492.20,'2017-12-13 14:32:01',1),(29,15,112,1,916.20,'2017-12-13 14:32:01',2),(30,15,112,2,1339.90,'2017-12-13 14:32:01',2),(31,14,113,1,2238.40,'2018-01-17 05:06:23',1),(32,14,113,2,2492.20,'2018-01-17 05:06:23',1),(33,14,113,1,916.20,'2018-01-17 05:06:23',2),(34,14,113,2,1339.90,'2018-01-17 05:06:23',2);
/*!40000 ALTER TABLE `tblMineProductTonnage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblMineProductTonnageOptimized`
--

DROP TABLE IF EXISTS `tblMineProductTonnageOptimized`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblMineProductTonnageOptimized` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mineID` int(11) NOT NULL,
  `projectID` int(11) NOT NULL,
  `tonnage` float(20,2) DEFAULT NULL,
  `date` date NOT NULL,
  `optimized` tinyint(1) DEFAULT NULL,
  `dateAdded` datetime NOT NULL,
  `stockpileID` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `projectID` (`projectID`),
  KEY `fk_tblMineProductTonnageOptimized_mineID` (`mineID`),
  CONSTRAINT `tblmineproducttonnageoptimized_ibfk_1` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`) ON UPDATE CASCADE,
  CONSTRAINT `tblmineproducttonnageoptimized_ibfk_3` FOREIGN KEY (`projectID`) REFERENCES `tblProject` (`projectID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblMineProductTonnageOptimized`
--

LOCK TABLES `tblMineProductTonnageOptimized` WRITE;
/*!40000 ALTER TABLE `tblMineProductTonnageOptimized` DISABLE KEYS */;
INSERT INTO `tblMineProductTonnageOptimized` VALUES (1,1,101,2200.00,'2017-05-01',0,'2017-06-14 02:54:24',0),(2,1,101,850.00,'2017-05-01',0,'2017-06-14 02:54:24',0),(3,1,101,2480.00,'2018-05-01',1,'2017-06-07 17:58:14',0),(4,1,101,1330.00,'2018-05-01',1,'2017-06-07 17:58:14',0),(5,14,107,2200.00,'2017-05-01',0,'2017-08-21 18:52:31',0),(6,14,107,900.00,'2017-05-01',0,'2017-08-21 18:52:31',0),(7,15,112,916.00,'2018-01-15',1,'2017-12-13 19:47:01',1),(8,15,112,2338.00,'2018-01-15',1,'2017-12-13 19:47:01',2),(11,15,112,2000.00,'2018-01-01',0,'2018-01-09 17:58:43',1),(12,15,112,800.00,'2018-01-01',0,'2018-01-09 17:58:43',2),(13,14,113,2238.00,'2018-01-01',1,'2018-01-22 05:05:52',1),(14,14,113,916.00,'2018-01-01',1,'2018-01-22 05:05:52',2),(15,14,113,2488.00,'2018-01-02',1,'2018-01-22 06:30:32',1),(16,14,113,1339.00,'2018-01-02',1,'2018-01-22 06:30:32',2);
/*!40000 ALTER TABLE `tblMineProductTonnageOptimized` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblOPEX`
--

DROP TABLE IF EXISTS `tblOPEX`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblOPEX` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `year` int(11) NOT NULL,
  `mining` decimal(20,2) NOT NULL,
  `infrastructure` decimal(20,2) NOT NULL,
  `stockpileLG` decimal(20,2) NOT NULL,
  `dewatering` decimal(20,2) NOT NULL,
  `processing` decimal(20,2) NOT NULL,
  `hauling` decimal(20,2) NOT NULL,
  `loadOutRailLoop` decimal(20,2) NOT NULL,
  `GASite` decimal(20,2) NOT NULL,
  `GARoomBoardFIFO` decimal(20,2) NOT NULL,
  `railTransport` decimal(20,2) NOT NULL,
  `GACorp` decimal(20,2) NOT NULL,
  `royalties` decimal(20,2) NOT NULL,
  `transportation` decimal(20,2) NOT NULL,
  `GA` decimal(20,2) NOT NULL,
  `shipping` decimal(20,2) NOT NULL,
  `dateAdded` datetime(6) NOT NULL,
  `mineID` int(11) NOT NULL,
  `opexPT` float(20,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tblOPEX_mineID_a7c19939_fk_tblMine_mineID` (`mineID`),
  CONSTRAINT `tblOPEX_mineID_a7c19939_fk_tblMine_mineID` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`)
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblOPEX`
--

LOCK TABLES `tblOPEX` WRITE;
/*!40000 ALTER TABLE `tblOPEX` DISABLE KEYS */;
INSERT INTO `tblOPEX` VALUES (1,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 16:16:03.204246',1,0.00),(2,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 16:16:03.204246',1,0.00),(3,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:03:19.697926',1,0.00),(4,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:03:19.697926',1,0.00),(5,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:14:18.616088',1,0.00),(6,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:14:18.616088',1,0.00),(7,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:14:47.351235',1,0.00),(8,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:14:47.351235',1,0.00),(9,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:15:32.717796',1,0.00),(10,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:15:32.717796',1,0.00),(11,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:16:35.530715',1,0.00),(12,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:16:35.530715',1,0.00),(13,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:17:41.461447',1,0.00),(14,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:17:41.461447',1,0.00),(15,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:24:45.882136',1,0.00),(16,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:24:45.882136',1,0.00),(17,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:25:20.385413',1,0.00),(18,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:25:20.385413',1,0.00),(19,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:27:36.355463',1,0.00),(20,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:27:36.355463',1,0.00),(21,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:34:23.421521',1,0.00),(22,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:34:23.421521',1,0.00),(23,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:36:53.651379',1,0.00),(24,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:36:53.651379',1,0.00),(25,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:37:04.431183',1,0.00),(26,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:37:04.431183',1,0.00),(27,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:38:52.012901',1,0.00),(28,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:38:52.012901',1,0.00),(29,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:40:22.546102',1,0.00),(30,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:40:22.546102',1,0.00),(31,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:46:04.205666',1,0.00),(32,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:46:04.205666',1,0.00),(33,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:47:36.362764',1,0.00),(34,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-26 21:47:36.362764',1,0.00),(35,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-27 13:06:52.409259',1,0.00),(36,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-27 13:06:52.409259',1,0.00),(37,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-27 13:07:37.248353',1,0.00),(38,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-27 13:07:37.248353',1,0.00),(39,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-28 18:40:48.195017',1,0.00),(40,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-02-28 18:40:48.195017',1,0.00),(41,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-01 20:49:03.056372',1,0.00),(42,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-01 20:49:03.056372',1,0.00),(43,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-02 01:05:02.620219',1,0.00),(44,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-02 01:05:02.620219',1,0.00),(45,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-02 01:06:28.887832',1,0.00),(46,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-02 01:06:28.887832',1,0.00),(47,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-07 15:26:32.916634',1,0.00),(48,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-07 15:26:32.916634',1,0.00),(49,1,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,'2017-03-09 14:12:14.199604',1,0.00),(50,2,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,3.33,'2017-03-09 14:12:14.199604',1,0.00),(51,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-12 19:45:44.893419',1,0.00),(52,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-12 19:45:44.893419',1,0.00),(53,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-13 00:34:43.370890',1,0.00),(54,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-13 00:34:43.370890',1,0.00),(55,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-13 23:20:54.594576',1,0.00),(56,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-13 23:20:54.594576',1,0.00),(57,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-14 04:17:15.533695',1,0.00),(58,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-14 04:17:15.533695',1,0.00),(59,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-14 22:35:44.781827',1,0.00),(60,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-14 22:35:44.781827',1,0.00),(61,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-21 16:49:44.462893',1,0.00),(62,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-21 16:49:44.462893',1,0.00),(63,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-21 20:34:19.172310',1,0.00),(64,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-21 20:34:19.172310',1,0.00),(65,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-21 20:37:32.540056',1,0.00),(66,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-21 20:37:32.540056',1,0.00),(67,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-23 05:55:19.321580',1,0.00),(68,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-03-23 05:55:19.321580',1,0.00),(69,1,34.68,0.00,0.00,0.94,5.08,8.15,2.53,4.66,4.26,71.39,1.93,3.86,0.00,0.00,15.63,'2017-03-26 22:44:00.542042',1,0.00),(70,2,34.68,0.00,0.00,0.94,5.08,8.15,2.53,4.66,4.26,71.39,1.93,3.86,0.00,0.00,15.63,'2017-03-26 22:44:00.542042',1,0.00),(71,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-04-07 16:29:26.316582',1,0.00),(72,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-04-07 18:56:30.311074',1,0.00),(73,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-04-07 19:18:00.566095',1,0.00),(74,1,34.68,0.00,0.00,0.94,5.08,8.15,2.53,4.66,4.26,71.39,1.93,3.86,0.00,0.00,15.63,'2017-04-11 16:50:12.429307',1,0.00),(75,1,34.68,0.00,0.00,0.94,5.08,8.15,2.53,4.66,4.26,71.39,1.93,3.86,0.00,0.00,15.63,'2017-04-13 21:09:35.380427',1,0.00),(76,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-04-22 15:32:36.299646',1,0.00),(77,1,34.68,0.00,0.00,0.94,5.08,8.15,2.53,4.66,4.26,0.00,1.93,3.86,0.00,0.00,15.63,'2017-04-26 14:55:23.379781',1,0.00),(78,1,34.68,0.00,0.00,0.94,5.08,8.15,2.53,4.66,4.26,71.39,1.93,3.86,0.00,0.00,15.63,'2017-05-11 21:27:44.422743',2,9.00),(79,2,45.19,0.00,0.00,1.25,5.61,8.67,2.74,6.21,5.09,79.49,2.57,1.75,0.00,0.00,15.63,'2017-05-11 21:27:44.422743',2,8.00),(80,1,34.68,0.00,0.00,0.94,5.08,8.15,2.53,4.66,4.26,71.39,1.93,3.86,0.00,0.00,15.63,'2017-05-12 02:53:20.547887',2,9.00),(81,2,45.19,0.00,0.00,1.25,5.61,8.67,2.74,6.21,5.09,79.49,2.57,1.75,0.00,0.00,15.63,'2017-05-12 02:53:20.547887',2,8.00),(82,1,34.68,0.00,0.00,0.94,5.08,8.15,2.53,4.66,4.26,71.39,1.93,3.86,0.00,0.00,15.63,'2017-05-12 03:50:01.211094',2,9.00),(83,2,45.19,0.00,0.00,1.25,5.61,8.67,2.74,6.21,5.09,79.49,2.57,1.75,0.00,0.00,15.63,'2017-05-12 03:50:01.211094',2,8.00),(84,1,34.68,0.00,0.00,0.94,5.08,8.15,2.53,4.66,4.26,71.39,1.93,3.86,0.00,0.00,15.63,'2017-05-13 16:49:01.118559',2,9.00),(85,2,45.19,0.00,0.00,1.25,5.61,8.67,2.74,6.21,5.09,79.49,2.57,1.75,0.00,0.00,15.63,'2017-05-13 16:49:01.118559',2,8.00),(86,1,34.68,0.00,0.00,0.94,5.08,8.15,2.35,4.66,4.26,71.39,1.93,3.86,0.00,0.00,15.63,'2017-05-24 21:32:53.982954',1,9.00),(87,2,45.19,0.00,0.00,1.25,5.61,8.67,2.74,6.21,5.09,79.49,2.57,1.75,0.00,0.00,15.63,'2017-05-24 21:32:53.982954',1,8.00),(88,1,34.68,0.00,0.00,0.94,5.08,8.15,2.53,4.66,4.26,71.39,1.93,3.86,0.00,0.00,15.63,'2017-05-24 21:55:46.845978',1,9.00),(89,2,45.19,0.00,0.00,1.25,5.61,8.67,2.74,6.21,5.09,79.49,2.57,1.75,0.00,0.00,15.63,'2017-05-24 21:55:46.845978',1,8.00),(90,1,34.68,0.00,0.00,0.94,5.08,8.15,2.53,4.66,4.26,71.39,1.93,3.86,0.00,0.00,15.63,'2017-05-28 21:24:15.614002',1,9.00),(91,2,45.19,0.00,0.00,1.25,5.61,8.67,2.74,6.21,5.09,79.49,2.57,1.75,0.00,0.00,15.63,'2017-05-28 21:24:15.614002',1,8.00),(92,1,34.68,0.00,3.00,0.94,5.08,8.15,2.53,4.66,4.26,71.39,1.93,3.86,0.00,0.00,15.63,'2017-05-30 21:40:14.480748',1,9.00),(93,2,45.19,0.00,0.64,1.25,5.61,8.67,2.74,6.21,5.09,79.49,2.57,1.75,0.00,0.00,15.63,'2017-05-30 21:40:14.480748',1,8.00),(94,1,34.68,0.00,3.00,0.94,5.08,8.15,2.53,4.66,4.26,71.39,1.93,3.86,0.00,0.00,15.63,'2017-06-06 07:20:38.316463',1,45.00),(95,2,45.19,0.00,0.00,1.25,5.61,8.67,2.74,6.21,5.09,79.49,2.57,1.75,0.00,0.00,15.63,'2017-06-06 07:20:38.316463',1,45.00),(96,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-07-14 17:19:38.379963',13,1.05),(97,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-07-14 17:19:38.379963',13,1.05),(98,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-07-18 01:32:08.899910',14,1.05),(99,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-07-18 01:32:08.899910',14,1.05),(100,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-07-18 19:39:21.342509',14,1.05),(101,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-07-18 19:39:21.342509',14,1.05),(102,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-11-27 05:58:34.236125',14,1.05),(103,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-11-27 05:58:34.236125',14,1.05),(104,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-11-27 06:12:20.970621',14,1.05),(105,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-11-27 06:12:20.970621',14,1.05),(106,1,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-12-01 16:11:03.772298',14,1.05),(107,2,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,'2017-12-01 16:11:03.772298',14,1.05),(108,1,34.68,0.00,0.00,0.94,5.08,8.15,2.53,4.66,4.26,71.39,1.93,3.86,0.00,0.00,15.63,'2017-12-13 14:32:01.423069',15,6.00),(109,2,45.19,0.00,0.00,1.25,5.61,8.67,2.74,6.21,5.09,79.49,2.57,1.75,0.00,0.00,15.63,'2017-12-13 14:32:01.423069',15,6.00),(110,1,34.68,0.00,0.00,0.94,5.08,8.15,2.53,4.66,4.26,71.39,1.93,3.86,0.00,0.00,15.63,'2018-01-17 05:06:22.706920',14,6.00),(111,2,45.19,0.00,0.00,1.25,5.61,8.67,2.74,6.21,5.09,79.49,2.57,1.75,0.00,0.00,15.63,'2018-01-17 05:06:22.706920',14,6.00);
/*!40000 ALTER TABLE `tblOPEX` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblPlantProduct`
--

DROP TABLE IF EXISTS `tblPlantProduct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblPlantProduct` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mineID` int(11) NOT NULL,
  `plantProductID` int(11) NOT NULL,
  `dateAdded` datetime NOT NULL,
  `projectID` int(11) NOT NULL,
  `recovery` float(12,6) DEFAULT NULL,
  `moisture` float(12,6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `plantProductID` (`plantProductID`),
  KEY `fk_tblPlantProduct_mineID` (`mineID`),
  KEY `projectID` (`projectID`),
  CONSTRAINT `tblplantproduct_ibfk_1` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`) ON UPDATE CASCADE,
  CONSTRAINT `tblplantproduct_ibfk_3` FOREIGN KEY (`plantProductID`) REFERENCES `tblPlantProductList` (`plantProductID`) ON UPDATE CASCADE,
  CONSTRAINT `tblplantproduct_ibfk_4` FOREIGN KEY (`projectID`) REFERENCES `tblProject` (`projectID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=203 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblPlantProduct`
--

LOCK TABLES `tblPlantProduct` WRITE;
/*!40000 ALTER TABLE `tblPlantProduct` DISABLE KEYS */;
INSERT INTO `tblPlantProduct` VALUES (167,1,1,'2017-05-24 21:30:04',87,NULL,NULL),(168,1,2,'2017-05-24 21:30:04',87,NULL,NULL),(169,1,1,'2017-05-24 21:53:27',97,NULL,NULL),(170,1,2,'2017-05-24 21:53:27',97,NULL,NULL),(171,1,1,'2017-05-28 21:16:28',98,NULL,NULL),(172,1,2,'2017-05-28 21:16:28',98,NULL,NULL),(173,1,1,'2017-05-30 21:33:58',99,NULL,NULL),(174,1,2,'2017-05-30 21:33:58',99,NULL,NULL),(175,1,1,'2017-05-30 21:34:41',100,NULL,NULL),(176,1,2,'2017-05-30 21:34:41',100,NULL,NULL),(177,1,1,'2017-06-06 07:14:26',101,NULL,NULL),(178,1,2,'2017-06-06 07:14:26',101,NULL,NULL),(179,13,1,'2017-07-14 17:19:38',102,NULL,NULL),(180,13,2,'2017-07-14 17:19:38',102,NULL,NULL),(181,14,1,'2017-07-18 01:32:09',103,NULL,NULL),(182,14,2,'2017-07-18 01:32:09',103,NULL,NULL),(183,14,1,'2017-07-18 19:28:45',104,NULL,NULL),(184,14,2,'2017-07-18 19:28:45',104,NULL,NULL),(185,14,1,'2017-07-18 19:32:44',105,NULL,NULL),(186,14,2,'2017-07-18 19:32:44',105,NULL,NULL),(187,14,1,'2017-07-18 19:35:07',106,NULL,NULL),(188,14,2,'2017-07-18 19:35:07',106,NULL,NULL),(189,14,1,'2017-07-18 19:39:21',107,NULL,NULL),(190,14,2,'2017-07-18 19:39:21',107,NULL,NULL),(191,14,1,'2017-11-27 05:51:13',108,NULL,NULL),(192,14,2,'2017-11-27 05:51:13',108,NULL,NULL),(193,14,1,'2017-11-27 05:58:34',109,NULL,NULL),(194,14,2,'2017-11-27 05:58:34',109,NULL,NULL),(195,14,1,'2017-11-27 06:12:21',110,NULL,NULL),(196,14,2,'2017-11-27 06:12:21',110,NULL,NULL),(197,14,1,'2017-12-01 16:11:04',111,NULL,NULL),(198,14,2,'2017-12-01 16:11:04',111,NULL,NULL),(199,15,1,'2017-12-13 14:32:01',112,NULL,NULL),(200,15,2,'2017-12-13 14:32:01',112,NULL,NULL),(201,14,1,'2018-01-17 05:06:23',113,NULL,NULL),(202,14,2,'2018-01-17 05:06:23',113,NULL,NULL);
/*!40000 ALTER TABLE `tblPlantProduct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblPlantProductGradeOptimized`
--

DROP TABLE IF EXISTS `tblPlantProductGradeOptimized`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblPlantProductGradeOptimized` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mineID` int(11) NOT NULL,
  `projectID` int(11) NOT NULL,
  `plantProductID` int(11) NOT NULL,
  `commodityID` int(11) NOT NULL,
  `grade` float(12,6) DEFAULT NULL,
  `date` date NOT NULL,
  `dateAdded` datetime NOT NULL,
  `optimized` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `mineID` (`mineID`),
  KEY `projectID` (`projectID`),
  KEY `plantProductID` (`plantProductID`),
  KEY `commodityID` (`commodityID`),
  CONSTRAINT `tblplantproductgradeoptimized_ibfk_1` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`) ON UPDATE CASCADE,
  CONSTRAINT `tblplantproductgradeoptimized_ibfk_2` FOREIGN KEY (`projectID`) REFERENCES `tblProject` (`projectID`) ON UPDATE CASCADE,
  CONSTRAINT `tblplantproductgradeoptimized_ibfk_3` FOREIGN KEY (`plantProductID`) REFERENCES `tblPlantProductList` (`plantProductID`) ON UPDATE CASCADE,
  CONSTRAINT `tblplantproductgradeoptimized_ibfk_4` FOREIGN KEY (`commodityID`) REFERENCES `tblCommodityList` (`commodityID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblPlantProductGradeOptimized`
--

LOCK TABLES `tblPlantProductGradeOptimized` WRITE;
/*!40000 ALTER TABLE `tblPlantProductGradeOptimized` DISABLE KEYS */;
INSERT INTO `tblPlantProductGradeOptimized` VALUES (1,1,97,1,22,61.660000,'2017-05-01','2017-05-24 22:01:38',1),(2,1,97,2,22,58.770000,'2017-05-01','2017-05-24 22:01:38',1),(3,1,97,1,3,0.540000,'2017-05-01','2017-05-24 22:01:38',1),(4,1,97,2,3,0.510000,'2017-05-01','2017-05-24 22:01:38',1),(5,1,97,1,33,0.780000,'2017-05-01','2017-05-24 22:01:38',1),(6,1,97,2,33,0.750000,'2017-05-01','2017-05-24 22:01:38',1),(7,1,97,1,50,11.980000,'2017-05-01','2017-05-24 22:01:38',1),(8,1,97,2,50,11.420000,'2017-05-01','2017-05-24 22:01:38',1),(9,1,97,1,22,61.660000,'2017-05-01','2017-05-24 22:02:09',1),(10,1,97,2,22,58.770000,'2017-05-01','2017-05-24 22:02:09',1),(11,1,97,1,3,0.540000,'2017-05-01','2017-05-24 22:02:09',1),(12,1,97,2,3,0.510000,'2017-05-01','2017-05-24 22:02:09',1),(13,1,97,1,33,0.780000,'2017-05-01','2017-05-24 22:02:09',1),(14,1,97,2,33,0.750000,'2017-05-01','2017-05-24 22:02:09',1),(15,1,97,1,50,11.980000,'2017-05-01','2017-05-24 22:02:09',1),(16,1,97,2,50,11.420000,'2017-05-01','2017-05-24 22:02:09',1),(17,1,100,1,22,61.660000,'2017-05-01','2017-06-03 18:23:19',1),(18,1,100,2,22,58.770000,'2017-05-01','2017-06-03 18:23:19',1),(19,1,100,1,3,0.540000,'2017-05-01','2017-06-03 18:23:19',1),(20,1,100,2,3,0.510000,'2017-05-01','2017-06-03 18:23:19',1),(21,1,100,1,33,0.780000,'2017-05-01','2017-06-03 18:23:19',1),(22,1,100,2,33,0.750000,'2017-05-01','2017-06-03 18:23:19',1),(23,1,100,1,50,11.980000,'2017-05-01','2017-06-03 18:23:19',1),(24,1,100,2,50,11.420000,'2017-05-01','2017-06-03 18:23:19',1),(25,1,100,1,22,61.660000,'2018-05-01','2017-06-03 18:23:53',1),(26,1,100,2,22,58.770000,'2018-05-01','2017-06-03 18:23:53',1),(27,1,100,1,3,0.540000,'2018-05-01','2017-06-03 18:23:53',1),(28,1,100,2,3,0.510000,'2018-05-01','2017-06-03 18:23:53',1),(29,1,100,1,33,0.780000,'2018-05-01','2017-06-03 18:23:53',1),(30,1,100,2,33,0.750000,'2018-05-01','2017-06-03 18:23:53',1),(31,1,100,1,50,11.980000,'2018-05-01','2017-06-03 18:23:53',1),(32,1,100,2,50,11.420000,'2018-05-01','2017-06-03 18:23:53',1),(33,1,100,1,22,59.549999,'2018-06-01','2017-06-03 18:24:27',1),(34,1,100,2,22,56.759998,'2018-06-01','2017-06-03 18:24:27',1),(35,1,100,1,3,0.620000,'2018-06-01','2017-06-03 18:24:27',1),(36,1,100,2,3,0.590000,'2018-06-01','2017-06-03 18:24:27',1),(37,1,100,1,33,0.720000,'2018-06-01','2017-06-03 18:24:27',1),(38,1,100,2,33,0.680000,'2018-06-01','2017-06-03 18:24:27',1),(39,1,100,1,50,14.900000,'2018-06-01','2017-06-03 18:24:27',1),(40,1,100,2,50,14.200000,'2018-06-01','2017-06-03 18:24:27',1),(41,1,101,1,22,60.410000,'2017-05-01','2017-06-14 02:54:24',0),(42,1,101,2,22,57.570000,'2017-05-01','2017-06-14 02:54:24',0),(43,1,101,1,3,0.690000,'2017-05-01','2017-06-14 02:54:24',0),(44,1,101,2,3,0.650000,'2017-05-01','2017-06-14 02:54:24',0),(45,1,101,1,33,1.130000,'2017-05-01','2017-06-14 02:54:24',0),(46,1,101,2,33,1.080000,'2017-05-01','2017-06-14 02:54:24',0),(47,1,101,1,50,12.580000,'2017-05-01','2017-06-14 02:54:24',0),(48,1,101,2,50,11.990000,'2017-05-01','2017-06-14 02:54:24',0),(49,1,101,1,22,59.549999,'2018-05-01','2017-06-07 17:58:14',1),(50,1,101,2,22,56.759998,'2018-05-01','2017-06-07 17:58:14',1),(51,1,101,1,3,0.620000,'2018-05-01','2017-06-07 17:58:14',1),(52,1,101,2,3,0.590000,'2018-05-01','2017-06-07 17:58:14',1),(53,1,101,1,33,0.720000,'2018-05-01','2017-06-07 17:58:14',1),(54,1,101,2,33,0.680000,'2018-05-01','2017-06-07 17:58:14',1),(55,1,101,1,50,14.900000,'2018-05-01','2017-06-07 17:58:14',1),(56,1,101,2,50,14.200000,'2018-05-01','2017-06-07 17:58:14',1),(57,14,107,1,22,58.430000,'2017-05-01','2017-08-21 18:52:31',0),(58,14,107,2,22,58.430000,'2017-05-01','2017-08-21 18:52:31',0),(59,14,107,1,3,0.660000,'2017-05-01','2017-08-21 18:52:31',0),(60,14,107,2,3,0.660000,'2017-05-01','2017-08-21 18:52:31',0),(61,14,107,1,33,1.090000,'2017-05-01','2017-08-21 18:52:31',0),(62,14,107,2,33,1.090000,'2017-05-01','2017-08-21 18:52:31',0),(63,14,107,1,50,12.330000,'2017-05-01','2017-08-21 18:52:31',0),(64,14,107,2,50,12.330000,'2017-05-01','2017-08-21 18:52:31',0),(65,15,112,1,22,60.380001,'2018-01-15','2017-12-13 19:47:01',1),(66,15,112,2,22,57.549999,'2018-01-15','2017-12-13 19:47:01',1),(67,15,112,1,3,0.690000,'2018-01-15','2017-12-13 19:47:01',1),(68,15,112,2,3,0.650000,'2018-01-15','2017-12-13 19:47:01',1),(69,15,112,1,33,1.130000,'2018-01-15','2017-12-13 19:47:01',1),(70,15,112,2,33,1.080000,'2018-01-15','2017-12-13 19:47:01',1),(71,15,112,1,50,12.610000,'2018-01-15','2017-12-13 19:47:01',1),(72,15,112,2,50,12.020000,'2018-01-15','2017-12-13 19:47:01',1),(73,15,112,1,22,60.349998,'2018-01-01','2018-01-09 17:58:43',0),(74,15,112,2,22,57.520000,'2018-01-01','2018-01-09 17:58:43',0),(75,15,112,1,3,0.690000,'2018-01-01','2018-01-09 17:58:43',0),(76,15,112,2,3,0.650000,'2018-01-01','2018-01-09 17:58:43',0),(77,15,112,1,33,1.130000,'2018-01-01','2018-01-09 17:58:43',0),(78,15,112,2,33,1.070000,'2018-01-01','2018-01-09 17:58:43',0),(79,15,112,1,50,12.670000,'2018-01-01','2018-01-09 17:58:43',0),(80,15,112,2,50,12.070000,'2018-01-01','2018-01-09 17:58:43',0),(81,14,113,1,22,60.320000,'2018-01-01','2018-01-22 05:05:52',1),(82,14,113,2,22,57.490002,'2018-01-01','2018-01-22 05:05:52',1),(83,14,113,1,3,0.690000,'2018-01-01','2018-01-22 05:05:52',1),(84,14,113,2,3,0.650000,'2018-01-01','2018-01-22 05:05:52',1),(85,14,113,1,33,1.120000,'2018-01-01','2018-01-22 05:05:52',1),(86,14,113,2,33,1.070000,'2018-01-01','2018-01-22 05:05:52',1),(87,14,113,1,50,12.730000,'2018-01-01','2018-01-22 05:05:52',1),(88,14,113,2,50,12.130000,'2018-01-01','2018-01-22 05:05:52',1),(89,14,113,1,22,59.549999,'2018-01-02','2018-01-22 06:30:32',1),(90,14,113,2,22,56.759998,'2018-01-02','2018-01-22 06:30:32',1),(91,14,113,1,3,0.620000,'2018-01-02','2018-01-22 06:30:32',1),(92,14,113,2,3,0.590000,'2018-01-02','2018-01-22 06:30:32',1),(93,14,113,1,33,0.720000,'2018-01-02','2018-01-22 06:30:32',1),(94,14,113,2,33,0.680000,'2018-01-02','2018-01-22 06:30:32',1),(95,14,113,1,50,14.900000,'2018-01-02','2018-01-22 06:30:32',1),(96,14,113,2,50,14.210000,'2018-01-02','2018-01-22 06:30:32',1);
/*!40000 ALTER TABLE `tblPlantProductGradeOptimized` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblPlantProductList`
--

DROP TABLE IF EXISTS `tblPlantProductList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblPlantProductList` (
  `plantProductID` int(11) NOT NULL AUTO_INCREMENT,
  `plantProduct` varchar(30) NOT NULL,
  PRIMARY KEY (`plantProductID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblPlantProductList`
--

LOCK TABLES `tblPlantProductList` WRITE;
/*!40000 ALTER TABLE `tblPlantProductList` DISABLE KEYS */;
INSERT INTO `tblPlantProductList` VALUES (1,'Lump'),(2,'Fines'),(3,'Ultra Fines'),(4,'Rejects');
/*!40000 ALTER TABLE `tblPlantProductList` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblPlantProductTonnage`
--

DROP TABLE IF EXISTS `tblPlantProductTonnage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblPlantProductTonnage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mineID` int(11) NOT NULL,
  `plantProductID` int(11) NOT NULL,
  `dateAdded` datetime NOT NULL,
  `optimized` tinyint(1) DEFAULT NULL,
  `tonnageWMT` float(20,2) DEFAULT NULL,
  `tonnageDMT` float(20,2) DEFAULT NULL,
  `date` date NOT NULL,
  `projectID` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `plantProductID` (`plantProductID`),
  KEY `fk_tblPlantProductTonnage_mineID` (`mineID`),
  KEY `tblPlantProductTonnage_optimized` (`optimized`),
  KEY `tblplantproducttonnage_ibfk_3` (`projectID`),
  CONSTRAINT `tblplantproducttonnage_ibfk_1` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`) ON UPDATE CASCADE,
  CONSTRAINT `tblplantproducttonnage_ibfk_2` FOREIGN KEY (`plantProductID`) REFERENCES `tblPlantProductList` (`plantProductID`) ON UPDATE CASCADE,
  CONSTRAINT `tblplantproducttonnage_ibfk_3` FOREIGN KEY (`projectID`) REFERENCES `tblProject` (`projectID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblPlantProductTonnage`
--

LOCK TABLES `tblPlantProductTonnage` WRITE;
/*!40000 ALTER TABLE `tblPlantProductTonnage` DISABLE KEYS */;
INSERT INTO `tblPlantProductTonnage` VALUES (48,1,1,'2017-05-24 22:01:38',1,6202.00,5953.92,'2017-05-01',97),(49,1,2,'2017-05-24 22:01:38',1,11518.00,10711.74,'2017-05-01',97),(50,1,1,'2017-05-24 22:02:09',1,6202.00,5953.92,'2017-05-01',97),(51,1,2,'2017-05-24 22:02:09',1,11518.00,10711.74,'2017-05-01',97),(52,1,1,'2017-06-03 18:23:19',1,6202.00,5953.92,'2017-05-01',100),(53,1,2,'2017-06-03 18:23:19',1,11518.00,10711.74,'2017-05-01',100),(54,1,1,'2017-06-03 18:23:53',1,6202.00,5953.92,'2018-05-01',100),(55,1,2,'2017-06-03 18:23:53',1,11518.00,10711.74,'2018-05-01',100),(56,1,1,'2017-06-03 18:24:27',1,1333.50,1280.16,'2018-06-01',100),(57,1,2,'2017-06-03 18:24:27',1,2476.50,2303.14,'2018-06-01',100),(58,1,1,'2017-06-14 02:54:24',0,1067.50,1024.80,'2017-05-01',101),(59,1,2,'2017-06-14 02:54:24',0,1982.50,1843.72,'2017-05-01',101),(60,1,1,'2017-06-07 17:58:14',1,1333.50,1280.16,'2018-05-01',101),(61,1,2,'2017-06-07 17:58:14',1,2476.50,2303.14,'2018-05-01',101),(62,14,1,'2017-08-21 18:52:31',0,32.55,32.21,'2017-05-01',107),(63,14,2,'2017-08-21 18:52:31',0,32.55,32.21,'2017-05-01',107),(64,15,1,'2017-12-13 19:47:01',1,1138.90,1093.34,'2018-01-15',112),(65,15,2,'2017-12-13 19:47:01',1,2115.10,1967.04,'2018-01-15',112),(66,15,1,'2018-01-09 17:58:43',0,1103.90,1059.74,'2018-01-01',112),(67,15,2,'2018-01-09 17:58:43',0,2050.10,1906.59,'2018-01-01',112),(68,14,1,'2018-01-22 05:05:52',1,1103.90,1059.74,'2018-01-01',113),(69,14,2,'2018-01-22 05:05:52',1,2050.10,1906.59,'2018-01-01',113),(70,14,1,'2018-01-22 06:30:32',1,1339.45,1285.87,'2018-01-02',113),(71,14,2,'2018-01-22 06:30:32',1,2487.55,2313.42,'2018-01-02',113);
/*!40000 ALTER TABLE `tblPlantProductTonnage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblPrice`
--

DROP TABLE IF EXISTS `tblPrice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblPrice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mineID` int(11) NOT NULL,
  `projectID` int(11) NOT NULL,
  `stockpileID` int(11) NOT NULL,
  `lump` float(12,2) DEFAULT NULL,
  `lumpPrem` float(12,2) DEFAULT NULL,
  `fines` float(12,2) DEFAULT NULL,
  `ultraFines` float(12,2) DEFAULT NULL,
  `lumpAvg` float(12,2) DEFAULT NULL,
  `dateAdded` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `projectID` (`projectID`),
  KEY `fk_tblPrice_mineID` (`mineID`),
  CONSTRAINT `tblprice_ibfk_1` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`) ON UPDATE CASCADE,
  CONSTRAINT `tblprice_ibfk_2` FOREIGN KEY (`projectID`) REFERENCES `tblProject` (`projectID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblPrice`
--

LOCK TABLES `tblPrice` WRITE;
/*!40000 ALTER TABLE `tblPrice` DISABLE KEYS */;
INSERT INTO `tblPrice` VALUES (1,14,110,1,1.05,1.05,1.05,1.05,1.05,'2017-11-27 06:12:21'),(2,14,110,2,1.05,1.05,1.05,1.05,1.05,'2017-11-27 06:12:21'),(3,14,111,1,1.05,1.05,1.05,1.05,1.05,'2017-12-01 16:11:04'),(4,14,111,2,1.05,1.05,1.05,1.05,1.05,'2017-12-01 16:11:04'),(5,15,112,1,110.00,15.00,95.00,0.00,100.25,'2017-12-13 14:32:01'),(6,15,112,2,98.00,15.00,83.00,0.00,88.25,'2017-12-13 14:32:01'),(7,14,113,1,110.00,15.00,95.00,0.00,100.25,'2018-01-17 05:06:23'),(8,14,113,2,98.00,15.00,83.00,0.00,88.25,'2018-01-17 05:06:23');
/*!40000 ALTER TABLE `tblPrice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblProject`
--

DROP TABLE IF EXISTS `tblProject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblProject` (
  `projectID` int(11) NOT NULL AUTO_INCREMENT,
  `LOM` int(11) NOT NULL,
  `dateAdded` datetime(6) NOT NULL,
  `mineID` int(11) NOT NULL,
  `projectTypeID` int(11) NOT NULL,
  `startDate` date NOT NULL,
  `numStockpiles` int(11) NOT NULL,
  PRIMARY KEY (`projectID`),
  KEY `tblProject_mineID_9ecbcca3_fk_tblMine_mineID` (`mineID`),
  KEY `tblPr_projectTypeID_629dc341_fk_tblProjectTypeList_projectTypeID` (`projectTypeID`),
  CONSTRAINT `tblPr_projectTypeID_629dc341_fk_tblProjectTypeList_projectTypeID` FOREIGN KEY (`projectTypeID`) REFERENCES `tblProjectTypeList` (`projectTypeID`),
  CONSTRAINT `tblProject_mineID_9ecbcca3_fk_tblMine_mineID` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`)
) ENGINE=InnoDB AUTO_INCREMENT=114 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblProject`
--

LOCK TABLES `tblProject` WRITE;
/*!40000 ALTER TABLE `tblProject` DISABLE KEYS */;
INSERT INTO `tblProject` VALUES (1,2,'2017-02-26 16:14:52.606197',1,1,'0000-00-00',0),(2,2,'2017-02-26 21:02:30.628041',1,1,'0000-00-00',0),(3,2,'2017-02-28 07:26:34.143306',1,1,'0000-00-00',0),(4,2,'2017-02-28 08:15:04.993474',1,1,'0000-00-00',0),(5,2,'2017-02-28 08:17:03.129215',1,1,'0000-00-00',0),(6,2,'2017-02-28 08:20:11.202918',1,1,'0000-00-00',0),(7,2,'2017-02-28 08:20:17.357399',1,1,'0000-00-00',0),(8,2,'2017-02-28 08:20:32.722969',1,1,'0000-00-00',0),(9,2,'2017-02-28 08:21:21.697992',1,1,'0000-00-00',0),(10,2,'2017-02-28 08:22:48.226649',1,1,'0000-00-00',0),(11,2,'2017-02-28 08:26:52.791587',1,1,'0000-00-00',0),(12,2,'2017-02-28 08:29:34.398728',1,1,'0000-00-00',0),(13,2,'2017-02-28 08:30:04.204225',1,1,'0000-00-00',0),(14,2,'2017-02-28 08:32:21.291853',1,1,'0000-00-00',0),(15,2,'2017-02-28 08:33:05.133306',1,1,'0000-00-00',0),(16,2,'2017-02-28 08:40:42.691161',1,1,'0000-00-00',0),(17,2,'2017-02-28 08:42:58.730522',1,1,'0000-00-00',0),(18,2,'2017-02-28 08:43:56.784108',1,1,'0000-00-00',0),(19,2,'2017-02-28 08:44:15.589206',1,1,'0000-00-00',0),(20,2,'2017-02-28 08:45:00.174459',1,1,'0000-00-00',0),(21,2,'2017-02-28 08:46:09.952554',1,1,'0000-00-00',0),(22,2,'2017-02-28 08:52:19.552731',1,1,'0000-00-00',0),(23,2,'2017-02-28 08:53:50.672619',1,1,'0000-00-00',0),(24,2,'2017-02-28 08:55:06.176515',1,1,'0000-00-00',0),(25,2,'2017-02-28 08:55:52.006537',1,1,'0000-00-00',0),(26,2,'2017-02-28 08:58:01.967545',1,1,'0000-00-00',0),(27,2,'2017-02-28 08:59:51.489572',1,1,'0000-00-00',0),(28,2,'2017-02-28 09:00:42.562329',1,1,'0000-00-00',0),(29,2,'2017-02-28 09:01:28.367313',1,1,'0000-00-00',0),(30,2,'2017-02-28 09:06:01.807909',1,1,'0000-00-00',0),(31,2,'2017-02-28 09:08:13.039147',1,1,'0000-00-00',0),(32,2,'2017-02-28 09:11:05.879121',1,1,'0000-00-00',0),(33,2,'2017-02-28 09:13:12.638429',1,1,'0000-00-00',0),(34,2,'2017-02-28 09:13:50.222940',1,1,'0000-00-00',0),(35,2,'2017-02-28 09:16:41.670606',1,1,'0000-00-00',0),(36,2,'2017-02-28 09:18:42.133914',1,1,'0000-00-00',0),(37,2,'2017-02-28 09:19:12.661418',1,1,'0000-00-00',0),(38,2,'2017-02-28 09:21:27.988653',1,1,'0000-00-00',0),(39,2,'2017-02-28 09:22:27.005200',1,1,'0000-00-00',0),(40,2,'2017-02-28 09:30:55.472011',1,1,'0000-00-00',0),(41,2,'2017-02-28 09:39:57.930764',1,1,'0000-00-00',0),(42,2,'2017-02-28 09:40:21.053586',1,1,'0000-00-00',0),(43,2,'2017-02-28 09:40:58.177911',1,1,'0000-00-00',0),(44,2,'2017-02-28 09:41:57.572033',1,1,'0000-00-00',0),(45,2,'2017-02-28 09:44:16.782744',1,1,'0000-00-00',0),(46,2,'2017-02-28 09:44:43.974965',1,1,'0000-00-00',0),(47,2,'2017-02-28 09:53:50.838112',1,1,'0000-00-00',0),(48,2,'2017-02-28 09:54:30.949292',1,1,'0000-00-00',0),(49,2,'2017-02-28 09:55:01.579890',1,1,'0000-00-00',0),(50,2,'2017-02-28 10:01:41.158476',1,1,'0000-00-00',0),(51,2,'2017-02-28 10:02:50.811624',1,1,'0000-00-00',0),(52,3,'2017-02-28 10:03:57.259092',1,1,'0000-00-00',0),(53,5,'2017-02-28 10:04:04.443366',1,1,'0000-00-00',0),(54,8,'2017-02-28 10:04:13.050698',1,1,'0000-00-00',0),(55,8,'2017-02-28 10:04:50.985657',1,1,'0000-00-00',0),(56,2,'2017-02-28 10:16:11.563247',1,1,'0000-00-00',0),(57,2,'2017-02-28 10:19:36.683627',1,1,'0000-00-00',0),(58,2,'2017-02-28 10:22:37.122380',1,1,'0000-00-00',0),(59,2,'2017-02-28 10:23:03.819543',1,1,'0000-00-00',0),(60,2,'2017-02-28 10:26:20.642587',1,1,'0000-00-00',0),(61,2,'2017-02-28 10:34:22.841916',1,1,'0000-00-00',0),(62,2,'2017-02-28 10:34:38.391069',1,1,'0000-00-00',0),(63,2,'2017-02-28 18:40:01.464541',1,1,'0000-00-00',0),(64,2,'2017-03-01 17:49:58.423691',1,1,'0000-00-00',0),(65,2,'2017-03-02 01:04:21.695870',1,1,'0000-00-00',0),(66,2,'2017-03-07 15:25:02.141321',1,1,'0000-00-00',0),(67,3,'2017-03-08 15:30:22.922324',1,2,'0000-00-00',0),(68,2,'2017-03-08 15:39:40.874208',1,2,'0000-00-00',0),(69,2,'2017-03-12 18:52:25.924555',1,1,'0000-00-00',0),(70,2,'2017-03-12 18:54:09.066782',1,1,'0000-00-00',0),(71,2,'2017-03-12 18:55:46.042464',1,1,'0000-00-00',0),(72,2,'2017-03-12 19:18:18.731249',1,1,'0000-00-00',0),(73,2,'2017-03-12 19:44:41.358754',1,1,'0000-00-00',0),(74,2,'2017-03-13 00:33:49.561785',1,1,'0000-00-00',0),(75,2,'2017-03-13 23:20:17.784602',1,1,'0000-00-00',0),(76,2,'2017-03-14 04:16:12.884568',1,1,'0000-00-00',0),(77,2,'2017-03-14 22:34:59.419196',1,1,'0000-00-00',0),(78,2,'2017-03-21 16:48:47.108331',1,1,'0000-00-00',0),(79,2,'2017-03-23 05:54:29.921850',1,1,'0000-00-00',0),(80,2,'2017-03-26 22:37:52.898434',1,1,'0000-00-00',0),(81,1,'2017-04-07 16:26:59.399524',1,1,'0000-00-00',0),(82,1,'2017-04-07 18:56:07.474571',1,1,'0000-00-00',0),(83,1,'2017-04-07 19:17:31.137403',1,1,'0000-00-00',0),(84,1,'2017-04-11 16:44:44.524442',1,1,'0000-00-00',0),(85,1,'2017-04-13 21:05:25.375586',1,1,'0000-00-00',0),(86,1,'2017-04-22 15:32:14.054799',1,1,'0000-00-00',0),(87,1,'2017-04-26 14:28:27.860000',1,1,'0000-00-00',0),(88,2,'2017-05-10 19:42:31.380480',2,1,'0000-00-00',0),(89,2,'2017-05-11 20:40:42.113603',2,1,'2017-05-01',0),(90,2,'2017-05-12 03:31:14.962860',2,1,'2017-05-01',0),(91,2,'2017-05-13 04:40:34.234989',2,1,'2017-05-01',0),(92,2,'2017-05-13 06:13:16.169029',2,1,'2017-05-01',0),(93,2,'2017-05-13 06:13:55.774695',2,1,'2017-05-01',0),(94,2,'2017-05-13 06:14:27.750981',2,1,'2017-05-01',0),(95,2,'2017-05-13 06:20:51.871582',2,1,'2017-05-01',0),(96,2,'2017-05-24 21:30:03.900035',1,1,'2017-01-01',0),(97,2,'2017-05-24 21:53:26.818793',1,1,'2017-01-01',0),(98,1,'2017-05-28 21:16:28.071395',1,1,'2017-05-01',0),(99,2,'2017-05-30 21:33:58.489398',1,1,'2017-01-01',0),(100,2,'2017-05-30 21:34:40.956360',1,1,'2017-01-01',0),(101,2,'2017-06-06 07:14:26.261270',1,1,'2017-01-01',0),(102,2,'2017-07-14 17:19:38.379963',13,1,'2017-01-01',0),(103,2,'2017-07-18 01:32:08.899910',14,1,'2017-01-01',0),(104,2,'2017-07-18 19:28:45.383178',14,1,'2017-01-01',0),(105,2,'2017-07-18 19:32:43.988200',14,1,'2017-01-01',0),(106,2,'2017-07-18 19:35:06.775799',14,1,'2017-01-01',0),(107,2,'2017-07-18 19:39:21.342509',14,1,'2017-01-01',0),(108,2,'2017-11-27 05:51:12.717978',14,1,'2018-01-01',2),(109,2,'2017-11-27 05:58:34.236125',14,1,'2018-01-01',2),(110,2,'2017-11-27 06:12:20.970621',14,1,'2018-01-01',2),(111,2,'2017-12-01 16:11:03.772298',14,1,'2018-01-01',2),(112,2,'2017-12-13 14:32:01.423069',15,1,'2018-01-01',2),(113,2,'2018-01-17 05:06:22.706920',14,1,'2018-01-01',2);
/*!40000 ALTER TABLE `tblProject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblProjectPeriods`
--

DROP TABLE IF EXISTS `tblProjectPeriods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblProjectPeriods` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mineID` int(11) NOT NULL,
  `projectID` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  `dateAdded` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `projectID` (`projectID`),
  KEY `fk_tblProjectPeriods_mineID` (`mineID`),
  CONSTRAINT `tblprojectperiods_ibfk_1` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`) ON UPDATE CASCADE,
  CONSTRAINT `tblprojectperiods_ibfk_2` FOREIGN KEY (`projectID`) REFERENCES `tblProject` (`projectID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblProjectPeriods`
--

LOCK TABLES `tblProjectPeriods` WRITE;
/*!40000 ALTER TABLE `tblProjectPeriods` DISABLE KEYS */;
INSERT INTO `tblProjectPeriods` VALUES (1,2,94,1,'2017-05-01','2018-04-30','2017-05-13 06:14:28'),(2,2,94,2,'2018-05-01','2019-04-30','2017-05-13 06:14:28'),(3,2,95,1,'2017-05-01','2018-04-30','2017-05-13 06:20:52'),(4,2,95,2,'2018-05-01','2019-04-30','2017-05-13 06:20:52'),(5,1,96,1,'2017-01-01','2017-12-31','2017-05-24 21:30:04'),(6,1,96,2,'2018-01-01','2018-12-31','2017-05-24 21:30:04'),(7,1,97,1,'2017-01-01','2017-12-31','2017-05-24 21:53:27'),(8,1,97,2,'2018-01-01','2018-12-31','2017-05-24 21:53:27'),(9,1,98,1,'2017-05-01','2017-12-31','2017-05-28 21:16:28'),(10,1,98,2,'2018-01-01','2018-12-31','2017-05-28 21:16:28'),(11,1,99,1,'2017-01-01','2017-12-31','2017-05-30 21:33:58'),(12,1,99,2,'2018-01-01','2018-12-31','2017-05-30 21:33:58'),(13,1,100,1,'2017-01-01','2017-12-31','2017-05-30 21:34:41'),(14,1,100,2,'2018-01-01','2018-12-31','2017-05-30 21:34:41'),(15,1,101,1,'2017-01-01','2017-12-31','2017-06-06 07:14:26'),(16,1,101,2,'2018-01-01','2018-12-31','2017-06-06 07:14:26'),(17,13,102,1,'2017-01-01','2017-12-31','2017-07-14 17:19:38'),(18,13,102,2,'2018-01-01','2018-12-31','2017-07-14 17:19:38'),(19,14,103,1,'2017-01-01','2017-12-31','2017-07-18 01:32:09'),(20,14,103,2,'2018-01-01','2018-12-31','2017-07-18 01:32:09'),(21,14,104,1,'2017-01-01','2017-12-31','2017-07-18 19:28:45'),(22,14,104,2,'2018-01-01','2018-12-31','2017-07-18 19:28:45'),(23,14,105,1,'2017-01-01','2017-12-31','2017-07-18 19:32:44'),(24,14,105,2,'2018-01-01','2018-12-31','2017-07-18 19:32:44'),(25,14,106,1,'2017-01-01','2017-12-31','2017-07-18 19:35:07'),(26,14,106,2,'2018-01-01','2018-12-31','2017-07-18 19:35:07'),(27,14,107,1,'2017-01-01','2017-12-31','2017-07-18 19:39:21'),(28,14,107,2,'2018-01-01','2018-12-31','2017-07-18 19:39:21'),(29,14,108,1,'2018-01-01','2018-12-31','2017-11-27 05:51:13'),(30,14,108,2,'2019-01-01','2019-12-31','2017-11-27 05:51:13'),(31,14,109,1,'2018-01-01','2018-12-31','2017-11-27 05:58:34'),(32,14,109,2,'2019-01-01','2019-12-31','2017-11-27 05:58:34'),(33,14,110,1,'2018-01-01','2018-12-31','2017-11-27 06:12:21'),(34,14,110,2,'2019-01-01','2019-12-31','2017-11-27 06:12:21'),(35,14,111,1,'2018-01-01','2018-12-31','2017-12-01 16:11:04'),(36,14,111,2,'2019-01-01','2019-12-31','2017-12-01 16:11:04'),(37,15,112,1,'2018-01-01','2018-12-31','2017-12-13 14:32:01'),(38,15,112,2,'2019-01-01','2019-12-31','2017-12-13 14:32:01'),(39,14,113,1,'2018-01-01','2018-12-31','2018-01-17 05:06:23'),(40,14,113,2,'2019-01-01','2019-12-31','2018-01-17 05:06:23');
/*!40000 ALTER TABLE `tblProjectPeriods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblProjectTypeList`
--

DROP TABLE IF EXISTS `tblProjectTypeList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblProjectTypeList` (
  `projectTypeID` int(11) NOT NULL AUTO_INCREMENT,
  `projectType` varchar(10) NOT NULL,
  PRIMARY KEY (`projectTypeID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblProjectTypeList`
--

LOCK TABLES `tblProjectTypeList` WRITE;
/*!40000 ALTER TABLE `tblProjectTypeList` DISABLE KEYS */;
INSERT INTO `tblProjectTypeList` VALUES (1,'Study'),(2,'Operation');
/*!40000 ALTER TABLE `tblProjectTypeList` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblRevenue`
--

DROP TABLE IF EXISTS `tblRevenue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblRevenue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mineID` int(11) NOT NULL,
  `plantProductID` int(11) NOT NULL,
  `sellingPrice` float(20,2) DEFAULT NULL,
  `netPriceUSD` float(20,2) DEFAULT NULL,
  `netPriceCAD` float(20,2) DEFAULT NULL,
  `plantProductRevenue` float(20,2) DEFAULT NULL,
  `dateAdded` datetime NOT NULL,
  `date` date NOT NULL,
  `projectID` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `plantProductID` (`plantProductID`),
  KEY `fk_tblRevenue_mineID` (`mineID`),
  KEY `tblrevenue_ibfk_3` (`projectID`),
  CONSTRAINT `tblrevenue_ibfk_1` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`) ON UPDATE CASCADE,
  CONSTRAINT `tblrevenue_ibfk_2` FOREIGN KEY (`plantProductID`) REFERENCES `tblPlantProductList` (`plantProductID`) ON UPDATE CASCADE,
  CONSTRAINT `tblrevenue_ibfk_3` FOREIGN KEY (`projectID`) REFERENCES `tblProject` (`projectID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblRevenue`
--

LOCK TABLES `tblRevenue` WRITE;
/*!40000 ALTER TABLE `tblRevenue` DISABLE KEYS */;
INSERT INTO `tblRevenue` VALUES (43,1,1,113.12,97.49,121.86,725559.56,'2017-05-24 22:01:38','2017-05-01',97),(44,1,1,113.12,97.49,121.86,725559.56,'2017-05-24 22:02:09','2017-05-01',97),(45,1,2,93.51,77.88,97.35,1042787.88,'2017-05-24 22:02:09','2017-05-01',97),(46,1,1,113.12,97.49,121.86,725559.56,'2017-06-03 18:23:19','2017-05-01',100),(47,1,2,93.51,77.88,97.35,1042787.88,'2017-06-03 18:23:19','2017-05-01',100),(48,1,1,113.12,97.49,121.86,725559.56,'2017-06-03 18:23:53','2018-05-01',100),(49,1,2,93.51,77.88,97.35,1042787.88,'2017-06-03 18:23:53','2018-05-01',100),(50,1,1,113.46,97.83,122.29,156547.56,'2017-06-03 18:24:27','2018-06-01',100),(51,1,2,89.55,73.92,92.40,212810.59,'2017-06-03 18:24:27','2018-06-01',100),(52,1,1,103.30,87.67,109.59,112305.27,'2017-06-14 02:54:24','2017-05-01',101),(53,1,2,79.08,63.45,79.31,146230.44,'2017-06-14 02:54:24','2017-05-01',101),(54,1,1,97.86,82.23,102.79,131584.45,'2017-06-07 17:58:14','2018-05-01',101),(55,1,2,75.01,59.38,74.22,170950.94,'2017-06-07 17:58:14','2018-05-01',101),(56,14,1,-71.49,-72.54,-90.67,-2920.48,'2017-08-21 18:52:31','2017-05-01',107),(57,14,2,-71.49,-72.54,-90.67,-2920.48,'2017-08-21 18:52:31','2017-05-01',107),(58,15,1,115.45,99.82,124.77,136422.00,'2017-12-13 19:47:01','2018-01-15',112),(59,15,2,90.23,74.60,93.25,183426.77,'2017-12-13 19:47:01','2018-01-15',112),(60,15,1,115.54,99.91,124.89,132348.78,'2018-01-09 17:58:43','2018-01-01',112),(61,15,2,90.18,74.55,93.19,177670.64,'2018-01-09 17:58:43','2018-01-01',112),(62,14,1,115.63,100.00,125.00,132468.00,'2018-01-22 05:05:52','2018-01-01',113),(63,14,2,90.12,74.49,93.11,177527.64,'2018-01-22 05:05:52','2018-01-01',113),(64,14,1,113.36,97.73,122.16,157085.34,'2018-01-22 06:30:32','2018-01-02',113),(65,14,2,89.47,73.84,92.30,213528.80,'2018-01-22 06:30:32','2018-01-02',113);
/*!40000 ALTER TABLE `tblRevenue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblSmelterTerms`
--

DROP TABLE IF EXISTS `tblSmelterTerms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblSmelterTerms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mineID` int(11) NOT NULL,
  `commodityID` int(11) NOT NULL,
  `stockpileID` int(11) NOT NULL,
  `minGrade` float(20,2) DEFAULT NULL,
  `maxGrade` float(20,2) DEFAULT NULL,
  `minPenalty` float(20,2) DEFAULT NULL,
  `maxPenalty` float(20,2) DEFAULT NULL,
  `minMaxPenalty` float(20,2) DEFAULT NULL,
  `premium` float(20,2) DEFAULT NULL,
  `increments` float(20,2) DEFAULT NULL,
  `PFMinGrade` float(20,2) DEFAULT NULL,
  `dateAdded` datetime NOT NULL,
  `projectID` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `commodityID` (`commodityID`),
  KEY `fk_tblSmelterTerms_mineID` (`mineID`),
  KEY `tblsmelterterms_ibfk_3` (`projectID`),
  CONSTRAINT `tblsmelterterms_ibfk_1` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`) ON UPDATE CASCADE,
  CONSTRAINT `tblsmelterterms_ibfk_2` FOREIGN KEY (`commodityID`) REFERENCES `tblCommodityList` (`commodityID`) ON UPDATE CASCADE,
  CONSTRAINT `tblsmelterterms_ibfk_3` FOREIGN KEY (`projectID`) REFERENCES `tblProject` (`projectID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblSmelterTerms`
--

LOCK TABLES `tblSmelterTerms` WRITE;
/*!40000 ALTER TABLE `tblSmelterTerms` DISABLE KEYS */;
INSERT INTO `tblSmelterTerms` VALUES (1,15,22,1,60.00,62.00,3.00,0.00,1.50,1.50,1.00,NULL,'2017-12-13 14:32:01',112),(2,15,3,1,1.00,1.00,0.20,0.00,0.20,-0.20,1.00,NULL,'2017-12-13 14:32:01',112),(3,15,33,1,0.00,0.00,0.00,0.00,0.00,0.00,1.00,NULL,'2017-12-13 14:32:01',112),(4,15,50,1,4.50,4.50,0.75,0.00,0.75,-0.75,1.00,NULL,'2017-12-13 14:32:01',112),(5,15,22,2,56.00,58.00,4.00,1.50,2.00,0.00,1.00,NULL,'2017-12-13 14:32:01',112),(6,15,3,2,1.00,1.00,0.20,0.20,0.20,0.00,100.00,NULL,'2017-12-13 14:32:01',112),(7,15,33,2,0.00,0.00,0.00,0.00,0.00,0.00,1.00,NULL,'2017-12-13 14:32:01',112),(8,15,50,2,10.00,10.00,0.75,0.75,0.75,0.00,1.00,NULL,'2017-12-13 14:32:01',112),(9,14,22,1,60.00,62.00,3.00,0.00,1.50,1.50,1.00,NULL,'2018-01-17 05:06:23',113),(10,14,3,1,1.00,1.00,0.20,0.00,0.20,-0.20,1.00,NULL,'2018-01-17 05:06:23',113),(11,14,33,1,0.00,0.00,0.00,0.00,0.00,0.00,1.00,NULL,'2018-01-17 05:06:23',113),(12,14,50,1,4.50,4.50,0.75,0.00,0.75,-0.75,1.00,NULL,'2018-01-17 05:06:23',113),(13,14,22,2,56.00,58.00,4.00,1.50,2.00,0.00,1.00,NULL,'2018-01-17 05:06:23',113),(14,14,3,2,1.00,1.00,0.20,0.20,0.20,0.00,100.00,NULL,'2018-01-17 05:06:23',113),(15,14,33,2,0.00,0.00,0.00,0.00,0.00,0.00,1.00,NULL,'2018-01-17 05:06:23',113),(16,14,50,2,10.00,10.00,0.75,0.75,0.75,0.00,1.00,NULL,'2018-01-17 05:06:23',113);
/*!40000 ALTER TABLE `tblSmelterTerms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblSmelterTermsOptimized`
--

DROP TABLE IF EXISTS `tblSmelterTermsOptimized`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblSmelterTermsOptimized` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mineID` int(11) NOT NULL,
  `commodityID` int(11) NOT NULL,
  `plantProductID` int(11) NOT NULL,
  `penalty` float(20,2) DEFAULT NULL,
  `dateAdded` datetime NOT NULL,
  `optimized` tinyint(1) DEFAULT NULL,
  `projectID` int(11) NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `commodityID` (`commodityID`),
  KEY `plantProductID` (`plantProductID`),
  KEY `fk_tblSmelterTermsOptimized_mineID` (`mineID`),
  KEY `tblSmelterTermsOptimized_optimized` (`optimized`),
  KEY `tblsmeltertermsoptimized_ibfk_4` (`projectID`),
  CONSTRAINT `tblsmeltertermsoptimized_ibfk_1` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`) ON UPDATE CASCADE,
  CONSTRAINT `tblsmeltertermsoptimized_ibfk_2` FOREIGN KEY (`commodityID`) REFERENCES `tblCommodityList` (`commodityID`) ON UPDATE CASCADE,
  CONSTRAINT `tblsmeltertermsoptimized_ibfk_3` FOREIGN KEY (`plantProductID`) REFERENCES `tblPlantProductList` (`plantProductID`) ON UPDATE CASCADE,
  CONSTRAINT `tblsmeltertermsoptimized_ibfk_4` FOREIGN KEY (`projectID`) REFERENCES `tblProject` (`projectID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=225 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblSmelterTermsOptimized`
--

LOCK TABLES `tblSmelterTermsOptimized` WRITE;
/*!40000 ALTER TABLE `tblSmelterTermsOptimized` DISABLE KEYS */;
INSERT INTO `tblSmelterTermsOptimized` VALUES (129,1,22,1,2.49,'2017-05-24 22:01:38',1,97,'2017-05-01'),(130,1,22,2,6.68,'2017-05-24 22:01:38',1,97,'2017-05-01'),(131,1,3,1,0.00,'2017-05-24 22:01:38',1,97,'2017-05-01'),(132,1,3,2,0.00,'2017-05-24 22:01:38',1,97,'2017-05-01'),(133,1,33,1,0.00,'2017-05-24 22:01:38',1,97,'2017-05-01'),(134,1,33,2,0.00,'2017-05-24 22:01:38',1,97,'2017-05-01'),(135,1,50,1,-5.61,'2017-05-24 22:01:38',1,97,'2017-05-01'),(136,1,50,2,-5.19,'2017-05-24 22:01:38',1,97,'2017-05-01'),(137,1,22,1,2.49,'2017-05-24 22:02:09',1,97,'2017-05-01'),(138,1,22,2,6.68,'2017-05-24 22:02:09',1,97,'2017-05-01'),(139,1,3,1,0.00,'2017-05-24 22:02:09',1,97,'2017-05-01'),(140,1,3,2,0.00,'2017-05-24 22:02:09',1,97,'2017-05-01'),(141,1,33,1,0.00,'2017-05-24 22:02:09',1,97,'2017-05-01'),(142,1,33,2,0.00,'2017-05-24 22:02:09',1,97,'2017-05-01'),(143,1,50,1,-5.61,'2017-05-24 22:02:09',1,97,'2017-05-01'),(144,1,50,2,-5.19,'2017-05-24 22:02:09',1,97,'2017-05-01'),(145,1,22,1,2.49,'2017-06-03 18:23:19',1,100,'2017-05-01'),(146,1,22,2,6.68,'2017-06-03 18:23:19',1,100,'2017-05-01'),(147,1,3,1,0.00,'2017-06-03 18:23:19',1,100,'2017-05-01'),(148,1,3,2,0.00,'2017-06-03 18:23:19',1,100,'2017-05-01'),(149,1,33,1,0.00,'2017-06-03 18:23:19',1,100,'2017-05-01'),(150,1,33,2,0.00,'2017-06-03 18:23:19',1,100,'2017-05-01'),(151,1,50,1,-5.61,'2017-06-03 18:23:19',1,100,'2017-05-01'),(152,1,50,2,-5.19,'2017-06-03 18:23:19',1,100,'2017-05-01'),(153,1,22,1,2.49,'2017-06-03 18:23:53',1,100,'2018-05-01'),(154,1,22,2,6.68,'2017-06-03 18:23:53',1,100,'2018-05-01'),(155,1,3,1,0.00,'2017-06-03 18:23:53',1,100,'2018-05-01'),(156,1,3,2,0.00,'2017-06-03 18:23:53',1,100,'2018-05-01'),(157,1,33,1,0.00,'2017-06-03 18:23:53',1,100,'2018-05-01'),(158,1,33,2,0.00,'2017-06-03 18:23:53',1,100,'2018-05-01'),(159,1,50,1,-5.61,'2017-06-03 18:23:53',1,100,'2018-05-01'),(160,1,50,2,-5.19,'2017-06-03 18:23:53',1,100,'2018-05-01'),(161,1,22,1,4.34,'2017-06-03 18:24:27',1,100,'2018-06-01'),(162,1,22,2,12.72,'2017-06-03 18:24:27',1,100,'2018-06-01'),(163,1,3,1,0.00,'2017-06-03 18:24:27',1,100,'2018-06-01'),(164,1,3,2,0.00,'2017-06-03 18:24:27',1,100,'2018-06-01'),(165,1,33,1,0.00,'2017-06-03 18:24:27',1,100,'2018-06-01'),(166,1,33,2,0.00,'2017-06-03 18:24:27',1,100,'2018-06-01'),(167,1,50,1,-7.80,'2017-06-03 18:24:27',1,100,'2018-06-01'),(168,1,50,2,-7.27,'2017-06-03 18:24:27',1,100,'2018-06-01'),(169,1,22,1,0.61,'2017-06-14 02:54:24',0,101,'2017-05-01'),(170,1,22,2,10.28,'2017-06-14 02:54:24',0,101,'2017-05-01'),(171,1,3,1,0.00,'2017-06-14 02:54:24',0,101,'2017-05-01'),(172,1,3,2,0.00,'2017-06-14 02:54:24',0,101,'2017-05-01'),(173,1,33,1,0.03,'2017-06-14 02:54:24',0,101,'2017-05-01'),(174,1,33,2,0.02,'2017-06-14 02:54:24',0,101,'2017-05-01'),(175,1,50,1,6.06,'2017-06-14 02:54:24',0,101,'2017-05-01'),(176,1,50,2,5.62,'2017-06-14 02:54:24',0,101,'2017-05-01'),(177,1,22,1,4.34,'2017-06-07 17:58:14',1,101,'2018-05-01'),(178,1,22,2,12.72,'2017-06-07 17:58:14',1,101,'2018-05-01'),(179,1,3,1,0.00,'2017-06-07 17:58:14',1,101,'2018-05-01'),(180,1,3,2,0.00,'2017-06-07 17:58:14',1,101,'2018-05-01'),(181,1,33,1,0.00,'2017-06-07 17:58:14',1,101,'2018-05-01'),(182,1,33,2,0.00,'2017-06-07 17:58:14',1,101,'2018-05-01'),(183,1,50,1,7.80,'2017-06-07 17:58:14',1,101,'2018-05-01'),(184,1,50,2,7.27,'2017-06-07 17:58:14',1,101,'2018-05-01'),(185,14,22,1,60.25,'2017-08-21 18:52:31',0,107,'2017-05-01'),(186,14,22,2,60.25,'2017-08-21 18:52:31',0,107,'2017-05-01'),(187,14,3,1,0.41,'2017-08-21 18:52:31',0,107,'2017-05-01'),(188,14,3,2,0.41,'2017-08-21 18:52:31',0,107,'2017-05-01'),(189,14,33,1,0.04,'2017-08-21 18:52:31',0,107,'2017-05-01'),(190,14,33,2,0.04,'2017-08-21 18:52:31',0,107,'2017-05-01'),(191,14,50,1,11.84,'2017-08-21 18:52:31',0,107,'2017-05-01'),(192,14,50,2,11.84,'2017-08-21 18:52:31',0,107,'2017-05-01'),(193,15,22,1,0.58,'2017-12-13 19:47:01',1,112,'2018-01-15'),(194,15,22,2,10.34,'2017-12-13 19:47:01',1,112,'2018-01-15'),(195,15,3,1,0.06,'2017-12-13 19:47:01',1,112,'2018-01-15'),(196,15,3,2,0.07,'2017-12-13 19:47:01',1,112,'2018-01-15'),(197,15,33,1,0.00,'2017-12-13 19:47:01',1,112,'2018-01-15'),(198,15,33,2,0.00,'2017-12-13 19:47:01',1,112,'2018-01-15'),(199,15,50,1,-6.09,'2017-12-13 19:47:01',1,112,'2018-01-15'),(200,15,50,2,-5.64,'2017-12-13 19:47:01',1,112,'2018-01-15'),(201,15,22,1,0.53,'2018-01-09 17:58:43',0,112,'2018-01-01'),(202,15,22,2,10.43,'2018-01-09 17:58:43',0,112,'2018-01-01'),(203,15,3,1,0.06,'2018-01-09 17:58:43',0,112,'2018-01-01'),(204,15,3,2,0.07,'2018-01-09 17:58:43',0,112,'2018-01-01'),(205,15,33,1,0.00,'2018-01-09 17:58:43',0,112,'2018-01-01'),(206,15,33,2,0.00,'2018-01-09 17:58:43',0,112,'2018-01-01'),(207,15,50,1,-6.13,'2018-01-09 17:58:43',0,112,'2018-01-01'),(208,15,50,2,-5.68,'2018-01-09 17:58:43',0,112,'2018-01-01'),(209,14,22,1,0.48,'2018-01-22 05:05:52',1,113,'2018-01-01'),(210,14,22,2,10.53,'2018-01-22 05:05:52',1,113,'2018-01-01'),(211,14,3,1,0.06,'2018-01-22 05:05:52',1,113,'2018-01-01'),(212,14,3,2,0.07,'2018-01-22 05:05:52',1,113,'2018-01-01'),(213,14,33,1,0.00,'2018-01-22 05:05:52',1,113,'2018-01-01'),(214,14,33,2,0.00,'2018-01-22 05:05:52',1,113,'2018-01-01'),(215,14,50,1,-6.17,'2018-01-22 05:05:52',1,113,'2018-01-01'),(216,14,50,2,-5.72,'2018-01-22 05:05:52',1,113,'2018-01-01'),(217,14,22,1,4.36,'2018-01-22 06:30:32',1,113,'2018-01-02'),(218,14,22,2,12.73,'2018-01-22 06:30:32',1,113,'2018-01-02'),(219,14,3,1,0.08,'2018-01-22 06:30:32',1,113,'2018-01-02'),(220,14,3,2,0.08,'2018-01-22 06:30:32',1,113,'2018-01-02'),(221,14,33,1,0.00,'2018-01-22 06:30:32',1,113,'2018-01-02'),(222,14,33,2,0.00,'2018-01-22 06:30:32',1,113,'2018-01-02'),(223,14,50,1,-7.80,'2018-01-22 06:30:32',1,113,'2018-01-02'),(224,14,50,2,-7.28,'2018-01-22 06:30:32',1,113,'2018-01-02');
/*!40000 ALTER TABLE `tblSmelterTermsOptimized` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblTaxes`
--

DROP TABLE IF EXISTS `tblTaxes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblTaxes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mineID` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `federal` float(10,4) DEFAULT NULL,
  `provincial` float(10,4) DEFAULT NULL,
  `mining` float(10,4) DEFAULT NULL,
  `dateAdded` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_tblTaxes_mineID` (`mineID`),
  CONSTRAINT `tbltaxes_ibfk_1` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblTaxes`
--

LOCK TABLES `tblTaxes` WRITE;
/*!40000 ALTER TABLE `tblTaxes` DISABLE KEYS */;
INSERT INTO `tblTaxes` VALUES (1,1,1,0.1300,0.1300,0.1300,'2017-02-27 16:12:40'),(2,1,2,0.1300,0.1300,0.1300,'2017-02-27 16:12:40'),(3,1,1,0.1300,0.1300,0.1300,'2017-02-27 18:33:52'),(4,1,2,0.1300,0.1300,0.1300,'2017-02-27 18:33:52'),(5,1,1,0.1300,0.1300,0.1300,'2017-02-27 18:34:20'),(6,1,2,0.1300,0.1300,0.1300,'2017-02-27 18:34:20'),(7,1,1,0.1300,0.1300,0.1300,'2017-03-02 01:16:36'),(8,1,2,0.1300,0.1300,0.1300,'2017-03-02 01:16:36'),(9,1,1,0.1300,0.1300,0.1300,'2017-03-07 15:27:15'),(10,1,2,0.1300,0.1300,0.1300,'2017-03-07 15:27:15'),(11,1,1,0.1300,0.1300,0.1300,'2017-03-07 15:33:27'),(12,1,2,0.1300,0.1300,0.1300,'2017-03-07 15:33:27'),(13,1,1,0.1300,0.1300,0.1300,'2017-03-12 19:46:21'),(14,1,2,0.1300,0.1300,0.1300,'2017-03-12 19:46:21'),(15,1,1,0.1300,0.1300,0.1300,'2017-03-13 00:35:14'),(16,1,2,0.1300,0.1300,0.1300,'2017-03-13 00:35:14'),(17,1,1,0.1300,0.1300,0.1300,'2017-03-13 23:21:23'),(18,1,2,0.1300,0.1300,0.1300,'2017-03-13 23:21:23'),(19,1,1,0.8000,0.8000,0.8000,'2017-03-14 04:21:53'),(20,1,2,0.8000,0.8000,0.8000,'2017-03-14 04:21:53'),(21,1,1,0.1300,0.1300,0.1300,'2017-03-14 22:36:59'),(22,1,2,0.1300,0.1300,0.1300,'2017-03-14 22:36:59'),(23,1,1,13.0000,13.0000,13.0000,'2017-03-21 22:48:08'),(24,1,2,13.0000,13.0000,13.0000,'2017-03-21 22:48:08'),(25,1,1,13.0000,13.0000,13.0000,'2017-03-23 05:57:27'),(26,1,2,13.0000,13.0000,13.0000,'2017-03-23 05:57:27'),(27,1,1,13.0000,13.0000,13.0000,'2017-03-26 22:50:38'),(28,1,2,13.0000,13.0000,13.0000,'2017-03-26 22:50:38'),(29,1,1,13.0000,13.0000,13.0000,'2017-04-07 16:38:08'),(30,1,1,13.0000,13.0000,13.0000,'2017-04-07 16:43:47'),(31,1,1,13.0000,13.0000,13.0000,'2017-04-07 17:02:53'),(32,1,1,13.0000,13.0000,13.0000,'2017-04-07 19:21:42'),(33,1,1,0.0000,0.0000,0.0000,'2017-04-11 16:54:59'),(34,1,1,0.0000,0.0000,0.0000,'2017-04-13 21:17:46'),(35,1,1,13.0000,13.0000,13.0000,'2017-04-22 17:04:05'),(36,1,1,0.0000,0.0000,0.0000,'2017-04-26 15:03:48'),(37,2,1,0.0000,0.0000,0.0000,'2017-05-12 04:49:47'),(38,2,2,0.0000,0.0000,0.0000,'2017-05-12 04:49:47'),(39,2,1,0.0000,0.0000,0.0000,'2017-05-13 17:26:06'),(40,2,2,0.0000,0.0000,0.0000,'2017-05-13 17:26:06'),(41,1,1,0.0000,0.0000,0.0000,'2017-05-24 21:35:27'),(42,1,2,0.0000,0.0000,0.0000,'2017-05-24 21:35:27'),(43,1,1,0.0000,0.0000,0.0000,'2017-05-24 21:58:37'),(44,1,2,0.0000,0.0000,0.0000,'2017-05-24 21:58:37'),(45,1,1,0.0000,0.0000,0.0000,'2017-05-28 21:33:42'),(46,1,2,0.0000,0.0000,0.0000,'2017-05-28 21:33:42'),(47,1,1,0.0000,0.0000,0.0000,'2017-05-28 21:35:23'),(48,1,2,0.0000,0.0000,0.0000,'2017-05-28 21:35:23'),(49,1,1,0.0000,0.0000,0.0000,'2017-05-30 22:42:49'),(50,1,2,0.0000,0.0000,0.0000,'2017-05-30 22:42:49'),(51,1,1,0.0000,0.0000,0.0000,'2017-06-06 07:44:57'),(52,1,2,0.0000,0.0000,0.0000,'2017-06-06 07:44:57'),(53,13,1,1.0500,1.0500,1.0500,'2017-07-14 17:19:38'),(54,13,2,1.0500,1.0500,1.0500,'2017-07-14 17:19:38'),(55,14,1,1.0500,1.0500,1.0500,'2017-07-18 01:32:09'),(56,14,2,1.0500,1.0500,1.0500,'2017-07-18 01:32:09'),(57,14,1,1.0500,1.0500,1.0500,'2017-07-18 19:39:21'),(58,14,2,1.0500,1.0500,1.0500,'2017-07-18 19:39:21'),(59,14,1,13.0000,13.0000,13.0000,'2017-11-27 06:12:21'),(60,14,2,13.0000,13.0000,13.0000,'2017-11-27 06:12:21'),(61,14,1,1.0500,1.0500,1.0500,'2017-12-01 16:11:04'),(62,14,2,1.0500,1.0500,1.0500,'2017-12-01 16:11:04'),(63,15,1,0.0000,0.0000,0.0000,'2017-12-13 14:32:01'),(64,15,2,0.0000,0.0000,0.0000,'2017-12-13 14:32:01'),(65,14,1,0.0000,0.0000,0.0000,'2018-01-17 05:06:23'),(66,14,2,0.0000,0.0000,0.0000,'2018-01-17 05:06:23');
/*!40000 ALTER TABLE `tblTaxes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblUsers`
--

DROP TABLE IF EXISTS `tblUsers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblUsers` (
  `userID` int(11) NOT NULL AUTO_INCREMENT,
  `mineID` int(11) NOT NULL,
  `companyID` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `firstName` varchar(50) DEFAULT NULL,
  `lastName` varchar(50) DEFAULT NULL,
  `company` varchar(250) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(32) DEFAULT NULL,
  `jobTitle` varchar(50) DEFAULT NULL,
  `userRole` int(11) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL,
  `lastLogin` datetime DEFAULT NULL,
  `dateAdded` datetime DEFAULT NULL,
  `reset` varchar(6) DEFAULT NULL,
  `resetExpiry` datetime DEFAULT NULL,
  PRIMARY KEY (`userID`),
  KEY `mineID` (`mineID`),
  KEY `companyID` (`companyID`),
  CONSTRAINT `tblusers_ibfk_1` FOREIGN KEY (`mineID`) REFERENCES `tblMine` (`mineID`) ON UPDATE CASCADE,
  CONSTRAINT `tblusers_ibfk_2` FOREIGN KEY (`companyID`) REFERENCES `tblCompany` (`companyID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblUsers`
--

LOCK TABLES `tblUsers` WRITE;
/*!40000 ALTER TABLE `tblUsers` DISABLE KEYS */;
INSERT INTO `tblUsers` VALUES (1,1,10,'kristafung','Krista','Fung',NULL,'kristafung@hotmail.com','6479978827','Owner',1,'1Wertyui','2017-09-08 19:47:17','2017-02-26 15:58:12','jqM6FT','2017-08-25 19:22:56'),(2,2,11,'abc','abc','abc',NULL,'abc','abc','abc',1,'abc','2017-05-11 20:10:08','2017-04-07 22:30:43',NULL,NULL),(3,6,15,'la','la','la',NULL,'la','la','la',1,'la',NULL,'2017-04-13 15:59:07',NULL,NULL),(4,7,16,'bb','bb','bb',NULL,'bb','bb','bb',1,'bb','2017-04-13 16:02:34','2017-04-13 16:00:32',NULL,NULL),(5,9,19,'test2','test2','test2',NULL,'test2@gmail.com','1234566','test',1,'abcde',NULL,'2017-04-20 15:33:01',NULL,NULL),(6,11,21,'12','12','12',NULL,'12','12','12',1,'12',NULL,'2017-04-20 15:42:51',NULL,NULL),(7,12,22,'a1','a1','a1',NULL,'a1','a1','a1',1,'a1','2017-07-07 17:44:22','2017-07-07 16:34:50',NULL,NULL),(8,13,23,'b1','b1','b1',NULL,'b1','b1','b1',1,'b1','2017-07-07 20:51:28','2017-07-07 18:09:23',NULL,NULL),(9,14,24,'cc','cc','cc',NULL,'cc','cc','cc',1,'cc','2018-01-22 18:23:53','2017-07-15 18:55:36',NULL,NULL),(10,15,25,'wes','wes','wes',NULL,'wesleycmtsang@gmail.com','wes','wes',1,'s680gc76ft','2017-12-30 21:07:06','2017-08-22 19:24:09','CQLroL','2017-08-25 22:27:01');
/*!40000 ALTER TABLE `tblUsers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-01-24 18:02:47
