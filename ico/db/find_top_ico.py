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
db = pymysql.connect("localhost","test","test","ico",charset="utf8mb4",init_command='SET NAMES utf8mb4')
cursor = db.cursor()

#Twitter API credentials
consumer_key            = " "
consumer_secret         = " "
access_key            = " - "
access_secret     = " "


#grab up to 3248 tweets per account
#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# get top ico accounts based on 24 hr retweet counts
get_top_rt = """select count(*) as cnt, lower(substring_index(text,':',1)) from twitter.tweets where (text not like '%heliumpay%' and text not like '%centra_card%' and text not like '%voisecom%' and text not like '%stocktwit%') and text like 'rt %' and (tweet_at > date_sub(utc_timestamp(), interval 24 hour)) group by text order by cnt desc limit 25;"""
cursor.execute(get_top_rt)
top_rt = cursor.fetchall()


# Make list of top 10-20 unique screen_names
top_teams = []
for row in top_rt:
    team = (str(row).split(",")[1].replace("rt @","").replace(")","").replace("'","").strip())
    top_teams.append(team)
top_list = sorted(set(top_teams))

# Log up ~3200 tweets per screen_name
#top_list = ['ViulyOfficial']
#top_list = ['dashpay', 'ethereumproject', 'Ripple', 'litecoin', 'NEMofficial', 'monerocurrency', 'bitconnect', 'NeosCoin', 'IoTa2016', 'EthereumClassic', 'eth_classic', 'BITCOlNCASH', 'vitalikbuterin']
for screen_name in top_list:
    print("xxxxxxxxxxxxxxxx")
    print(screen_name)
    print("xxxxxxxxxxxxxxxx")
    alltweets = []	
    user_data = api.get_user(screen_name)
    time.sleep(3)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    #print(new_tweets)
    oldest = alltweets[-1].id - 1

    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        time.sleep(3)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        print("...%s tweets downloaded so far" % (len(alltweets)))
        for tweet in alltweets:
            #print(tweet)
            # replace into to get new  ico account statuses as available
            cursor.execute("replace INTO twitter.tweets (tweet_id, screen_name, tweet_at, born, urls,symbols,description,text,followers,friends,source, location,statuses_count, time_zone, utc_offset, user_id, verified,logged) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(tweet.id,str(tweet.user.screen_name).encode("utf8","ignore"), tweet.created_at, user_data.created_at, str(tweet.entities['urls']).encode("utf8","ignore"),str(tweet.entities['symbols']).encode("utf8","ignore"), str(user_data.description).encode("utf8","ignore"),tweet.text.encode("utf-8"), user_data.followers_count, user_data.friends_count,tweet.source,user_data.location, str(user_data.statuses_count), user_data.time_zone, user_data.utc_offset, user_data.id, user_data.verified, datetime.datetime.now()))
        db.commit()
    
    # get newest 3 tweet_id from ico team can be higher, n * 100 retweeters * 3200 tweets each will be logged 
    name = "%" + screen_name.replace("@","") + "%"
    get_first_tweets = "select tweet_id from twitter.tweets where lower(text) not like 'rt @%' and screen_name like '" + name + "'  order by tweet_id desc limit 5;"
    print(name)
    cursor.execute(get_first_tweets)
    first_retweets = cursor.fetchall() 
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")    
    print(first_retweets)
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")    
    first_tweets_list = []
    for fp in first_retweets:
        first_tweets_list.append(str(fp).replace(",","").replace("(","").replace(")",""))
        
    # get 100 retweeter screen_names as per api this is the max but should be able to crawl this tweet/group weekly/regularly to obtain new retweeters
    for first_tweet in first_tweets_list:
        target_user_data = api.get_user(screen_name)
        retweeter_ids = api.retweeters(first_tweet)
        time.sleep(3)
        if len(retweeter_ids) > 0:
            retweeters_list = api.lookup_users(user_ids=retweeter_ids)
            #retweeters_list = ['xxx']
            # log up to 3200 of each of the 100 retweeters tweets
            for retweeter in retweeters_list:
                target_alltweets = []
                print("xxxxxxxxxxxxxxxx")
                print(screen_name)
                print("xxxxxxxxxxxxxxxx")                
                print("retweeter is: " + retweeter.screen_name)
                target_user_data = api.get_user(retweeter.screen_name)
                target_new_tweets = api.user_timeline(screen_name = retweeter.screen_name,count=200)
                time.sleep(3)
                target_alltweets.extend(target_new_tweets)
                target_oldest = target_alltweets[-1].id - 1
            
                while len(target_new_tweets) > 0:
                    print("xxxxxxxxxxxxxxxx")
                    print(screen_name)
                    print("xxxxxxxxxxxxxxxx")                    
                    print("retweeter is: " + retweeter.screen_name)
                    print("getting tweets before %s" % (target_oldest))
                    target_new_tweets = api.user_timeline(screen_name = retweeter.screen_name,count=200,max_id=target_oldest)
                    time.sleep(3)
                    print("retweeter is: " + retweeter.screen_name)
                    target_alltweets.extend(target_new_tweets)
                    target_oldest = target_alltweets[-1].id - 1
                    print("...%s tweets downloaded so far" % (len(target_alltweets)))
                    for target_tweet in target_alltweets: 
                        # insert ignore to avoid deadlock with stream dumper
                        cursor.execute("insert ignore INTO twitter.tweets (tweet_id, screen_name, tweet_at, born, urls,symbols,description,text,followers,friends,source, location,statuses_count, time_zone, utc_offset, user_id, verified,logged) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(target_tweet.id,str(target_tweet.user.screen_name), target_tweet.created_at, target_user_data.created_at, str(target_tweet.entities['urls']).encode("utf8","ignore"),str(target_tweet.entities['symbols']).encode("utf8","ignore"), str(target_user_data.description).encode("utf8","ignore"),target_tweet.text.encode("utf-8"), target_user_data.followers_count, target_user_data.friends_count,target_tweet.source,target_user_data.location, str(target_user_data.statuses_count), target_user_data.time_zone, target_user_data.utc_offset, target_user_data.id, target_user_data.verified, datetime.datetime.now()))
                    db.commit()
db.close()
