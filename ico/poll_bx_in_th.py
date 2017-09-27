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

select_sql = "SELECT symbol FROM ico.coins where exchange like 'bx.in.th'"
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
        
# Get coins from bx
r = requests.get('https://bx.in.th/api/pairing/')
json_obj = json.loads(r.text)
print(r.text)
#print(json_obj['2']['secondary_currency'])
print(json_obj)
pairing_ids = []
for item in json_obj:
    id = item
    pairing_ids.append(id)
    
# Remove duplicates
uniq_ids = set(pairing_ids)
print(len(uniq_ids))
    
for pairing_id in uniq_ids:
    primary = (json_obj[pairing_id]['primary_currency'])
    secondary = (json_obj[pairing_id]['secondary_currency'])
    pair = primary + "-" + secondary
    out = pairing_id + " " + pair
    symbol = secondary + "-" + primary
    if (symbol) in known_coins:
        pass
    else:
        name = symbol
        mysql_select = "insert into ico.coins (symbol, name, exchange, discovered) values(%s, %s, %s, %s)"
        cursor.execute(mysql_select, (symbol, name, 'bx.in.th', datetime.utcnow()))
    db.commit() 
db.close()

