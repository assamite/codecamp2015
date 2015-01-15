from django.shortcuts import render
from django.http import HttpResponse

import core

from io import fetch_movies_from_web
import nlp
from models import Movie, Article, Keyword

import nlp
# Create your views here.

def test(request):
    print "plaa"
    return HttpResponse("OK")

def main(request):
    tweet = core.main(False, spoof = True)
    return HttpResponse(tweet)

def nlps(request):
    ret = nlp.parse("Angelina Jolie is having breakfast with Brad Pitt.")
    return HttpResponse(ret)

def fetch_movies(request):
    movies = fetch_movies_from_web(1000)
    return HttpResponse(movies)

def process_summaries(request):
    movies = Movie.objects.all()
    for movie in movies:
        print movie.title
        keywords = nlp.parse(movie.long_summary)
        
        for kw in keywords:
            mkw = movie.keywords.filter(type = kw.type, word = kw.word)
            print u"{:<10}{}".format(kw.type, kw.word)
            if len(mkw) == 0:
                movie.keywords.add(kw)
        movie.save()
    return HttpResponse("OK")

def filter_keywords(request):
    movies = Movie.objects.all()
    for movie in movies:
        print movie.title
        keywords = movie.keywords.all()
        for kw in keywords:
            if kw.type[:2] not in ['NN', 'JJ', 'VB', 'PE']:
                print u"Removing {} {}".format(kw.type, kw.word)
                movie.keywords.remove(kw)
            else:
                kw.type = kw.type[:2]
                kw.save()
                
    for i in range(10):
        print 
                
    articles = Article.objects.all()
    for a in articles:
        print a.headline
        keywords = a.keywords.all()
        for kw in keywords:
            if kw.type[:2] not in ['NN', 'JJ', 'VB', 'PE']:
                print u"Removing {} {}".format(kw.type, kw.word)
                a.keywords.remove(kw)
            else:
                kw.type = kw.type[:2]
                kw.save()
                
    keywords = Keyword.objects.all()
    for kw in keywords:
        if kw.type[:2] not in ['NN', 'JJ', 'VB', 'PE']:
            print u"Removing {} {}".format(kw.type, kw.word)
            kw.delete()
            
    return HttpResponse("OK")


                