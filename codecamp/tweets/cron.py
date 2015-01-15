'''Cron jobs from django-cron.
'''
import sys
import os 

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'codecamp.settings'

import logging
import traceback
from django.conf import settings
from django_cron import CronJobBase, Schedule
import tweepy

#from core import TWEET_CORE
from models import Article, Movie
from core import main

logger = logging.getLogger('django.cron')

class MovieRefresher(CronJobBase):
    """Refresh Movies loaded from the IMDB into database."""
    
    RUN_EVERY_MINS = 600
    RETRY_AFTER_FAILURE_MINS = 30
    #_tak = settings.TWITTER_API_KEY
    #_tas = settings.TWITTER_API_SECRET
    #_tat = settings.TWITTER_ACCESS_TOKEN
    #_tats = settings.TWITTER_ACCESS_TOKEN_SECRET
    
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = "tweets.MovieRefresher"
     
    def do(self): 
        logger.info("Initiating cronjob: {}".format(self.code)) 
        pass
    

class ArticleReader(CronJobBase):
    """Read new articles from RSS feeds."""
    
    RUN_EVERY_MINS = 30
    RETRY_AFTER_FAILURE_MINS = 5
    #_tak = settings.TWITTER_API_KEY
    #_tas = settings.TWITTER_API_SECRET
    #_tat = settings.TWITTER_ACCESS_TOKEN
    #_tats = settings.TWITTER_ACCESS_TOKEN_SECRET
    
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = "tweets.ArticleReader"
     
    def do(self): 
        logger.info("Initiating cronjob: {}".format(self.code)) 
        main()           

                