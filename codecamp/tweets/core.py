import io
import nlp
from models import Movie
from django.http.response import HttpResponse
#from tweets.io import fetch_movies_from_web, fetch_articles_from_web

if __name__ == '__main__':
    pass

def main(send_to_twitter = False):
    #Check if database is empty. In this case, fetch movies, parse them, and store them in database
    import gensim
    print "Loading gensim model"
    model = gensim.models.Word2Vec.load('/Users/pihatonttu/nltk_data/gensim/googlenews_gensim_v2w.model')
    print "Model loaded"
    
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
    threshold = 0.0
    articleSelection = []
    for i in range(0,len(articles)):
        score = nlp.assess(articles[i].keywords.all())
        if(score > threshold):
            articleSelection.append(articles[i])
            
    if(len(articleSelection)==0):
        #Sleep
        return 1
        
    #Retrieve best matching pair of movie and news article
    maxFitness = threshold
    bestPair = []
    for a in articles:
        print a.headline
        for m in movies:
            fitness = get_fitness(a, m, model)         
            if(fitness>maxFitness):
                print "\t", m.title, fitness
                maxFitness = fitness
                bestPair = [a,m]
                
    if(len(bestPair)==0):
        #Sleep
        return 1
    
    tweet = nlp.blend(bestPair[0],bestPair[1])
    if send_to_twitter: 
        io.tweet(tweet)
    return tweet


def get_fitness(article, movie, model):
    totalScore = 0
    comparisons = 0
    article_kws = article.keywords.filter(type = "NN")
    movie_kws = movie.keywords.filter(type = "NN")
    
    for articleKeyword in article_kws:
        akw = articleKeyword.word
        for movieKeyword in movie_kws:  
            mkw = movieKeyword.word
            try:
                score = model.similarity(akw, mkw)    
                totalScore += score
                comparisons += 1
            except:
                continue
                
    comparisons = 1 if comparisons == 0 else comparisons
                
    return float(totalScore)/comparisons
    