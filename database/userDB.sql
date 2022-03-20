CREATE DATABASE IF NOT EXISTS `userDB` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `userDB`;

# USERDB
DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `AccID` INT NOT NULL AUTO_INCREMENT,
  `Trad_AccID` INT NOT NULL,
  `Name` CHAR(100) NOT NULL,
  `Birthdate` DATE NOT NULL,
  `Email` VARCHAR(100) NOT NULL,
  `Password` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`AccID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `user` (`AccID`, `Trad_AccID`, `Name`, `Birthdate`, `Email`, `Password`) VALUES
('1000001', '2000001', 'John Mark', '1992-06-15', 'johnmark@gmail.com','temp'),
('1000002', '2000002', 'Mary Esther', '1994-12-03', 'maryesther@gmail.com','temp1');
COMMIT;

select * from userDB.user;