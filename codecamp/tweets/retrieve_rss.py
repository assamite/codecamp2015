import feedparser

def retrieve_rss ():
    d = feedparser.parse('http://rss.cnn.com/rss/edition_entertainment.rss')
    return d.entries
    
<<<<<<< Local Changes
#news = retrieve_rss()
#for post in news:
#    print post.title+" : "+ post.link+ " : " +post.published;
	=======
#news = retrieve_rss()
#for post in news:
#    print post.title+" : "+ post.link+ " : " +post.published;
	
>>>>>>> External Changes
