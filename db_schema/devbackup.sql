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
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=312 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=110 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=209 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-01-09 14:50:04
