'''
.. py:module:: freebase
    :platform: Unix
    
Freebase.com API queries.
'''
import os
import sys
import json
import urllib

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'codecamp.settings'
from django.conf import settings
    

def query(id = None, name = None, type = None):
    if id is None and name is None and type is None:
        raise Exception("You have to specify at least on of the following: id, name or type")
    
    api_key = open(settings.FREEBASE_API_KEY).read()
    service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
    query = [{'id': id, 'name': name, 'type': type}]
    params = {
        'query': json.dumps(query),
        'key': api_key
    }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    return response['result']