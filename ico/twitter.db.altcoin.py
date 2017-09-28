#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import webbrowser
import pprint
import MySQLdb
import time
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import re


conn = MySQLdb.connect("localhost","test","test","twitter",charset="utf8mb4",init_command='SET NAMES utf8mb4')
c = conn.cursor()

# authentication pieces
consumer_key            = ""
consumer_secret         = ""
access_token            = ""
access_token_secret     = ""



class StdOutListener(StreamListener):

    def on_data(self, data):
        try:
            data = (data).encode("utf-8","ignore")
            description = (json.loads(data)['user']['description'])
            name     = json.loads(data)['user']['name']
            text     = json.loads(data)['text']
            screen_name = json.loads(data)['user']['screen_name']
            profurl = ("https://twitter.com/%s" % screen_name) 
            followers = json.loads(data)['user']['followers_count']
            friends = json.loads(data)['user']['friends_count']
            source = json.loads(data)['source'].split(">")[-2].replace("</a","")
            location = json.loads(data)['user']['location']
            tweet_id = json.loads(data)['id']
            tweet_date = json.loads(data)['created_at']
            user_created = json.loads(data)['user']['created_at']
            tweet_at = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet_date,'%a %b %d %H:%M:%S +0000 %Y'))
            born = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(user_created,'%a %b %d %H:%M:%S +0000 %Y'))
            text = text.lower()  
            c.execute("INSERT INTO tweets (born,tweet_at,tweet_id,screen_name,name,text,description,profurl,followers,friends,source,location) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(born,tweet_at,tweet_id,screen_name,name,text,description,profurl,followers,friends,source,location))
            conn.commit()
            return True
        except:
            pass

def on_error(self, status):
    print(status)

if __name__ == '__main__':


    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['$GRWI ','$eli ','$hac ','$deep ','$hdlb '], async=True)
