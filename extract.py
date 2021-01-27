# CS288 Homework 8

import sys
import os
import re
import sys
import mysql.connector
from xml.dom.minidom import parse, parseString
from io import StringIO
from xml.parsers import expat

# get all text recursively to the bottom
def get_text(x):
    lst=[]
    if x.nodeType in (3,4):
       lst.append(x.nodeValue)
    else:
        for child in x.childNodes:
            lst = lst + get_text(child)
    return lst

def flatten(l):
    return list(map(lambda x: x[0] if x else 'None', l))

def to_dict(vals):
    keys = ['symbol', 'name', 'price', 'change', 'pchange', 'volume', 'avg_volume', 'market_cap', 'pe_ratio', '52_week_range']
    vals[3] = vals[3].replace('+','')
    vals[4] = vals[4].replace('+','')
    vals[4] = vals[4].replace('%','')
    vals[5] = vals[5][:-1]
    vals[6] = vals[6][:-1]
    if vals[7][-1]=='B':
        vals[7] = vals[7][:-1]
    elif vals[7][-1]=='T':
        vals[7] = str(float(vals[7][:-1])*1000)
    return dict(map(lambda i: (keys[i], vals[i]), range(len(keys))))

# mysql> describe most_active;
def insert_to_db(l,tbl):
    db = mysql.connector.connect(host="localhost", user="root", password="password", database="stock_market", auth_plugin='mysql_native_password')
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS `%s` (Symbol VARCHAR(255), Name VARCHAR(255), Price VARCHAR(255), Chng VARCHAR(255), PcChng VARCHAR(255), Volume VARCHAR(255), Avg_Volume VARCHAR(255), Market_Cap VARCHAR(255))""" % (tbl))
    for line in l:
        query = """INSERT INTO `%s` (Symbol, Name, Price, Chng, PcChng, Volume, Avg_Volume, Market_Cap) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s');""" % (tbl, line['symbol'], line['name'], line['price'], line['change'], line['pchange'], line['volume'], line['avg_volume'], line['market_cap'])
        print(query)
        cursor.execute(query)
        db.commit()
    cursor.close()
    db.close()

# show databases;
# show tables;
def main():
    xhtml_fn = sys.argv[1]
    global e
    e = parse(xhtml_fn)
    l_trs = e.getElementsByTagName('tr')
    hdr = l_trs[0]
    del l_trs[0]
    l_ths = hdr.getElementsByTagName('th')
    hdr_txts = list(map(lambda x: get_text(x),l_ths))
    lst_hdr_txts = flatten(hdr_txts)
    l_txts = list(map(lambda tr: list(map(lambda x: get_text(x),tr.getElementsByTagName('td'))), l_trs))
    new_l_txts = list(map(lambda x: flatten(x),l_txts))
    l_dicts = list(map(lambda company: to_dict(company), new_l_txts))
    fn = xhtml_fn.replace('.xhtml', '')
    cursor = insert_to_db(l_dicts,fn) 
    return True
# end of main()

if __name__ == "__main__":
    main()
