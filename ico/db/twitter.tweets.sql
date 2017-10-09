CREATE DATABASE twitter 
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;


CREATE TABLE twitter.tweets (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,  
screen_name varchar(24),
tweet_at datetime,
born datetime,
urls varchar(1024),
symbols varchar(256),
description varchar(320),
username varchar(32),
text varchar(320),
favorite_count bigint(20),
favorited bool,
followers bigint(20),
friends bigint(20),
source varchar(48),
location varchar(48),
tweet_id bigint(20),
statuses_count bigint(20),
time_zone varchar(48),
utc_offset varchar(24),
user_id bigint(20),
in_reply_to_screen_name varchar(512),
in_reply_to_status_id bigint(20),
in_reply_to_user_id bigint(20),
retweet_count bigint(20),
retweeted bigint(20));
