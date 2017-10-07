#!/usr/bin/python3
import pymysql
import json
from subprocess import call
import os
import fileinput

# db
db = pymysql.connect("localhost","test","test","ico")
cursor = db.cursor()	

# only new - no btc/eth/$$$$ - don't want them in the filters
select_sql = """SELECT lower(symbol) FROM ico.coins where (
symbol not like '300' and symbol  not like '$$$' and symbol not like 'btc' and symbol not like 'ltc' and 
symbol not like 'eth' and new = 1);"""
cursor.execute(select_sql)
results = cursor.fetchall()

# Make list of coins in the db
known_coins = []
for row in results:
    coin = "$" + row[0] + " "
    known_coins.append(coin)

# Remove duplicates
uniq_list = set(known_coins)
known_coins = (uniq_list)
print(len(uniq_list))

select_sql = "select distinct count(*) as cnt, text from twitter.tweets where text like 'rt %' and (tweet_at > date_sub(utc_timestamp(), interval 24 hour)) group by text order by cnt desc limit 10;"
cursor.execute(select_sql)
tweets = cursor.fetchall()
for item in tweets:
    print(item)
        #cursor.execute("INSERT INTO ico.stats (symbol,tweet_at) VALUES (%s,%s)", (coin, tweet_at))
    #db.commit()
db.close()