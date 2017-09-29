#!/usr/bin/python3
import pymysql
import json
from subprocess import call
import os
import fileinput

# db
db = pymysql.connect("localhost","test","test","ico")
cursor = db.cursor()

select_sql = "SELECT symbol FROM ico.coins where new like '1'"
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
print(uniq_list)
print(len(uniq_list))

coin_list = "','".join(known_coins)
print(coin_list)
filter_list = "'" + coin_list + "'"
print(filter_list)

# Stop, update and restart the Twitter stream
command="supervisorctl stop twitter.db.altcoin.py"
p = os.system('sudo %s' % (command))

command="cp /home/josh/tw/twitter.db.altcoin.pristine.py /home/josh/tw/twitter.db.altcoin.py"
p = os.system(command)

with fileinput.FileInput('/home/josh/tw/twitter.db.altcoin.py', inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace('listofsymbolshere', filter_list), end='')

command="supervisorctl start /home/josh/tw/twitter.db.altcoin.py"
p = os.system('sudo %s' % (command))
