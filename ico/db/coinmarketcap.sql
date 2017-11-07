CREATE TABLE ico.ticker (
id varchar(128) NOT NULL PRIMARY KEY,
name varchar(128),
symbol varchar(10),
rank int,
price_usd decimal(19,4),
price_btc decimal(19,8),
24h_volume_usd bigint(20),
market_cap_usd bigint(20),
available_supply bigint(20),
total_supply bigint(20),
percent_change_1h decimal(5,2),
percent_change_24h decimal(5,2),
percent_change_7d decimal(5,2),
last_updated bigint(20));
