'''
.. py:module: urls
    :platform: Unix
    
Custom URLs for the app.
'''
from django.conf.urls import patterns, include, url

from views import main, nlps, fetch_movies

urlpatterns = patterns('',
    url(r'^main$', main, name='tweets_main_url'),
    url(r'^nlp$', nlps, name='tweets_nlp_url'),
    url(r'^fetch_movies$', fetch_movies, name='tweets_movies_url'),
)
