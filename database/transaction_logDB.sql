CREATE DATABASE IF NOT EXISTS `transaction_logDB` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `transaction_logDB`;

# TRANSACTION_LOGDB
DROP TABLE IF EXISTS `transaction_log`;
CREATE TABLE IF NOT EXISTS `transaction_log` (
  `TransactionID` INT NOT NULL AUTO_INCREMENT,
  `AccID` INT NOT NULL,
  `Trade_AccID` INT NOT NULL,
  `Transaction_Action` VARCHAR(20) NOT NULL,
  `Transaction_Value` DECIMAL(13, 2) NOT NULL,
  `Transaction_Date` DATETIME NOT NULL,
  PRIMARY KEY (`TransactionID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;