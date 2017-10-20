#!/usr/bin/python3
import pymysql
import json
import tweepy #https://github.com/tweepy/tweepy
import time
#Twitter API credentials
consumer_key            = " "
consumer_secret         = " "
access_key            = " - "
access_secret     = " "

#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# db
db = pymysql.connect("localhost","test","test","ico")
cursor = db.cursor()	

# only new - no btc/eth/$$$$ - don't want them in the filters
select_sql = """SELECT trim(upper(symbol)) FROM ico.coins where (
symbol not like '300' and symbol  not like '$$$' and symbol not like 'btc' and symbol not like 'ltc' and 
symbol not like 'eth' and symbol not like '0x%' and new = 1 and active = 0);"""
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

add_list = list(uniq_list)
print(add_list)
text = []
add = []
rem = []
for symbol in add_list:
    max_tweets = 5
    tweets = tweepy.Cursor(api.search, q=symbol).items(max_tweets)
    time.sleep(15)
    for tweet in tweets:
        print(symbol)
        print(tweet.text)
        if symbol in tweet.text:
            add.append(symbol)
        else:
            rem.append(symbol)
    if (symbol in add and symbol not in rem) or (symbol in add and symbol in rem):
        print(symbol)
        symbol = str(symbol).replace("$","").strip()
        update = ("update ico.coins set active = 1 where symbol like '%s" % symbol + "';")
        print(update)
        cursor.execute(update)
    else:
        print(symbol)
    db.commit()
db.close()    