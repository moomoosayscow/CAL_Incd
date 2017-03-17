from twython import Twython
import requests

def sending(tweet):
	with open('twt.txt') as f:
		lines = f.read().splitlines()

	client = Twython(lines[0], lines[1], lines[2], lines[3]) #for tweeting
	client.update_status(status=tweet) #send tweet