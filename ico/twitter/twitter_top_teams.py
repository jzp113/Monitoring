#!/usr/bin/python3
import pymysql
import json
from subprocess import call
import os
import fileinput
from collections import defaultdict
import pandas as pd
import pandasql as pdsql
import tweepy
import csv

#Twitter API credentials
consumer_key            = ""
consumer_secret         = ""
access_key            = ""
access_secret     = ""

#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# db
db = pymysql.connect("localhost","test","test","ico")
cursor = db.cursor()	

pysql = lambda q: pdsql.sqldf(q, globals())

# get top retweeted ico's in past 24 hours
select_sql = "select substring_index(substring_index(text, ':', 1), ':', 1) from twitter.tweets where text not like '%stocks%' and text like 'rt %' and (tweet_at > date_sub(utc_timestamp(), interval 24 hour));"
cursor.execute(select_sql)
results = cursor.fetchall()
counts = defaultdict(int)

for x in results:
    counts[x] += 1
    
# create dataframe and take top 10
df = ""
df = sorted(counts.items(), reverse=True, key=lambda tup: tup[1])
for team in df[:10]:
    name =  str(team).replace("rt @","%").split("'")[1] + "%"
    get_members = """SELECT distinct screen_name from twitter.tweets where text like '%s'""" % (name)   
    cursor.execute(get_members)
    members = cursor.fetchall()
    for member in members:
        print(member)
        screen_name = member
        print('grab tweets')
        
db.commit()
db.close()
