#!/usr/bin/python

#----------------------------------#
# Scraper for Windows Phone        #
# Coded by Francis Plaza           #
# For the Mobile Innovation Group  #
# MIT Sloan School of Management   #
# (c) 2011.                        #
#----------------------------------#

import feedparser
import MySQLdb
import time
import random

localtime = time.localtime()
year = localtime[0]
month = localtime[1]
day = localtime[2]

print 'Started win_scraper.py at ',
print month, day, year,
print str(localtime[3]) + ':' + str(localtime[4])

startLink = 'http://catalog.zune.net/v3.2/en-US/appCategories/windowsphone.'
endLink = '/apps?store=Zest&clientType=WinMobile+7.0'
categories = ['games','entertainment', 'musicandvideo', 'photo', 'lifestyle', 'newsandweather', 'sports', 'healthandfitness', 'finance', 'travel', 'navigation', 'social', 'productivity', 'tools', 'business', 'booksandreference']

# Connect to database
db = MySQLdb.connect('localhost', 'nagaraj','Fdr21$avaumH','nagaraj')

def getNextLink(feed):
	f = feed['feed']
	links = f['links']
	for ent in links:
		if str(ent['rel']) == 'next':
			return ent['href']
	
	return False

def getFeed(link):
	return feedparser.parse(link)

def getEntries(feed):
	return feed['entries']

def getAllData(startLink):
	dataList = list()
	link = startLink
	while not link == False:
		feed = getFeed(link)
		dataList.append(getEntries(feed))
		link = getNextLink(feed)

	return dataList

def writeData(data, cat, allappsenabled = True):
	if allappsenabled:
		for ent in data:
		# GB18030 to include Chinese encoding
			writeAllApps(ent['mediainstanceid'].encode('gb18030'), ent['updated'].encode('gb18030'), cat, ent['sorttitle'].encode('gb18030'), ent['tag'].encode('gb18030'), ent['id'].encode('gb18030'), ent['displayprice'].encode('gb18030'), ent['averagelastinstanceuserrating'].encode('gb18030'), ent['pricecurrencycode'].encode('gb18030'), ent['title'].encode('gb18030'), ent['offerid'].encode('gb18030'), ent['version'].encode('gb18030'), ent['store'].encode('gb18030'), ent['licenseright'].encode('gb18030'), ent['lastinstanceuserratingcount'].encode('gb18030'), ent['userratingcount'].encode('gb18030'), ent['averageuserrating'].encode('gb18030'), ent['clienttype'].encode('gb18030'), ent['releasedate'].encode('gb18030'), ent['paymenttype'].encode('gb18030'))

def writeAllApps(mediainstanceid, updated, category, sorttitle, tag, id, displayprice, averagelastinstanceuserrating, pricecurrencycode, title, offerid, version, store, licenseright, lastinstanceuserratingcount, userratingcount, averageuserrating, clienttype, releasedate, paymenttype):
	sec = time.time()
	utc = int(sec)
	timestamp = time.ctime(sec)
	
	# Some workaround to get publisher name
	idreverse = id[::-1]
	publisher = ''
	for s in idreverse:
		if not s == '/':
			publisher += s
		else: break
	publisher = publisher[::-1]
	
	# Write to database
	cursor = db.cursor()
	cursor.execute("""INSERT INTO windows_main (mediainstanceid, updated, category, sorttitle, tag, id, displayprice, averagelastinstanceuserrating, pricecurrencycode, title, offerid, version, store, licenseright, lastinstanceuserratingcount, userratingcount, averageuserrating, clienttype, releasedate, paymenttype, publisher, year, month, day, UTCsecs, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (mediainstanceid, updated, category, sorttitle, tag, id, displayprice, averagelastinstanceuserrating, pricecurrencycode, title, offerid, version, store, licenseright, lastinstanceuserratingcount, userratingcount, averageuserrating, clienttype, releasedate, paymenttype, publisher, year, month, day, utc, timestamp))

#-----MAIN PROGRAM-----#
for cat in categories:
	fullStartLink = startLink + cat + endLink
	dataList = getAllData(fullStartLink)
	for data in dataList:
		writeData(data, cat)
	time.sleep(random.randint(1,5))

db.close()

localtime = time.localtime()

print 'Finished win_scraper.py at ',
print localtime[1], localtime[2], localtime[0], 
print str(localtime[3]) + ':' + str(localtime[4])
