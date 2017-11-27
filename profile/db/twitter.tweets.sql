CREATE DATABASE twitter 
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

CREATE TABLE twitter.tweets (
tweet_id bigint(20) NOT NULL PRIMARY KEY,
screen_name varchar(24),
tweet_at datetime,
born datetime,
urls varchar(2048),
symbols varchar(2048),
description varchar(320),
username varchar(32),
text varchar(320),
followers bigint(20),
friends bigint(20),
source varchar(48),
location varchar(128),
statuses_count bigint(20),
time_zone varchar(48),
utc_offset varchar(24),
user_id bigint(20),
verified bool,
in_reply_to_screen_name varchar(512),
in_reply_to_status_id bigint(20),
in_reply_to_user_id bigint(20),
user_mentions varchar(2048),
logged datetime);
