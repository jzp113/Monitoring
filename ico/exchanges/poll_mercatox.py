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

select_sql = "SELECT symbol FROM ico.coins where exchange like 'mercatox'"
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
        
# Get coins from mercatox
r = requests.get('https://mercatox.com/public/json24full')
json_obj = json.loads(r.text)
add_list = ""
#pprint.pprint(json_obj['pairs'])
for item in (json_obj['pairs']):
    symbol = item.replace("_ETH","").replace("_BTC","").replace("_PM USD","").replace("_OK USD","").replace("_QIWI","").replace("_DOGE","").replace("_PR USD","").replace("_PR RUB","").replace("_PM EUR","").replace("_YA RUB","")
    name = item
    if (symbol in known_coins or symbol in add_list):
        pass
    else:
        mysql_select = "insert into ico.coins (symbol, name, exchange, discovered, new) values(%s, %s, %s, %s, %s)"
        cursor.execute(mysql_select, (symbol, name, 'mercatox', datetime.utcnow(), '1'))
        add_list += symbol
    db.commit()        
db.close()