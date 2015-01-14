'''
.. py:module: urls
    :platform: Unix
    
Custom URLs for the app.
'''
from django.conf.urls import patterns, include, url

from views import test, nlps

urlpatterns = patterns('',
    url(r'^test$', test, name='tweets_test_url'),
    url(r'^nlp$', nlps, name='tweets_nlp_url'),
)
