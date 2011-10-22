import torrent
import time
import random

# -*- coding: utf-8 -*-
## this function takes in a set of keywords, assumes that the data is present in data/ and parses it and print it

def parsedata(keywords):
    
    count = 0
    query = ""

    for keyword in keywords:
        query = query + keyword + '_'

    while count < 200:

        f = open('data/'+query+str(count)+'.txt','r')
        data =  torrent.getdata(f.read())

        for row in data:
               print str(count) + "." + row['url']

        count = count +1

keywords = ['software','windows']
parsedata(keywords)

