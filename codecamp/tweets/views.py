from django.shortcuts import render
from django.http import HttpResponse

from core import main

from io import fetch_movies_from_web

import nlp
# Create your views here.

def test(request):
    print "plaa"
    return HttpResponse("OK")

def main(request):
    tweet = main()
    return HttpResponse(tweet)

def nlps(request):
    ret = nlp.parse("Angelina Jolie is having breakfast with Brad Pitt.")
    return HttpResponse(ret)

def fetch_movies(request):
    movies = fetch_movies_from_web(1000)
    return HttpResponse(movies)