#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import MySQLdb
import json
import time

conn = MySQLdb.connect("localhost","test","test","twitter",charset="utf8mb4",init_command='SET NAMES utf8mb4')
c = conn.cursor()

# Auth
consumer_key            = " "
consumer_secret         = " "
access_token            = " - "
access_token_secret     = " "

class StdOutListener(StreamListener):

    def on_data(self, data):
        screen_name = json.loads(data)['user']['screen_name']
        screen_name = (screen_name).encode("utf-8","ignore")
        json.loads(data)['created_at']
        tweet_date = json.loads(data)['created_at']
        tweet_at = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet_date,'%a %b %d %H:%M:%S +0000 %Y'))
        user_created = json.loads(data)['user']['created_at']
        born = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(user_created,'%a %b %d %H:%M:%S +0000 %Y'))
        user_mentions = json.loads(data)['entities']['user_mentions']
        urls = json.loads(data)['entities']['urls']
        urls = str(urls)
        symbols = json.loads(data)['entities']['symbols']
        symbols = str(symbols)
        description = (json.loads(data)['user']['description'])
        username     = json.loads(data)['user']['name']
        username = str(username)
        text     = json.loads(data)['text']
        text = text.lower()
        followers = json.loads(data)['user']['followers_count']
        friends = json.loads(data)['user']['friends_count']
        source = json.loads(data)['source'].split(">")[-2].replace("</a","")
        location = json.loads(data)['user']['location']
        tweet_id = json.loads(data)['id']
        time_zone = json.loads(data)['user']['time_zone']
        utc_offset = json.loads(data)['user']['utc_offset']
        user_id = json.loads(data)['user']['id']
        in_reply_to_screen_name = json.loads(data)['in_reply_to_screen_name']
        in_reply_to_status_id = json.loads(data)['in_reply_to_status_id']
        in_reply_to_user_id = json.loads(data)['in_reply_to_user_id']
        retweet_count = json.loads(data)['retweet_count']
        retweeted = json.loads(data)['retweeted']
        c.execute("INSERT INTO tweets (screen_name,tweet_at,born,urls,symbols,description, username, text, followers, friends, source, location, tweet_id, time_zone, utc_offset, in_reply_to_screen_name, in_reply_to_status_id, in_reply_to_user_id,retweet_count,retweeted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",([screen_name,tweet_at,born,urls,symbols,description, username, text, followers, friends, source, location, tweet_id, time_zone, utc_offset, in_reply_to_screen_name, in_reply_to_status_id, in_reply_to_user_id,retweet_count,retweeted]))
        conn.commit()        

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['basketball'])
