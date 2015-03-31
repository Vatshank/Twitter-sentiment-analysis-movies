#!/usr/bin/env python

import oauth2 as oauth
import json, pydot
import urllib2
import pickle

##Authentication tokens
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
token = oauth.Token(key=access_token, secret=access_secret)
client = oauth.Client(consumer, token)

data = {}

##Movie list
movie_hashtag_list = ['#ImitationGame', '#AmericanSniper','#Selma','#FiftyShadesOfGrey','#InherentVice','#Blackhat','#TheWeddingRinger','#KingsmanTheSecretService','#McFarlandUSA', '#Birdman']
movie_list = ['The Imitation Game','American Sniper','Selma','Fifty Shades Of Grey','Inherent Vice','Blackhat','The Wedding Ringer','Kingsman The Secret Service','McFarland USA', 'Birdman']
##Get data from the twitter API
for count,movie in enumerate(movie_hashtag_list):
	movie_name = movie_list[count]

	data[movie_name] = []
	movie_url_encoding = urllib2.quote(movie)
	date_arr = range(14,24) 
	for date in date_arr:
		header, response = client.request('https://api.twitter.com/1.1/search/tweets.json?q='+movie_url_encoding+'&lang=en&count=100&until=2015-02-'+str(date+1) + '&since_id=2015-02-' + str(date), method="GET")
		response_json = json.loads(response)
		for status in response_json['statuses']:
			data[movie_name].extend([status['text']])

##Get unique tweets
for movie in data.keys():
	data[movie] = set(data[movie])
	print movie, len(data[movie])

##Pickle the data
with open('test_data','w') as f:
	pickle.dump(data, f)
