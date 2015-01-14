'''
.. py:module:: 
    :platform: Unix
    
IO functionality
'''
import sys
import os
import logging
import traceback
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
        a = Article() 
        articles.append(a)
        
    return articles



def fetch_movies_from_web(self, count):
    movies = []
    for i in range(0,count):
        #Fetch movies from imdb
        #Create Movie object
        #Add to list
        a = Movie() 
        movies.append(a)
        
    return movies



def fetch_movies_from_database(self):
    movies = []
    #Query DB and store movies in list. Return list.
    
    return movies



def push_movies_to_database(movies):
    
    #Push list of movies to database
    
    return 1

