from models import Keyword

def parse(text):
    
    keywords = ()
    #Parse: extract nouns, adjectives, named entities, etc., and add keyword-objects to list
    k = Keyword()
    k.type = ""
    k.word = ""
    k.weight = 0
    keywords.append(k)
    
    return keywords



def assess(keywords):
    
    #Assess the keywords and return a number between 0..1, where 1 indicates best suitability
    return 0

