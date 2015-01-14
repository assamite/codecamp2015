'''
.. py:module:: 
    :platform: Unix
    
IO functionality
'''
import sys
import os
import logging
import traceback

# In case we are not running these through Django, let module know
# the correct twitter app settings from TwatBot's settings file.
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'codecamp.settings'
from django.conf import settings
import tweepy

logger = logging.getLogger('tweets.default')

DEBUG = False

def tweet(self, tweet):
    '''Tweet to the twitter.
    
    .. warning:: 
        Don't use this method directly as the sent tweets are not stored in
        the bot's memory.
    
    :returns: tuple -- (bool, str), where bool is True if the tweet was send,
    and False otherwise. str contains the actual tweet returned by Twitter,
    it can be altered from the given tweet by, e.g. adding short URL for the
    given image.
    '''
    if DEBUG: 
        logger.info("DEBUG mode on, choosing not to tweet.")
        return (True, tweet)   
    try:
        auth = tweepy.OAuthHandler(self.tak, self.tas)
        auth.set_access_token(self.tat, self.tats)
        api = tweepy.API(auth)
        api.update_status(status = tweet)
    except Exception:
        e = traceback.format_exc()
        logger.error("Could not tweet to Twitter. Error: {}".format(e))
        return (False, "")
    
    return (True, tweet)