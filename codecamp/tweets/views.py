from django.shortcuts import render
from django.http import HttpResponse

from core import main

# Create your views here.

def test(request):
    print "plaa"
    return HttpResponse("OK")

def main(request):
    tweet = main()
    return HttpResponse(tweet)