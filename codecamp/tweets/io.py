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
from pattern.web import DOM, URL, plaintext, encode_utf8, decode_utf8, cache
#import plaintext
import urllib2
from datetime import datetime

import feedparser

from models import Article, Movie, Person, Keyword


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

def tweet(tweet):
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
        auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET)
        auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        api.update_status(status = tweet)
    except Exception:
        e = traceback.format_exc()
        logger.error("Could not tweet to Twitter. Error: {}".format(e))
        return (False, "")
    
    return (True, tweet)

def fetch_articles_from_web(count):
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
    
def fetch_movies_from_web(amount):
    movies = []
    mainUrl = "http://www.imdb.com/search/title?groups=top_1000&sort=user_rating&view=simple"
    listPos = 1;

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
            
            #newKeyword = Keyword() 

            movieURL = "http://akas.imdb.com" + str(p.href)

            src = download_en(movieURL) #force english downloading of movie URL
            filmDom = DOM(src)
            
            toplist_pos = int(str(ranking[count][0])[:-1])
            url = movieURL
            title = ""
            year = 0
            genre = ""

            #get film year
            for filmYear in filmDom(".header .nobr"):
                year = int(str(filmYear[1][0]))

            #get film title
            for filmTitle in filmDom(".header .itemprop"):
                title = str(filmTitle[0])

            #get film genres
            for filmGenre in filmDom(".infobar .itemprop"):
                genre = str(filmGenre[0])
                
            #intentionally commented out for now

            #get film keywords
            #for filmKeyword in filmDom(".see-more .itemprop"):
			#	newKeyword.word = filmKeyword[0]
            #    newKeyword.save() #add new keyword
            #    newMovie.add(newKeyword)


                
            #get short summary
            filmShortSummary = filmDom("#overview-top p")[1]
            filmShortSummary = str(filmShortSummary)
            filmShortSummary = filmShortSummary.replace('<p itemprop="description">', "")
            filmShortSummary = filmShortSummary.replace('</p>', "")
            filmShortSummary = str(filmShortSummary.strip())
            short_summary = filmShortSummary

            #get long summary
            for filmLongSummary in filmDom("#titleStoryLine .canwrap p"):
                filmLongSummary = filmLongSummary[0]
                filmLongSummary = str(filmLongSummary).strip()
                long_summary = filmLongSummary
                
            newMovie = Movie(title = title, genre = genre, year = year,\
                             url = url, short_summary = short_summary,\
                             long_summary = long_summary,\
                             toplist_pos = toplist_pos)
            newMovie.save()
                    
                        #get film actors
            for filmActor in filmDom(".cast_list .itemprop a span"):
                name = str(filmActor[0])
                actor = Person.objects.get_or_none(name = name)
                if actor is None:
                    actor = Person(name = name, birthday = datetime.now(),\
                                   nationality = "Unknown", gender = "O")
                    actor.save()
                newMovie.cast.add(actor)
                print filmActor[0]

            #get film characters
            for filmCharacter in filmDom(".cast_list .character a"):
                name = str(filmCharacter[0])
                person = Person.objects.get_or_none(name = name)
                if person is None:
                    person = Person(name = name, birthday = datetime.now(),\
                                    nationality = "Unknown", gender = "O")
                    person.save()
                newMovie.persons.add(person)
                print filmCharacter[0]

            count += 1
            totalResults += 1
            newMovie.save()
            movies.append(newMovie)
        
    return movies
