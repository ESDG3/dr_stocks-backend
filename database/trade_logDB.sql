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
  `Currency` CHAR(3) NOT NULL,
  `Trade_Action` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`TradeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `trade_log` (`TradeID`, `AccID`, `Trade_Date`,`Trade_Value`, `Trade_Stock_Symbol`, `Trade_Quantity`, `Currency`, `Trade_Action`) VALUES
('6000001', '1000001', '2022-03-10 13:44:02','154.73', 'AAPL', '1', 'USD', 'BUY'),
('6000002', '1000002', '2022-03-10 15:43:27','104.29', 'AMD', '1', 'USD', 'BUY');
COMMIT;

select * from trade_logDB.trade_log;