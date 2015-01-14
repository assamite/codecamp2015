from models import Keyword
from pattern.en import parse,parsetree

def parse(text):

    keywords = list()
    #Parse: extract nouns, adjectives, named entities, etc., and add keyword-objects to list
    # k = Keyword()
    # k.type = ""
    # k.word = ""
    # k.weight = 0
    # keywords.append(k)

    namedEntities = list()

    previous_chunk=""
    index=0
    for sentence in parsetree(text, lemmata=True):
        for chunk in sentence.chunks:
            for word in chunk.words:
              #  print index
                if '-PERS' in word.tag and  '-PERS' in previous_chunk:
                    namedEntities[index-1]=namedEntities[index-1]+" "+" "+word.lemma

                else:
                    if '-PERS' in word.tag:
                        namedEntities.append(word.lemma)
                        index+=1
                    else:
                        keywordLemma = Keyword()
                        keywordLemma.type = word.tag
                        keywordLemma.word = word.lemma
                        keywordLemma.weight = 0
                        keywords.append(keywordLemma)
                previous_chunk=word.tag

                #  print word.string,word.lemma,word.tag


            #  print namedEntities

    for namedEntity in namedEntities:
        # print 'olaaaaaa',namedEntity
        namedEntityKW = Keyword()
        namedEntityKW.type = "NAMED_ENTITY_PERSON"
        namedEntityKW.word = namedEntity
        namedEntityKW.weight = 0
        keywords.append(namedEntityKW)

    for keyword in keywords:
        print keyword.type, keyword.word

    return keywords



def assess(keywords):
    quality = 0
    for key in keywords:
        if "PERSON" in key.type:
            quality = 1
            break

    return quality
    #Assess the keywords and return a number between 0..1, where 1 indicates best suitability



def fitness(article, movie):
    
    #Calculate similarity score
    return 1



def blend(article, movie):
    
    blended = ""
    #Blend article and movie together and return result text
    for key_movie in movie.keywords:
        if "PERSON" in key_movie.type:
            for key_news in article.keywords:
                if "PERSON" in key_news.type:
                    key_movie.word = key_news.word
                    break
                    
    for key_movie in movie.keywords:
        blended = blended + key_movie.word
    
    return blended
