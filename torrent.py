#!/usr/bin/python

#----------------------------------#
# Scraper for mininova             #
# Coded by Abhishek Nagaraj        #
# MIT Sloan School of Management   #
# (c) 2011.                        #
#----------------------------------#

## this library returns a list of hashes with the following keys
## name, url, days, size, date_collected, seeds, peers, verified

from BeautifulSoup import BeautifulSoup
import re
import urllib2
import locale

# INIT STUFF
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 


def getdata(url):

 count = 0
 page = urllib2.urlopen(url)
 # FEED DATA TO THE SOUP!
 soup = BeautifulSoup(page)
 # FIND ALL ITEMS OF INTEREST 
 item = soup.findAll('dl')

 # LOOK FOR OBJECTS IN ITEM
 global r
 r = list()
 for i in item:
     count = count + 1
     if count>3:
         result = getitem(i)
         if result!=0:
             r.append(result)
 return r


#getitem returns one row of the data

def getitem(i):
    
         url = i.dt.a['href']
         name = ''.join(i.dt.a.findAll(text=True))
         days = i.dd.span.span.string
         size = i.dd.find("span", "s").text
         seeds = i.dd.find("span", "u").text
         seeds = locale.atoi(seeds) # step needed to convert a number with commas
         peers = i.dd.find("span", "d").text
         peers = locale.atoi(peers)  # step needed to convert a number with commas
         date_collected = i.dd.span.span["title"]

         # verified logic
         verified = i.findAll(attrs={"style" : re.compile(".*accept.*")})
         if len(verified)==1:
             verified = 1
         else:
             verified=0

         result = {'name' : name.strip(), 'url':"http://torrents.eu"+url.strip(), 'days':days.strip(), 'size':size.strip(), 'date_collected':date_collected.strip(), 'seeds':seeds, 'peers':peers, 'verified':verified}

         if url!=None: 
             return result
         else:
             return 0
         
