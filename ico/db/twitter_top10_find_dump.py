#!/usr/bin/python3
import pymysql
import json
from subprocess import call
import os
import fileinput
import tweepy 
import csv	
import datetime
import time

# db
db = pymysql.connect("localhost","test","test","ico")
cursor = db.cursor()

#Twitter API credentials
consumer_key            = ""
consumer_secret         = ""
access_key            = ""
access_secret     = ""


#grab up to 3248 tweets per account
#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# get new in the past 10 min
get_top_rt = """select count(*) as cnt, text from twitter.tweets where text like 'rt %' and (tweet_at > date_sub(utc_timestamp(), interval 5 minute)) group by text order by cnt desc limit 3;"""
cursor.execute(get_top_rt)
top_rt = cursor.fetchall()
top_list = []
for rt in top_rt:
    team = "@" + (str(rt).split(':')[0].split('@')[1])
    top_list.append(team) 
#    print(team)
#print(top_list)
top_list = ['eLTC_Network']
for screen_name in top_list:
    alltweets = []	
    user_data = api.get_user(screen_name)
    time.sleep(5)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        time.sleep(5)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        print("...%s tweets downloaded so far" % (len(alltweets)))

        for tweet in alltweets:
            print(screen_name)
            cursor.execute("REPLACE INTO twitter.tweets (tweet_id, screen_name, tweet_at, born, urls,symbols,description,text,followers,friends,source, location,statuses_count, time_zone, utc_offset, user_id, verified,in_reply_to_screen_name,in_reply_to_status_id,in_reply_to_user_id,logged) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(tweet.id,str(tweet.user.screen_name), tweet.created_at, user_data.created_at, str(tweet.entities['urls']).encode("ascii","ignore"),str(tweet.entities['symbols']).encode("ascii","ignore"), str(user_data.description).encode("ascii","ignore"),tweet.text.encode("utf-8"), user_data.followers_count, user_data.friends_count,tweet.source,user_data.location, str(user_data.statuses_count), user_data.time_zone, user_data.utc_offset, user_data.id, user_data.verified, tweet.in_reply_to_screen_name, tweet.in_reply_to_status_id, tweet.in_reply_to_user_id, datetime.datetime.now()))
            
            #cursor.execute("select screen_name from twitter.tweets limit 10;")
        db.commit()
    
    # get newest 3 tweets from ico team
    #print('commit')
    name = "%" + screen_name.replace("@","") + "%"
    get_first_tweets = "select tweet_id from twitter.tweets where screen_name like '" + name + "'  order by tweet_at desc limit 3;"
    
    print('----------------------------------')
    print(name)
    cursor.execute(get_first_tweets)
    first_retweets = cursor.fetchall() 
    first_tweets_list = []
    for fp in first_retweets:
        first_tweets_list.append(str(fp).replace(",","").replace("(","").replace(")",""))
    
    for first_tweet in first_tweets_list:
        target_user_data = api.get_user(screen_name)
        retweeter_ids = api.retweeters(first_tweet)
        time.sleep(5)
        if len(retweeter_ids) > 0:
            retweeters_list = api.lookup_users(user_ids=retweeter_ids)
            
            for retweeter in retweeters_list:
                target_alltweets = []	
                print("retweeter is: " + retweeter.screen_name)
                target_user_data = api.get_user(retweeter.screen_name)
                target_new_tweets = api.user_timeline(screen_name = retweeter.screen_name,count=200)
                time.sleep(5)
                target_alltweets.extend(target_new_tweets)
                target_oldest = target_alltweets[-1].id - 1
            
                while len(target_new_tweets) > 0:
                    print("getting tweets before %s" % (target_oldest))
                    target_new_tweets = api.user_timeline(screen_name = retweeter.screen_name,count=200,max_id=target_oldest)
                    time.sleep(5)
                    target_alltweets.extend(target_new_tweets)
                    target_oldest = target_alltweets[-1].id - 1
                    print("...%s tweets downloaded so far" % (len(target_alltweets)))
                    print("secondary")
                    for target_tweet in target_alltweets:  
                        cursor.execute("REPLACE INTO twitter.tweets (tweet_id, screen_name, tweet_at, born, urls,symbols,description,text,followers,friends,source, location,statuses_count, time_zone, utc_offset, user_id, verified,in_reply_to_screen_name,in_reply_to_status_id,in_reply_to_user_id,logged) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(target_tweet.id,str(target_tweet.user.screen_name), target_tweet.created_at, user_data.created_at, str(target_tweet.entities['urls']).encode("ascii","ignore"),str(target_tweet.entities['symbols']).encode("ascii","ignore"), str(user_data.description).encode("ascii","ignore"),target_tweet.text.encode("utf-8"), user_data.followers_count, user_data.friends_count,target_tweet.source,user_data.location, str(user_data.statuses_count), user_data.time_zone, user_data.utc_offset, user_data.id, user_data.verified, target_tweet.in_reply_to_screen_name, target_tweet.in_reply_to_status_id, target_tweet.in_reply_to_user_id, datetime.datetime.now()))

                    db.commit()
db.close()
