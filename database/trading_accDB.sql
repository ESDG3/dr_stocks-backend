CREATE DATABASE IF NOT EXISTS `trading_accDB` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `trading_accDB`;

# TRADING_ACCDB
DROP TABLE IF EXISTS `trading_acc`;
CREATE TABLE IF NOT EXISTS `trading_acc` (
  `Trade_AccID` INT NOT NULL AUTO_INCREMENT,
  `AccID` INT NOT NULL,
  `Trade_Acc_Balance` DECIMAL(13, 2) NOT NULL,
  PRIMARY KEY (`Trade_AccID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO `trading_acc` (`Trade_AccID`, `AccID`, `Trade_Acc_Balance`) VALUES
('4000001', '1000001', '1000.00'),
('4000002', '1000002', '500.00');
COMMIT;

--select * from trading_accDB.trading_acc;