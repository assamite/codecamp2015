'''
.. py:module::
    :platform: Unix

IO functionality
'''
import sys
import os
import json
import urllib
import logging
import operator
import traceback
import math
import operator
from pattern.web import DOM, URL, plaintext, encode_utf8, decode_utf8, cache
import urllib2
from datetime import datetime
import feedparser

import nlp
from models import Article, Movie, Person, Keyword

RSS_URL = 'http://rss.cnn.com/rss/edition_entertainment.rss'


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
        ars = Article.objects.filter(url = a['url'])
        if len(ars) == 0:
            article = Article(headline = a['title'], url = a['url'], date = datetime.now(), content = "")
            article.save()
            keywords = nlp.parse(a['title'])
            for kw in keywords:
                article.keywords.add(kw)
            article.save()
            
        else:
            article = ars[0]
     
        articles.append(article) 
    return articles
    

def fetch_single_movie_from_web(singleUrl):
    src = download_en(singleUrl) #force english downloading of movie URL
    filmDom = DOM(src)

    #We should first query the database to see if this url exists.
    #If it does, we should return that object instead of needlessly scraping

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
    #newKeyword.word = filmKeyword[0]
    #newKeyword.save() #add new keyword
    #newMovie.add(newKeyword)

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
                    url = singleUrl, short_summary = short_summary,\
                    long_summary = long_summary,\
                    toplist_pos = 9999)
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

    newMovie.save()

    return newMovie

def get_movie_based_on_keyword(keyword):
    src = download_en("http://www.imdb.com/find?ref_=nv_sr_fn&q=" + keyword + "&s=all")
    dom = DOM(src)

    #initializing dictionary
    filmRatings = dict()

    for filmInstances in dom(".findList .result_text a"):
        resultString = str(filmInstances[0])
        if "title" in filmInstances.href:
            indivUrl = "http://akas.imdb.com" + filmInstances.href
            indivFilmSrc = download_en(indivUrl)
            indivFilmDom = DOM(indivFilmSrc)

            filmPopularityElement = indivFilmDom(".star-box-details a span")
            if len(filmPopularityElement) == 0:
                continue
            filmPopularity = str(filmPopularityElement[0][0])
            filmPopularity = filmPopularity.replace(",", "")
            filmRatings[indivUrl] = int(filmPopularity)

    sorted_filmRatings = sorted(filmRatings.items(), key=operator.itemgetter(1), reverse=True)
    return fetch_single_movie_from_web(sorted_filmRatings[0][0])

#Fetch pairs of noun:((adjective:score),(adjective:score),...)  from specially prepared file
def fetch_adjectives(filename): 
    d = {}
    if not os.path.exists(filename):
        return d
    
    with open(filename) as f:
        for line in f.readlines():
            words = line.split("\t")
            key = words[0].split("#")[0]
            values = []
            for i in range(1,len(words)):
                words[i]=words[i].replace(" ","#")
                splitted = words[i].split("#")
                if(len(splitted)!=3):
                    continue
                if(splitted[1]=="a"):
                    values.append((splitted[0],splitted[2]))
            d[key]=values
    return d

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
            #newKeyword.word = filmKeyword[0]
            #newKeyword.save() #add new keyword
            #newMovie.add(newKeyword)

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

def queryFreebaseNotableFromName(keyword):
    service_url = 'https://www.googleapis.com/freebase/v1/search'
    params = {
    'query': keyword,
    'key': settings.FREEBASE_API_KEY,
    'filter':'(any type:/people/person)',
    'limit':1
    }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    if(len(response["result"])>0):
        if("notable" in response["result"][0].keys()):
            return response["result"]
        return response["result"][0]["notable"]["name"]
    return -1

def queryFreebasePeopleNameFromAlias(keyword):
    service_url = 'https://www.googleapis.com/freebase/v1/search'
    print settings.FREEBASE_API_KEY
    params = {
    'query': keyword,
    'key': settings.FREEBASE_API_KEY,
    'filter':'(any type:/people/person)',
    'limit':1
    }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    print response
    if(len(response["result"])>0):
        return response["result"][0]["name"]
    return -1

#Query max 10 times per second!
def queryFreebaseAliases(keyword):
    service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
    query = [{ "name": keyword, "/common/topic/alias": []}]
    params = { 'query': json.dumps(query), 'key': settings.FREEBASE_API_KEY, 'limit':1}
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    if(len(response["result"])>0):
        return response[0]["/common/topic/alias"]
    else:
        return []
