# Twitter-sentiment-analysis-movies
Correlating the IMDb/Rotten Tomatoes movie ratings with the sentiments scores in tweets posted after the release date

get_ratings_data.py : Makes calls to the OMDb / Themoviedb.org APIs to gather ratings for movies listed in the script and dumps the data dictionary

get_tweets_data.py : Uses the Twitter Search API to collect tweets with the hashtag of the selected movies. Note that the data only goes back 6-9 days with the Search API

analysis.py : Assigns a sentiment score (ratio of no. of negative tweets to that of positive tweets) for each movie. A word list created by Finn Årup Nielsen is used for this purpose. Details at http://www2.imm.dtu.dk/pubdb/views/publication_details.php?id=6010
