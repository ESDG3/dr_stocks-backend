CREATE DATABASE IF NOT EXISTS `user_stockDB` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `user_stockDB`;

# USER_STOCKDB
DROP TABLE IF EXISTS `user_stock`;
CREATE TABLE IF NOT EXISTS `user_stock` (
  `User_StockID` INT NOT NULL AUTO_INCREMENT,
  `AccID` INT NOT NULL,
  `TradeID` INT NOT NULL,
  `Stock_Symbol` CHAR(5) NOT NULL,
  `Stock_Quantity` INT NOT NULL,
  `Purchased_Price` DECIMAL(13, 2) NOT NULL,
  `Currency` CHAR(3) NOT NULL,
  PRIMARY KEY (`User_StockID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `user_stock` (`User_StockID`, `AccID`, `TradeID`,`Stock_Symbol`, `Stock_Quantity`, `Purchased_Price`, `Currency`) VALUES
('5000001', '1000001', '6000001','AAPL', '1', '154.73', 'USD'),
('5000002', '1000002', '6000002','AMD', '1', '104.29', 'USD');
COMMIT;

select * from user_stockDB.user_stock;