CREATE TABLE  coins (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,  
marketcurrency VARCHAR(6), 
basecurrency VARCHAR(6), 
name VARCHAR(32), 
created datetime,  
isactive VARCHAR(10),  
exchange VARCHAR(16), 
discovered datetime);

