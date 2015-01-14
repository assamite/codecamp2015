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
import urllib2
import urllib
import json
from pattern.web import DOM, URL, plaintext, encode_utf8, decode_utf8, cache
from datetime import datetime
import nlp
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

RSS_URL = 'http://rss.cnn.com/rss/edition_entertainment.rss'

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


def get_feed(rss_url, max_items = 10):
    '''Get most recent entries from the given RSS feed.
    
    The returned entries are in the same format as created by `feedparser <http://pythonhosted.org/feedparser/>`_.
    
    :param rss_url: URL to the RSS feed
    :type rss_url: str
    :param max_items: Maximum amount of items returned from feed
    :type max_items: int
    :returns: list - feed's last entries
    '''
    logger.info("Getting {} newest articles from {}".format(max_items, rss_url))
    feed = feedparser.parse(rss_url)
    return feed['entries'] if len(feed['entries']) < max_items else feed['entries'][:max_items]


def get_articles(rss_url, amount = 10):
    '''Get most recent articles from the given RSS feed.
    
    Each article is returned as a dictionary with following contents:
    
    =====    =================================================
    Key      Value
    =====    =================================================
    title    Headline for the article
    url      URL for the article
    =====    =================================================
    
    :param rss_url: URL to the RSS feed
    :type rss_url: str
    :param amount: Amount of articles to retrieve. For safety, should be in [1, 25].
    :type amount: int
    :returns: list -- Parsed articles  
    '''
    #if url_type not in SUPPORTED_FORMATS:
    #    raise ValueError('Given url_type: {} not in supported formats.'.format(url_type))
        
    entries = get_feed(rss_url, max_items = amount)
    ret = []
    for entry in entries:
        article = {}
        article['title'] = entry['title']
        article['url'] = entry['link']
        #soup = _get_soup(entry['link'])
        #article['text'] = _parse_article(soup, url_type = url_type)
        #if bow:
        #    article['bow_counts'] = text.bow(article['text'], counts = True)
        #    article['bow'] = [w[0] for w in article['bow_counts']]
        ret.append(article)
    return ret
        

def fetch_articles_from_web(count):
    articles = []
    ret = get_articles(RSS_URL, count)
    for a in ret:
        article = Article(headline = a['title'], url = a['url'], date = datetime.now(), content = "")
        article.save()
        keywords = nlp.parse(a['title'])
        for kw in keywords:
            article.keywords.add(kw)
        
        articles.append(article)
        
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

def queryFreebase(keyword):
    #API Key: AIzaSyCWE4FZLfisjhrprvuLZyDWxIR
    api_key = "AIzaSyCMgSTWG1sBvqV2PgjSSYLDEQSOpUqVJAI"
    service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
    query = [{ "name": keyword, "/common/topic/alias": []}]
    params = { 'query': json.dumps(query), 'key': api_key, 'limit':5}
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    print json.dumps(response,indent=4)
