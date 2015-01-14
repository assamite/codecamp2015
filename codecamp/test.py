import json, urllib
keyword = "Arnold Schwarzenegger"
api_key = "AIzaSyCMgSTWG1sBvqV2PgjSSYLDEQSOpUqVJAI"
service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
query = [{ "name": keyword, "/common/topic/alias": []}]
params = { 'query': json.dumps(query), 'key': api_key, 'limit':5}    
url = service_url + '?' + urllib.urlencode(params)
response = json.loads(urllib.urlopen(url).read())
print json.dumps(response,indent=4)
