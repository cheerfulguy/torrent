import torrent
import time
import random
import urllib2

## this libary will take a list of keywords and dump pages to the data directory
## it also needs a sleep variable that is greater than zero

def dumpfiles(sleeptime, keywords):
    
    count =0
    query = ""
    
    for keyword in keywords:
        query = query + keyword + '+'

    query = query[:-1]

    while count < 200:
        f = open('data/software_windows_' + str(count) + '.txt','w')
        url = "http://torrentz.eu/search?q=" + query + "&p="+str(count)
        page = urllib2.urlopen(url)
        f.write(page.read())
        time.sleep(random.randrange(0,sleeptime))
        count = count +1
        print "got page # " + str(count)
