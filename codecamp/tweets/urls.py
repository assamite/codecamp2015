'''
.. py:module: urls
    :platform: Unix
    
Custom URLs for the app.
'''
from django.conf.urls import patterns, include, url

from views import test

urlpatterns = patterns('',
    url(r'^test$', test, name='tweets_test_url'),
)
