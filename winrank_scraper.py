#!/usr/bin/python

#------------------------------------------#
# Ranking Scraper for Windows Phone        #
# Coded by Francis Plaza                   #
# For the Mobile Innovation Group          #
# MIT Sloan School of Management           #
# (c) 2011.                                #
#------------------------------------------#


import feedparser
import MySQLdb
import time
import random

localtime = time.localtime()
year = localtime[0]
month = localtime[1]
day = localtime[2]

print 'Started winrank_scraper.py at ',
print month, '-', day, '-',  year,
print str(localtime[3]) + ':' + str(localtime[4])

startLink = 'http://catalog.zune.net/v3.2/en-US/appCategories/windowsphone.'
endLink = '/apps?store=Zest&clientType=WinMobile+7.0&orderby=downloadRank'
costs = ['all', 'paid', 'free']

########################
## Categories
games = ['games', 'puzzleandtrivia', 'actionandadventure', 'cardandcasino', 'boardandclassic', 'sportsandracing', 'strategy', 'family', 'music', 'shooter', 'xboxcompanion']
entertainment = ['entertainment']
musicandvideo = ['musicandvideo']
photo = ['photo']
lifestyle = ['lifestyle', 'shopping', 'outandabout', 'foodanddining', 'community']
news = ['newsandweather']
sports = ['sports']
health = ['healthandfitness', 'health', 'fitness', 'dietandnutrition']
finance = ['finance']
travel = ['travel', 'planning', 'cityguides', 'language', 'traveltools']
navigation = ['navigation']
social = ['social']
productivity = ['productivity']
tools = ['tools']
business = ['business']
books = ['booksandreference', 'ereader', 'fiction', 'non-fiction', 'reference']

categories = games + entertainment + musicandvideo + photo + lifestyle + news + sports + health + finance + travel + navigation + social + productivity + tools + business + books
##
########################


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

def writeData(data, cat, cost, rank, allappsenabled = True):
	if allappsenabled:
		for ent in data:
		# GB18030 to include Chinese encoding
			writeAllApps(ent['mediainstanceid'].encode('gb18030'), ent['sorttitle'].encode('gb18030'), cat, cost, rank)
			rank = rank + 1
	return rank

def writeAllApps(mediainstanceid, sorttitle, category, cost, rank):
	sec = time.time()
	utc = int(sec)
	timestamp = time.ctime(sec)
	
	# Write to database
	cursor = db.cursor()
	cursor.execute("""INSERT INTO windows_rank (YEAR, MONTH, DAY, TIME, APPNAME, APPID, CATEGORY, COST, RANK) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (year, month, day, timestamp, sorttitle, mediainstanceid, category, cost, rank))

#-----MAIN PROGRAM-----#
for cat in categories:
	for cost in costs:
		fullStartLink = startLink + cat + endLink
		if not cost == 'all':
			fullStartLink = fullStartLink + '&cost=' + cost
		dataList = getAllData(fullStartLink)
		rank = 1
		for data in dataList:
			rank = writeData(data, cat, cost, rank)
		time.sleep(random.randint(1,5))

db.close()

localtime = time.localtime()

print 'Finished winrank_scraper.py at ',
print localtime[1], '-', localtime[2], '-', localtime[0], 
print str(localtime[3]) + ':' + str(localtime[4])
