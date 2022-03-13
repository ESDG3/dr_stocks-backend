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
  `Currency` CHAR(3) NOT NULL,
  PRIMARY KEY (`TransactionID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `transaction_log` (`TransactionID`, `AccID`, `Trade_AccID`,`Transaction_Action`, `Transaction_Value`, `Transaction_Date`, `Currency`) VALUES
('7000001', '1000001', '4000001','DEPOSIT', '1000.00', '2022-03-08 10:34:22', 'USD'),
('7000002', '1000002', '4000002','DEPOSIT', '500.00', '2022-03-08 09:04:52', 'USD');
COMMIT;

select * from transaction_logDB.transaction_log;
