#!/usr/bin/python3
import pymysql
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import json
from urllib.parse import urlparse
from datetime import datetime

# Bittrex and CCEX - same API exchanges
api_list =['https://bittrex.com/api/v1.1/public/getmarkets', 'https://c-cex.com/t/api_pub.html?a=getmarkets']

# db
db = pymysql.connect("localhost","test","test","ico")
cursor = db.cursor()

for exchange in api_list:
    
    select_sql = "SELECT marketcurrency FROM coins"
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
    r = requests.get(exchange)
    json_obj = json.loads(r.text)

    for i in (json_obj['result']):
        marketcurrency = (i['MarketCurrency'])
        # Only making a list of coins trading in BTC for now
        if (i['MarketCurrency']) in known_coins or ((i['BaseCurrency']) != 'BTC') :
            pass
        else:
            print(marketcurrency + ' nope')
            basecurrency = (i['BaseCurrency'])
            created = (i['Created'])
            isactive = (i['IsActive'])
            name = (i['MarketCurrencyLong'])
            exname = urlparse(exchange)
            # Exchange column 
            exch = (exname.netloc.replace("-","_").split(".",1)[0])
            marketcurrency = (i['MarketCurrency']) 
            mysql_select = "insert into coins (marketcurrency, basecurrency, created, status, name, exchange, discovered) values(%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(mysql_select, (i['MarketCurrency'], i['BaseCurrency'], i['Created'], i['IsActive'], name, exch, datetime.utcnow()))
    db.commit()

select_sql = "SELECT marketcurrency FROM coins"
cursor.execute(select_sql)
results = cursor.fetchall()


# Get coins listed on Cryptopia
# Make list of coins in the db
known_coins = []
for row in results:
    coin = row[0] 
    known_coins.append(coin)
        
# Get coins from cryptopia
r = requests.get('https://www.cryptopia.co.nz/api/GetCurrencies')
json_obj = json.loads(r.text)

for item in json_obj['Data']:
    marketcurrency = item['Symbol']
    if (marketcurrency) in known_coins:
        pass
    else:
        print("fholy shit")
        name = (item['Name'])
        status = (item['Status'])
        mysql_select = "insert into coins (marketcurrency, basecurrency, created, status, name, exchange, discovered) values(%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(mysql_select, (marketcurrency, 'na', '2014-01-01 00:00:00', status, name, 'cryptopia', datetime.utcnow()))
    db.commit()        
db.close()