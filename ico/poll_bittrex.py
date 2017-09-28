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

select_sql = "SELECT symbol FROM ico.coins where exchange like 'bittrex'"
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

# Get coins to compare with known_coins
r = requests.get('https://bittrex.com/api/v1.1/public/getmarkets')
json_obj = json.loads(r.text)

for i in (json_obj['result']):
    symbol = (i['MarketCurrency'])
# Only making a list of coins trading in BTC for now
    if (i['MarketCurrency']) in known_coins:
        pass
    else:
        print(symbol + ' nope')
        name = (i['MarketCurrencyLong'])
        # Exchange column 
        symbol = (i['MarketCurrency']) 
        mysql_select = "insert into coins (symbol, name, exchange, discovered, new) values(%s, %s, %s, %s, %s)"
        cursor.execute(mysql_select, (i['MarketCurrency'], name, 'bittrex', datetime.utcnow(), '1'))
    db.commit()        
db.close()