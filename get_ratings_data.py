##Get ratings from OMDb, Rotten tomatoes, and TMDb
import urllib2
import xml.etree.ElementTree as ET
import pickle
import json
import numpy as np

import matplotlib.pyplot as plt

with open('z_scores', 'r') as f:
    z_scores = pickle.load(f)

movie_data = {}

movie_list = ['The Imitation Game','Selma','American Sniper','Fifty Shades Of Grey','Inherent Vice','Blackhat','The Wedding Ringer','Kingsman The Secret Service','McFarland USA', 'Birdman']

for movie in movie_list:
	movie_data[movie] = {}
	title = urllib2.quote(movie)
	
	##OMDb API for movie information in xml format, also includes Rotten Tomatoes ratings if available
	
	response = urllib2.urlopen('http://www.omdbapi.com/?t='+ title + '&r=xml&tomatoes=true')
	xml_res = response.read()
	root = ET.fromstring(xml_res)
	movie_data[movie]['title'] = root.find('movie').attrib['title']
	movie_data[movie]['imdbID'] = root.find('movie').attrib['imdbID']
	movie_data[movie]['imdbRating'] = root.find('movie').attrib['imdbRating']
	movie_data[movie]['tomatoRating'] = root.find('movie').attrib['tomatoRating']
	movie_data[movie]['actors'] = root.find('movie').attrib['actors']

	##Calling the Themoviedb.org API using IMDb ID obtained above to get another set of ratings as some
	##of the the ratings returned by the OMDb API are marked 'N/A'
	api_key = ''
	response = urllib2.urlopen('http://api.themoviedb.org/3/search/movie?api_key='+'&query=' + title)
	json_res = json.loads(response.read())
	movie_data[movie]['tmdbRating'] = json_res['results'][0]['vote_average']
	##Average rating
	movie_data[movie]['avgRating'] = np.mean([float(rating) for rating in [movie_data[movie]['tomatoRating'], movie_data[movie]['imdbRating'], movie_data[movie]['tmdbRating']] if rating != 'N/A'])
	movie_data[movie]['z_score'] = z_scores[movie]
	##Add 'pickled' z-scores to this dictionary

with open('ratings_data','w') as f:
	pickle.dump(movie_data, f)


##Plotting
a=[]
b=[]
for movie in movie_data.keys():
	a.append(movie_data[movie]['avgRating']), b.append(movie_data[movie]['z_score'])

b_mat = np.append(np.matrix(b).T,np.matrix(np.ones(len(b))).T, axis = 1)
a_mat = np.matrix(a)
m, c = np.linalg.lstsq(b_mat, a_mat.T)[0]

plt.scatter(b,a)
plt.plot(b_mat[:,0], int(m)*b_mat[:,0] + c, 'b', label='All points')
for count,(i,j) in enumerate(zip(b,a)):
	plt.annotate(movie_data.keys()[count], xy=(i,j),textcoords='offset points')

plt.title('Average rating of movies v/s Nature of tweets')
plt.xlabel('Ratio of the number of negative tweets to positive tweets')
plt.ylabel('Average rating')
plt.legend()
plt.grid()
plt.show()