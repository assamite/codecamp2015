import io
import nlp
from models import Movie
from django.http.response import HttpResponse
#from tweets.io import fetch_movies_from_web, fetch_articles_from_web

if __name__ == '__main__':
    pass

def main(self):
    
    io.queryFreebase("Arnold Schwarzenegger")
    return
    
    #Check if database is empty. In this case, fetch movies, parse them, and store them in database
    movies = Movie.objects.all()
    if(len(movies)==0):
        movies = io.fetch_movies_from_web(250)
        for i in range(0,len(movies)):
            for keyword in nlp.parse(movies[i].title):
                movies[i].keywords.add(keyword)
                movies[i].save()
        
    #Pull the latest news. There's no need to persist them.
    articles = io.fetch_articles_from_web(10)
    
    #Parse articles
    for i in range(0,len(articles)):
        keywords = nlp.parse(articles[i].headline)
        for keyword in keywords:
            articles[i].keywords.add(keyword)
        
    #Assess articles
    threshold = 0.5
    articleSelection = []
    for i in range(0,len(articles)):
        score = nlp.assess(articles[i].keywords)
        if(score > threshold):
            articleSelection.append(articles[i])
            
    if(len(articleSelection)==0):
        #Sleep
        return 1
        
    #Retrieve best matching pair of movie and news article
    maxFitness = threshold
    bestPair = []
    for i in range(0,len(articles)):
        for j in range(0, len(movies)):
            fitness = nlp.fitness(articles[i], movies[j])
            if(fitness>maxFitness):
                maxFitness = fitness
                bestPair = [articles[i],movies[j]]
                
    if(len(bestPair)==0):
        #Sleep
        return 1
    
    tweet = nlp.blend(bestPair[0],bestPair[1])
    io.tweet(tweet)
    return tweet

