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

select_sql = "SELECT symbol FROM ico.coins where exchange like 'ccex'"
cursor.execute(select_sql)
results = cursor.fetchall()

# Make list of coins in the db
known_coins = []
for row in results:
    coin = row[0] 
    known_coins.append(coin)
  
# Remove duplicates
uniq_list = set(known_coins)
print(len(known_coins))

# Get coins to compare with known_coins
r = requests.get('https://c-cex.com/t/api_pub.html?a=getmarkets')
json_obj = json.loads(r.text)
#print(r.text)
c = 0
for i in (json_obj['result']):
    c = c + 1
    print(c)
    print(i['MarketCurrency'])
    symbol = (i['MarketCurrency'])
    name = (i['MarketCurrencyLong'])
    if (symbol) not in known_coins:
    # Exchange column 
        mysql_select = "insert into coins (symbol, name, exchange, discovered, new) values(%s, %s, %s, %s, %s)"
        cursor.execute(mysql_select, (i['MarketCurrency'], name, 'ccex', datetime.utcnow(), '1'))
    else:
        pass
    db.commit()        
db.close()