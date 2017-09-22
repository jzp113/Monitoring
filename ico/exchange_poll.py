#!/usr/bin/python3
import pymysql
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import json

# Supported exchanges
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

    # Get coins from bittrex to compare with known_coins
    #url = bittrex_url
    r = requests.get(exchange)
    json_obj = json.loads(r.text)

    for i in (json_obj['result']):
        marketcurrency = (i['MarketCurrency'])
        # Only making a list of coins trading in BTC or ETC
        if (i['MarketCurrency']) in known_coins or ((i['BaseCurrency']) != 'BTC' or (i['BaseCurrency']) != 'ETH') :
            pass
        else:
            print(marketcurrency + ' nope')
            basecurrency = (i['BaseCurrency'])
            created = (i['Created'])
            isactive = (i['IsActive'])
            exchange = 'bittrex'
            marketcurrency = (i['MarketCurrency']) 
            mysql_select = "insert into coins (marketcurrency, basecurrency, created, isactive, exchange) values(%s, %s, %s, %s, %s)"
            cursor.execute(mysql_select, (i['MarketCurrency'], i['BaseCurrency'], i['Created'], i['IsActive'], exchange))

    db.commit()
db.close()