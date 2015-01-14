from django.shortcuts import render
from django.http import HttpResponse
<<<<<<< HEAD
=======

from core import main
>>>>>>> FETCH_HEAD

from core import main

import nlp
# Create your views here.

def test(request):
    print "plaa"
    return HttpResponse("OK")

def main(request):
    tweet = main()
<<<<<<< HEAD
    return HttpResponse(tweet)

def nlps(request):
    ret = nlp.parse("Angelina Jolie is having breakfast with Brad Pitt.")
    return HttpResponse(ret)
=======
    return HttpResponse(tweet)
>>>>>>> FETCH_HEAD
