'''
.. py:module:: 
    :platform: Unix
    
IO functionality
'''
import sys
import os
import logging
import traceback
import math

import feedparser

from models import Article
from models import Movie


# In case we are not running these through Django, let module know
# the correct twitter app settings from TwatBot's settings file.
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'codecamp.settings'
from django.conf import settings
import tweepy

logger = logging.getLogger('tweets.default')

DEBUG = False

def download_en(url, cached=False): # set cached=True to store the download source locally (faster)
    id = "en-hack-" + url
    if cached and url in cache:
        return cache[id]
    r = urllib2.Request(encode_utf8(url), "get", {"Accept-Language": "en-US"})
    src = urllib2.urlopen(r).read()
    src = decode_utf8(src) # Unicode
    cache[id] = src
    return src

def tweet(self, tweet):
    '''Tweet to the twitter.
    
    .. warning:: 
        Don't use this method directly as the sent tweets are not stored in
        the bot's memory.
    
    :returns: tuple -- (bool, str), where bool is True if the tweet was send,
    and False otherwise. str contains the actual tweet returned by Twitter,
    it can be altered from the given tweet by, e.g. adding short URL for the
    given image.
    '''
    if DEBUG: 
        logger.info("DEBUG mode on, choosing not to tweet.")
        return (True, tweet)   
    try:
        auth = tweepy.OAuthHandler(self.tak, self.tas)
        auth.set_access_token(self.tat, self.tats)
        api = tweepy.API(auth)
        api.update_status(status = tweet)
    except Exception:
        e = traceback.format_exc()
        logger.error("Could not tweet to Twitter. Error: {}".format(e))
        return (False, "")
    
    return (True, tweet)

def fetch_articles_from_web(self, count):
    articles = []
    for i in range(0,count):
        #Fetch news article
        #Create Article object
        #Add to list
        
        """    
        d = feedparser.parse('http://rss.cnn.com/rss/edition_entertainment.rss')
        """
        
        a = Article() 
        articles.append(a)
        
    return articles
    
def fetch_movies_from_web(self, amount):
    movies = []
    mainUrl = "http://www.imdb.com/search/title?groups=top_1000&sort=user_rating&view=simple"
    listPos = 1;
    newMovie = Movie()
    newPerson = Person()
    newCast = Cast()
    newKeyword = Keyword()
    
    totalResults = 0;

    pageAmount = int(math.ceil(amount / float(100)))

    for i in range(0, pageAmount):
        url = mainUrl + "&start=" + str(listPos)
        listPos += 100
        src = URL(url).download(cached = True)
        dom = DOM(src)

        ranking = dom(".number") #get all rankings
		count = 0
		
        for p in dom(".title a"):
            if totalResults == amount:
                break

            movieURL = "http://akas.imdb.com" + p.href

            src = download_en(movieURL) #force english downloading of movie URL
            filmDom = DOM(src)

            yearNumber = 0
            
            newMovie.toplist_pos = ranking[count][0]
            newMovie.url = movieURL

            #get film year
            for filmYear in filmDom(".header .nobr"):
                yearNumber = filmYear[1][0]
                newMovie.year = yearNumber

            #get film title
            for filmTitle in filmDom(".header .itemprop"):
                newMovie.title = filmTitle[0]

            #get film genres
            for filmGenre in filmDom(".infobar .itemprop"):
				newMovie.genre = filmGenre[0]
                
            #intentionally commented out for now

            #get film keywords
            #for filmKeyword in filmDom(".see-more .itemprop"):
			#	newKeyword.word = filmKeyword[0]
            #    newKeyword.save() #add new keyword
            #    newMovie.add(newKeyword)

            #get film actors
            for filmActor in filmDom(".cast_list .itemprop a span"):
				newCast.name = filmActor[0]
				newCast.save()
				newMovie.append(newCast)
				print filmActor[0]

            #get film characters
            for filmCharacter in filmDom(".cast_list .character a"):
				newPerson.name = filmCharacter[0]
				newPerson.save()
				newMovie.append(newPerson)
                print filmCharacter[0]

            #get short summary
            filmShortSummary = filmDom("#overview-top p")[1]
            filmShortSummary = str(filmShortSummary)
            filmShortSummary = filmShortSummary.replace('<p itemprop="description">', "")
            filmShortSummary = filmShortSummary.replace('</p>', "")
            filmShortSummary = filmShortSummary.strip()
            newMovie.short_summary = filmShortSummary

            #get long summary
            for filmLongSummary in filmDom("#titleStoryLine .canwrap p"):
                filmLongSummary = filmLongSummary[0]
                filmLongSummary = str(filmLongSummary).strip()
                newMovie.long_summary = filmLongSummary

            count += 1
            totalResults += 1
			
			newMovie.save()
			movies.append(newMovie)
        
    return movies
