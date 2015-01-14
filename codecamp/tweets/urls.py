'''
.. py:module: urls
    :platform: Unix
    
Custom URLs for the app.
'''
from django.conf.urls import patterns, include, url

from views import main, nlps, fetch_movies, process_summaries, filter_keywords

urlpatterns = patterns('',
    url(r'^main$', main, name='tweets_main_url'),
    url(r'^nlp$', nlps, name='tweets_nlp_url'),
    url(r'^fetch_movies$', fetch_movies, name='tweets_movies_url'),
    url(r'^process_summaries$', process_summaries, name='tweets_summaries_url'),
    url(r'^filter_keywords$', filter_keywords, name='tweets_filter_url'),
)
