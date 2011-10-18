import torrent
# -*- coding: utf-8 -*-


## name, url, days, size, date_collected, seeds, peers, verified

url = "http://torrentz.eu/so/software+windows-q"

data =  torrent.getdata(url)

f = open('test.txt','w')

for row in data:
    f.write(row['name'] + '\n')


