#!/usr/bin/python3
import pymysql
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import json
from urllib.parse import urlparse
from datetime import datetime

# db
db = pymysql.connect("localhost","test","test","ico")
cursor = db.cursor()

select_sql = "SELECT symbol FROM ico.coins where exchange like 'liqui'"
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
        
# Get coins from liqui
r = requests.get('https://api.liqui.io/api/3/info')
json_obj = json.loads(r.text)
add_list = ""
print(json_obj['pairs'])
for item in json_obj['pairs']:
    symbol = item.replace("_eth","").replace("_btc","").replace("_usdt","")
    if (symbol in known_coins or symbol in add_list):
        pass
    else:
        name = item
        mysql_select = "insert into ico.coins (symbol, name, exchange, discovered, new) values(%s, %s, %s, %s, %s)"
        cursor.execute(mysql_select, (symbol, name, 'liqui', datetime.utcnow(), '1'))
        add_list += symbol
    db.commit()        
db.close()