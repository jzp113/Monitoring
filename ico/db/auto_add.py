#!/usr/bin/python3
import pymysql
import json
from subprocess import call
import os
import fileinput

# db
db = pymysql.connect("localhost","test","test","ico")
cursor = db.cursor()	

# get new in the past 30 min
get_newest_sql = """SELECT distinct lower(symbol) FROM ico.coins where (
symbol not like '300' and symbol  not like '$$$' and symbol not like 'btc' and symbol not like 'ltc' and 
symbol not like 'eth' and symbol not like '0x%' and new = 1 and active = 1 and (discovered > date_sub(utc_timestamp(), interval 10 minute)));"""
cursor.execute(get_newest_sql)
newest = cursor.fetchall()

# if new get the full list - need to figure out before this reaches 400, at 189 now @ ~10 new per day.
if len(newest) > 0:
    all_new_sql = """SELECT distinct lower(symbol) FROM ico.coins where (
    symbol not like '300' and symbol  not like '$$$' and symbol not like 'btc' and symbol not like 'ltc' and 
    symbol not like 'eth' and symbol not like '0x%' and symbol not like '% %' new = 1);"""
    cursor.execute(all_new_sql)
    all_new = cursor.fetchall()    
    add_list = []
    for symbol in all_new:
        add_list.extend(symbol)
    print(len(add_list))
    
    # if add list == 0 and active = 1:
    if add_list == 0:
        pass
    # Format for twitter stream track parameter as an array.
    coin_list = " ','$".join(add_list)
    filter_list = "'$" + coin_list + " '"
    print(filter_list)
    
    # Stop, update and restart the Twitter stream
    command="supervisorctl stop twitter.db.altcoin1.py"
    p = os.system('sudo %s' % (command))
    
    command="cp /home/josh/tw/twitter.db.altcoin1.pristine.py /home/josh/tw/twitter.db.altcoin1.py"
    p = os.system(command)
    
    with fileinput.FileInput('/home/josh/tw/twitter.db.altcoin1.py', inplace=True) as file:
        for line in file:
            print(line.replace('listofsymbolshere', filter_list), end='')
    
    command="supervisorctl start twitter.db.altcoin1.py"
    p = os.system('sudo %s' % (command))    
    
    command="chown josh /home/josh/tw/* -Rf"
    p = os.system('sudo %s' % (command)) 
    
    command="chgrp josh /home/josh/tw/* -Rf"
    p = os.system('sudo %s' % (command))    