CREATE DATABASE IF NOT EXISTS `userDB` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `userDB`;

# USERDB
DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `accid` INT NOT NULL AUTO_INCREMENT,
  `trade_accid` INT NOT NULL,
  `name` CHAR(100) NOT NULL,
  `birthdate` DATE NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`accid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `user` (`accid`, `trade_accid`, `name`, `birthdate`, `email`, `password`) VALUES
('1000001', '4000001', 'John Mark', '1992-06-15', 'johnmark@gmail.com','temp'),
('1000002', '4000002', 'Mary Esther', '1994-12-03', 'maryesther@gmail.com','temp1');
COMMIT;

select * from userDB.user;