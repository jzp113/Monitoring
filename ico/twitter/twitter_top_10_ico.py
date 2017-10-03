#!/usr/bin python
# -*- coding: utf-8 -*-
import pymysql
import pandas as pd
from pandasql import sqldf
import MySQLdb

# db
db = pymysql.connect("localhost","test","test","ico")
cursor = db.cursor()	

select_coins = "SELECT lower(symbol) FROM ico.coins where (symbol  not like '300' and symbol  not like '$$$' and symbol not like 'btc' and symbol not like 'ltc' and symbol not like 'eth');"
cursor.execute(select_coins)
coins = cursor.fetchall()

# Make list of coins in the db
known_coins = []
for row in coins:
    coin = "$" + row[0] + " "
    known_coins.append(coin)

# Remove duplicates
uniq_list = set(known_coins)
coins = (uniq_list)

select_tweets = "SELECT lower(text) FROM twitter.tweets where (tweet_at > date_sub(utc_timestamp(), interval 1 hour));"
cursor.execute(select_tweets)
tweets = cursor.fetchall()

for coin in coins:
    for tweet in tweets:
        if str(coin) in str(tweet):
            print(coin)