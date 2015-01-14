'''
.. py:module:: tinyurl
    :platform: Unix
    
Shorten URL by querying Tinyurl.com
'''
import urllib

base_url = 'http://tinyurl.com/api-create.php?url='

def get(url):
    '''Shorten given URL.
    
    :param url: URL to shorten
    :type url: str
    :returns: str -- URL shortened by querying tinyurl.com
    '''
    compound_url = base_url + url
    return urllib.urlopen(compound_url).read()
