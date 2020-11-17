CREATE TABLE Packets (
  ID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  Date Date DEFAULT CURRENT_TIMESTAMP,
  Source_Ip varchar(100) NOT NULL,
  Dest_Ip varchar(100) NOT NULL,
  Source_MAC varchar(100) NOT NULL,
  Method varchar(50) NOT NULL,
  Port int NOT NULL,
  Path varchar(10000),
  Origin varchar(255)
);