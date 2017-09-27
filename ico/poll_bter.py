#!/usr/bin/python3
import pymysql
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import json
from urllib.parse import urlparse
from datetime import datetime
import pprint

# db
db = pymysql.connect("localhost","test","test","ico")
cursor = db.cursor()

select_sql = "SELECT symbol FROM ico.coins where exchange like 'bter'"
cursor.execute(select_sql)
results = cursor.fetchall()

# Make list of coins in the db
known_coins = []
for row in results:
    coin = row[0] 
    known_coins.append(coin)
  
# Remove duplicates
uniq_list = set(known_coins)
known_coins = uniq_list
print(len(known_coins))
        
# Get coins from poloniex
r = requests.get('http://data.bter.com/api2/1/pairs')
json_obj = json.loads(r.text)

for item in (json_obj):
   #print(json_obj)
    symbol = item
    if (symbol) in known_coins:
       pass
    else:
        name = symbol
        mysql_select = "insert into ico.coins (symbol, name, exchange, discovered) values(%s, %s, %s, %s)"
        cursor.execute(mysql_select, (symbol, name, 'bter', datetime.utcnow()))
    db.commit()        
db.close()