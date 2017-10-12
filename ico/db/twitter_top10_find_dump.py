#!/usr/bin/python3
import pymysql
import json
from subprocess import call
import os
import fileinput
import tweepy 
import csv	

# db
db = pymysql.connect("localhost","test","test","ico")
cursor = db.cursor()

#Twitter API credentials
consumer_key            = " "
consumer_secret         = " "
access_key            = " - "
access_secret     = " "

#grab up to 3240 tweets per account

#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# get new in the past 30 min
get_top_rt = """select distinct count(*) as cnt, text from twitter.tweets where text like 'rt %' and (tweet_at > date_sub(utc_timestamp(), interval 2 hour)) group by text order by cnt desc limit 1;"""
cursor.execute(get_top_rt)
top_rt = cursor.fetchall()
top_list = []
for rt in top_rt:
    team = "@" + (str(rt).split(':')[0].split('@')[1])
    top_list.append(team) 
print(top_list)

for screen_name in top_list:
    alltweets = []	
    user_data = api.get_user(screen_name)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        print("...%s tweets downloaded so far" % (len(alltweets)))

        for tweet in alltweets:
            cursor.execute("INSERT IGNORE INTO twitter.tweets (screen_name, tweet_at, born, urls,symbols,description,username,text,followers,friends,source, location, tweet_id, user_mentions) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(tweet.user.screen_name, tweet.created_at, user_data.created_at, str(tweet.entities['urls']).encode("utf-8","ignore"),str(tweet.entities['symbols']).encode("utf-8","ignore"), user_data.description, user_data.screen_name, tweet.text.encode("utf-8"), user_data.followers_count, user_data.friends_count,tweet.source, user_data.location, tweet.id,str(tweet.entities['user_mentions']).encode("utf-8","ignore")))
    db.commit()
db.close()
