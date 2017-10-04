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

# Authentication pieces
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
    stream.filter(track=['$bmchain token ', '$sht ', '$hmq ', '$piex ', '$0x81be91c7e74ad0957b4156f782263e7b0b88cf7b ', '$bis ', '$sggcoin ', '$0x32c785e4e8477b277fea2ca2301727084d79d933 ', '$dtc ', '$mkr ', '$rpl ', '$goku ', '$hsr ', '$san ', '$pow ', '$frd ', '$cnx ', '$swp ', '$odn ', '$zec ', '$whl ', '$0xe2f45f1660dc99daf3bd06f637ab1e4debc15bde ', '$mgo ', '$dcnt ', '$0x6fff3806bbac52a20e0d79bc538d527f6a22c96b ', '$cld ', '$ldm ', '$hpc ', '$ind ', '$lun ', '$adt ', '$hkg ', '$rep ', '$bop ', '$tft ', '$alis ', '$lottereum ', '$dgd ', '$gno ', '$edoge ', '$btn ', '$orme ', '$pt ', '$nxx ', '$0x4bf215086c05c0384bdf3731bdb2b37799e9bb5b ', '$r token ', '$rup ', '$vsmold ', '$proxy token ', '$xai ', '$umc ', '$0x93182d5f3a05bf5eb6b9f6c0e003a46dff9128ff ', '$rare ', '$salt ', '$bananacoin extended ', '$32c7 ', '$0x865d176351f287fe1b0010805b110d08699c200a ', '$evr ', '$silent notary token ', '$0x2df8286c9396f52e17dfee75d2e41e52609cf897 ', '$fuckold ', '$ndc ', '$kick ', '$bmt ', '$pts ', '$1life ', '$tgt ', '$ntc ', '$inxt ', '$0x2167bcd8bc794f2c7039c3516cd5d37aac8de7c6 ', '$natcoin ', '$dgb ', '$trx ', '$r ', '$exn ', '$network ', '$jet ', '$gcc24 ', '$oax ', '$bco ', '$nmr ', '$f2utoken ', '$e4row ', '$net ', '$ebtc ', '$nxc ', '$bnt ', '$quiztum ']
, async=True)
