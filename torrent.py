#!/usr/bin/python

#----------------------------------#
# Scraper for mininova             #
# Coded by Abhishek Nagaraj        #
# For the Mobile Innovation Group  #
# MIT Sloan School of Management   #
# (c) 2011.                        #
#----------------------------------#

from BeautifulSoup import BeautifulSoup
import re
import urllib2
import locale

# INIT STUFF
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 
count = 0


# GET DATA

#page = '<dl><dt style="background: transparent url(\'/img/accept.png\') no-repeat right center" title="Verified By Users"><a href="/2b946e66bf1440109b6bb2c242049752b04634b3"><b>Windows</b> 7 ULTIMATE SP1 ALL EDITIONS 32 64 bit MAFIAA</a> &#187; appz apps pc <b>software</b> applications <b>windows</b></dt><dd><span class="a"><span title="Sun, 12 Jun 2011 18:45:42">4 months ago</span></span> <span class="s">4322 Mb</span> <span class="u">2,608</span> <span class="d">1,248</span></dd></dl>'

page = urllib2.urlopen("http://torrentz.eu/so/software+windows-q")


# FEED DATA TO THE SOUP!
soup = BeautifulSoup(page)


# FIND ALL ITEMS OF INTEREST 
item = soup.findAll('dl')

#item = soup.body.dl.dt.a

# LOOK FOR OBJECTS IN ITEM

for i in item:
    count = count + 1
    if count>3 and count <7:

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


    #verified = i.dt['title']
    #print i.dt.attrs

        if url!=None:
            print i
            print
            print "http://torrentz.eu"+ url
            print name
            print days
            print size
            print date_collected
            print seeds, peers
            print verified
            print "-----"


    #fragment = BeautifulSoup(i)
    #print fragment.dt.a
    #print fragment.dd





#print soup.prettify()

#print item

# for incident in soup('td', width="90%"):
#     where, linebreak, what = incident.contents[:3]
#     print where.strip()
#     print what.strip()
#     print
