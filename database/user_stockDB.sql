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