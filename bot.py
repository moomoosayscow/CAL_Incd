from send_tweet import sending
from look_calfire import parseIncidents
from datetime import datetime
from dateutil import parser as dateparser
import time

def hms_to_seconds(t):
    h, m, s = [int(i) for i in t.split(':')]
    return 3600*h + 60*m + s


while(True):
	activeseconds=0	#arbitrary values
	secondsnow=1

	activetime=dateparser.parse('12:00').time()
	datenow=datetime.now() #gives today's date
	datenow=datenow.replace(microsecond=0)
	timenow=datenow.time()
	secondsnow=hms_to_seconds(str(timenow))
	activeseconds=hms_to_seconds(str(activetime))


	if (activeseconds - secondsnow) == 0: #if time is met, send tweet
		url="http://www.fire.ca.gov/current_incidents" 
		filename="current_incidents"
		tweet = parseIncidents(url, filename)
		sending(tweet)
		time.sleep(3)