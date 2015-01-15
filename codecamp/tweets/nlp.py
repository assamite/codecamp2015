from models import Keyword
from pattern.en import parse, parsetree, wordnet, NOUN
import re

import io

def parse(text):

    keywords = list()
    #Parse: extract nouns, adjectives, named entities, etc., and add keyword-objects to list
    # k = Keyword()
    # k.type = ""
    # k.word = ""
    # k.weight = 0
    # keywords.append(k)

    namedEntities = list()
    print text

    previous_chunk=""
    index=0
    for sentence in parsetree(text, lemmata=True):
        print sentence
        for chunk in sentence.chunks:
            for word in chunk.words:
                #  print index
                if '-PERS' in word.tag and  '-PERS' in previous_chunk:
                    namedEntities[index-1]=namedEntities[index-1]+" "+(word.lemma).capitalize()
                else:
                    if '-PERS' in word.tag:
                        namedEntities.append((word.lemma).capitalize())
                        index+=1
                    else:
                        tag = word.tag
                        lemma = word.lemma
                        if tag[:2] in ['NN', 'JJ', 'VB']:
                            if tag == "NNP":
                                lemma = lemma.capitalize()
                                person = io.queryFreebasePeopleNameFromAlias(lemma)
                                if person != -1:
                                    namedEntities.append(person)
                            else:    
                                kws = Keyword.objects.filter(type = tag, word = lemma)
                                if len(kws) == 0:
                                    keywordLemma = Keyword(type = tag, word = lemma, weight = 0)
                                    keywordLemma.save()
                                else:
                                    keywordLemma = kws[0]
                                keywords.append(keywordLemma)
                previous_chunk=word.tag

                #  print word.string,word.lemma,word.tag


            #  print namedEntities

    for namedEntity in namedEntities:
        kws = Keyword.objects.filter(type = 'PERSON', word = namedEntity)
        if len(kws) == 0:     
            namedEntityKW = Keyword(type = "PERSON", word = namedEntity, weight = 0)
            namedEntityKW.save()
        else:
            namedEntityKW = kws[0]
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


def fitness(article, movie, model):
    
    #Calculate similarity score
    totalScore = 0
    comparisons = 0
    article_kws = article.keywords.filter(type = "NN")
    movie_kws = movie.keywords.filter(type = "NN")
    
    for articleKeyword in article_kws:
        for movieKeyword in movie_kws:       
            movieSynsets = wordnet.synsets(movieKeyword, NOUN)
            if len(movieSynsets) > 0:
                movieSynset = movieSynsets[0]
            else:
                continue
            if articleKeyword.type == movieKeyword.type:
                articleSynsets = wordnet.synsets(articleKeyword, NOUN)
                if len(articleSynsets) > 0:
                    articleSynset = movieSynsets[0]
                else:
                    continue
                score = wordnet.similarity(movieSynset,articleSynset)
                print movieSynset, articleSynset, score
                totalScore += score
                comparisons += 1
                
    comparisons = 1 if comparisons == 0 else comparisons
                
    return float(totalScore)/comparisons


def blend(article, movie,adjectives):
    title = movie.title
    #print title
    
    movie_kw = ""
    article_kw = ""
    #Blend article and movie together and return result text
    for key_movie in movie.keywords.all():
        if "PERSON" in key_movie.type:
            movie_kw = key_movie.word
            break
        
    for key_news in article.keywords.all():
        if "PERSON" in key_news.type:
            article_kw = key_news.word 
            break
    print movie_kw, article_kw, title
        
    return re.sub(movie_kw, article_kw, title)
    
