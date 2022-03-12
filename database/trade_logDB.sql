CREATE DATABASE IF NOT EXISTS `trade_logDB` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `trade_logDB`;

# TRADE_LOGEB
DROP TABLE IF EXISTS `trade_log`;
CREATE TABLE IF NOT EXISTS `trade_log` (
  `TradeID` INT NOT NULL AUTO_INCREMENT,
  `AccID` INT NOT NULL,
  `Trade_Date` DATETIME NOT NULL,
  `Trade_Value` DECIMAL(13, 2) NOT NULL,
  `Trade_Stock_Symbol` CHAR(5) NOT NULL,
  `Trade_Quantity` INT NOT NULL,
  PRIMARY KEY (`TradeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;