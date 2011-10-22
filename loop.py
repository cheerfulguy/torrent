import torrent
import time
import random

# -*- coding: utf-8 -*-
## name, url, days, size, date_collected, seeds, peers, verified

f = open('urls.txt','w')
count =84
while count < 200:
    url = "http://torrentz.eu/search?q=software+windows&p="+str(count)
    print url
    data =  torrent.getdata(url)
    time.sleep(2*random.random())
    for row in data:
        f.write(row['url'] + '\n')
        print str(count) + "." + row['url']
    count = count +1

