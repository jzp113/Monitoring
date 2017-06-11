#!/usr/bin/env python

import os
import MySQLdb
# Imports the Google Cloud client library
from google.cloud import translate

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/josh/google/vision-05e77e255f0c.json'


# Instantiates a client
translate_client = translate.Client()

conn = MySQLdb.connect("localhost","test","test","twitter",charset="utf8mb4",init_command='SET NAMES utf8mb4')
c = conn.cursor()
c.execute("select count(*) as cnt, screen_name, description from tweets group by screen_name, description order by cnt desc limit 100;")
data = c.fetchall()
#print data
for line in data:
    # Translate into English
    translation = translate_client.translate(
        line[2],
        target_language='en')
    print(u'Translation: {}'.format(translation['translatedText']))
    
