
from datetime import datetime

import io
import nlp
from models import Movie, Tweet
import random
#from tweets.io import fetch_movies_from_web, fetch_articles_from_web

DEBUG = False

def main(send_to_twitter = False, spoof = False):
    #Check if database is empty. In this case, fetch movies, parse them, and store them in database
    '''
    if not spoof:
        import gensim
        print "Loading Word2Vec model"
        model = gensim.models.Word2Vec.load('/Users/pihatonttu/nltk_data/gensim/googlenews_gensim_v2w.model')
        print "Model loaded"
    else:
    '''
    model = None
    
    movies = Movie.objects.all()
    if(len(movies)==0):
        movies = io.fetch_movies_from_web(250)
        for i in range(0,len(movies)):
            for keyword in nlp.parse(movies[i].title):
                movies[i].keywords.add(keyword)
                movies[i].save()
                
    #Fetch noun-adjective pairs from external file. Will return an empty list if file not found
    adjectives = io.fetch_adjectives("lsa-matrix-full.txt")
        
    #Pull the latest news. There's no need to persist them.
    articles = io.fetch_articles_from_web(300, spoof = spoof)
        
    #Assess articles
    threshold = -1000
    articleSelection = []
    for i in range(0,len(articles)):
        score = nlp.assess(articles[i].keywords.all())
        if(score > threshold):
            articleSelection.append(articles[i])
            
    if(len(articleSelection)==0):
        #Sleep
        return 1
        
    #Retrieve best matching pair of movie and news article
    maxFitness = threshold
    curtweets = []
    for a in articles:
        tweet, movie =  build_tweet(a, movies, model, maxFitness, adjectives, send_to_twitter)
        if tweet != "":
            curtweets.append((tweet, movie))
        print u"{} -- {} -- {}".format(tweet, a.headline, movie.title)

    return curtweets


def build_tweet(a, movies, model, maxFitness, adjectives, send_to_twitter):
    bestPair = []
    print u"Building Tweet for: {}".format(a.headline)
    akw = a.keywords.filter(type = "NN")
    mvs = []
    '''
    for mv in movies:
        mkw = mv.keywords.filter(type = "NN")
        for kw in  mkw:
            if akw[0].word == kw.word:
                print akw[0].word, kw.word
                mvs.append(mv)
    '''
    if len(mvs) == 0:           
        for kw in akw:
            curmvs = io.get_movie_based_on_keyword(kw.word, model)
            mvs.extend(curmvs)
            if len(mvs) == 0:
                continue

    for m in mvs:
        #if len(m.title.split()) < 3:
        #    continue
        
        fitness = get_fitness(a, m, model)   
        print m.title, fitness      
        if fitness >= maxFitness:
            print "\t", m.title, fitness
            maxFitness = fitness
            bestPair = [a,m]
    
    '''       
    for m in movies:
        if len(m.title.split()) < 4:
            continue
        fitness = get_fitness(a, m, model)         
        if fitness > maxFitness:
            print "\t", m.title, fitness
            maxFitness = fitness
            bestPair = [a,m]
    '''          
    if len(bestPair) == 0:
        #Sleep
        return "", ""
    
    article = bestPair[0]
    movie = bestPair[1] 
    
    tweet = nlp.blend(article, movie, adjectives, model)
    
    if send_to_twitter and len(tweet) != 0: 
        tweets = Tweet.objects.filter(content = tweet)
        if tweet != movie.title and len(tweets) == 0:
            tweet_links = tweet + " - " + article.headline
            if len(tweet_links) > 135: 
                tweet_links = tweet + " " + article.url
            print u"TWEETING: {}".format(tweet_links) 
            if not DEBUG:
                print u"REALLY TWEETING: {}".format(tweet_links)
                ret = io.tweet(tweet_links)
                if ret[0] is not False:
                    inst = Tweet(content = tweet)
                    inst.save()
                    article.used = True
                    article.save()
                    #movie.save()
                tweet = tweet_links
    return tweet, movie


def get_fitness(article, movie, model):
    if model is None:
        return random.randint(0, 20)
    
    totalScore = 0
    comparisons = 0
    article_kws = article.keywords.filter(type = "NN")
    movie_kws = movie.keywords.filter(type = "NN")
    max_sim = -1
    
    for articleKeyword in article_kws:
        akw = articleKeyword.word
        for movieKeyword in movie_kws:  
            mkw = movieKeyword.word
            try:
                score = model.similarity(akw, mkw) 
                if score > max_sim:   
                    max_sim = score
            except:
                continue
                
    return max_sim
    
