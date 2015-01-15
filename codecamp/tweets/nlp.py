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

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
 
     # len(s1) >= len(s2)
    if len(s2) == 0:
         return len(s1)
 
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]


def similarwords(word, adjectives):
    #READ THE FILE
    #SEARCH THE TERM IN COLUMN N. 1
    #TAKE THE MOST SIMILAR ADJECTIVE: look similarity numbers
   
    l = adjectives[word]
    final_adj = ""
    if(len(l)>0):
        final_adj = l[0]
        max_score = l[0][1]
        for adj in l:
            if adj[1]>=max_score:
                final_adj=adj
    return final_adj
    
    
#def blend(article, movie):
def blend(article, movie, adjectives):
      
    blended = ""
    flag = 0
    
    #Blend article and movie together and return result text
    title = movie.title
    noun_needed = ""
    movie_kw = ""
    article_kw = ""
    adj_candidates = list()
    noun_candidates = list()
    alias_list = list()
    rank_min = 10000;
    #Blend article and movie together and return result text
    
    #Case that we can exchange Person in the article by Person in the movie
    for key_movie in movie.keywords.all():
        if "PERSON" in key_movie.type:
            movie_kw = key_movie.word
            alias_list = io.queryFreebaseAliases(movie_kw)
            flag = 1
            break
    
    if flag == 1:
        flag = 0
        for key_news in article.keywords.all():
            if "PERSON" in key_news.type:
                for alias in alias_list:
                    rank=levenshtein(alias,key_news.word)
                    if rank < rank_min:
                        rank_min = rank
                        article_kw = alias 
                flag = 1
                break
        if flag == 1:
            #       print "ME VOYYYY"
            return re.sub(movie_kw, article_kw, title)  #END CASE PERSON
    
    else:   
        #  if flag == 0:
        for key_movie in movie.keywords.all():
            if "N" in key_movie.type: #We take the first noun in the movie title
                movie_kw = key_movie.word
                
         #Case where we have an adjective in the article        
        for key_article in article.keywords.all():
            if "J" in key_article.type:           
                article_kw = key_article.word
               
                #measure similarity??
                #similarity = "0"
                #adj_candidates.append([key_article.word, similarity])
                flag =2
                break;
    #Case where we have nouns in the article 
    if flag != 2:
        for key_article in article.keywords.all():
            if key_article.word not in movie.title:
                if "NN" == key_article.type or "NNS"== key_article.type:
                    #Similarity words
              #      print "HOLAAAA"+key_article.word
                    adj_list = similarwords(key_article.word, adjectives)
                    
                    #Save the adj
                    article_kw = adj_list[0]
                    #article_kw = key_article.word
                    break;

    print re.sub(movie_kw, article_kw+" "+movie_kw, title)
    return re.sub(movie_kw, article_kw+" "+movie_kw, title)

    
