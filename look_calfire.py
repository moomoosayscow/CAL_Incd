import requests
from bs4 import BeautifulSoup
from os.path import exists
from datetime import datetime
from dateutil import parser as dateparser


def download(url, filename):
	print(url,' downloading to ', filename, '...')
	resp=requests.get(url)
	destname = filename
	destfile = open(destname, 'wb')
	destfile.write(resp.content)
	destfile.close()
	destfile = open(filename, 'r', encoding="utf8")
	soup = BeautifulSoup(destfile, 'lxml') #downloading and opening html from website
	return soup


def findDays(itemday):
	occur=[]
	for item in itemday:
		if 'updated' in item.text.lower():
			itemtxtd=item.text
			itemtxtd=itemtxtd[8:].strip() #take of unnecessary information
			dateold=dateparser.parse(itemtxtd)
			datenow=datetime.now() #gives today's date
			#datenow=dateparser.parse(' March 09, 2017 11:45 am') # for testing purposes, since I am using an archived verion
			diff = datenow.timestamp() - dateold.timestamp()
			seconds_per_day = 60*60*24
			fractional_days = diff/seconds_per_day
			numdays=round(fractional_days, 2)
			print(numdays)
			if numdays <= 1 and numdays>0: #if day updated was less than a day ago
				print('still occuring')
				occur.append(1) #store 1 if the event is still occuring
			else:
				print('not occuring anymore')
				occur.append(0)

	return occur

def findIncidents(itemincd, occur):
	incidents=[]
	count=0
	for item in itemincd:
		itemtxt=item.text.strip()[:-1] #take off unnecessary information
		if 'more info...' in item.text.lower(): #some of the headers do not contain more info
			itemtxt=item.text.strip()[:-13]
			itemtxt=itemtxt.strip()
			itemtxt=itemtxt[:-1]
			if occur[count]==1:
				incidents.append(itemtxt) #add incident name to array if currently occuring
				count+=1
	return incidents

def makeTweet(incidents):
	if(len(incidents)>0): # goes through the array of incidents that we created
		tweet='Current Incidents Reported: '
		for inc in incidents:
			tweet=tweet+inc+' | '
	else:
		tweet='No current incidents reported' 
	return tweet

def parseIncidents(url, filename):
	soupfile=download(url, filename)
	itemincd=soupfile.findAll('td', attrs={'class': 'header_td'}) #headers contain the name of the incident
	itemday=soupfile.select('td')#going to search generally for the date since it follows a more noticeabe format
	occur=findDays(itemday)
	incidents=findIncidents(itemincd, occur)
	tweet=makeTweet(incidents)
	print(tweet)
	return tweet