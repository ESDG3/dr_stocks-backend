CREATE DATABASE IF NOT EXISTS `stock_prefDB` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `stock_prefDB`;

# STOCK_PREFDB
DROP TABLE IF EXISTS `stock_pref`;
CREATE TABLE IF NOT EXISTS `stock_pref` (
  `Stock_PrefID` INT NOT NULL AUTO_INCREMENT,
  `AccID` INT NOT NULL,
  `Stock_Industry` CHAR(100) NOT NULL,
  PRIMARY KEY (`Stock_PrefID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `stock_pref` (`Stock_PrefID`, `AccID`, `Stock_Industry`) VALUES
('3000001', '1000001', 'Energy'),
('3000002', '1000001', 'Information Technology'),
('3000003', '1000001', 'Financials'),
('3000004', '1000002', 'Real Estate'),
('3000005', '1000002', 'Materials');
COMMIT;

select * from stock_prefDB.stock_pref;