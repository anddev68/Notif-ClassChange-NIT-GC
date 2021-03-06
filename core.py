# -*- coding: utf-8 -*-

import sys
import urllib
import subprocess
import argparse
import datetime


# Constants
URL = "http://www.gifu-nct.ac.jp/gakka/keijiyou/keijiyou.pdf"
LOCALPDF = "keijiyou.pdf"
LOCALTEXT = "keijiyou.txt"

def download():
    urllib.urlretrieve(URL, LOCALPDF)

def pre_parse():
    cmd = "pdftotext -raw " + LOCALPDF + " " + LOCALTEXT 
    #print("done:" + cmd)
    let = subprocess.check_call( cmd.split(" ") )
    return let

def get_date():
    today = datetime.date.today()
    return str(today.monnth+1) + "月" + str(today.day) + "日"

def filter1(gakunen, gakka, map):
    return filter(lambda item:item['gakka'] is gakka and item['gakunen'] is gakunen, map) 

def filter2(gakunen, map):
    return filter(lambda item:item['gakunen'] is gakunen, map) 

def filter_today(map):
    return filter(lambda item:item['date'] is get_date(), map) 

def dumps(map):
    tmp = ""
    for item in map:
        tmp += item['date'] + item['weeks'] + item['jigen'] + " " + item['gakunen'] + item['gakka'] + "  " + item['old'] + " -> " + item['new']
    return tmp


def parse():
    map = []
    for line in open(LOCALTEXT, "r", encoding="utf-8"):
        terms = line.split(" ")
        # discard headers
        # change conditions if need
        if line.find("教員名") is not -1 or len(terms) < 5 or line is "":
            continue
        # read body
        map.append({
            'date': terms[0],
            'weeks': terms[1],
            'jigen': terms[2],
            'gakka': terms[3],
            'gakunen': terms[4],
            'old': terms[5],
            'new': terms[7].replace("\n","") if 7 < len(terms) else "空きコマ"
        })
    return map


if __name__ == "__main__":
    # arg check
    parser = argparse.ArgumentParser()
    parser.add_argument('--cache',help='Using cache, not download original pdf')
    parser.add_argument('--filter',help='[1E|2E|2C etc...]')
    parser.add_argument('--date', help='today')
    args = parser.parse_args()
    
    # execute
    if args.cache is not None:
        download()
    pre_parse()
    data = parse()
    
    # use filter
    if args.filter is not None:
        data = filter1(args.filter[0], args.filter[1], data)
    
    if args.date is "today":
        date = filter_today(map)

    # print
    if len(data) is 0:
        print("No data.")
    
    for item in data:
        print(item['date'] + item['weeks'] + item['jigen'] + " " + item['gakunen'] + item['gakka'] + "  " + item['old'] + " -> " + item['new'])



