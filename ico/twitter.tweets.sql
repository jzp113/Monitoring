CREATE TABLE twitter.tweets (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,  
name VARCHAR(24),  
description varchar(128), 
profurl VARCHAR(36), 
followers bigint(20),
friends bigint(20),
source varchar(48),
location varchar(48),
screen_name varchar(512),
tweet_id bigint(20),
tweet_at datetime,
born datetime,
text varchar(240));
