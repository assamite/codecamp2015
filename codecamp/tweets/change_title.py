from models import Keyword

def change_title (keywords_movie,keywords_news):   
    for key_movie in keywords_movie:
        if "PERSON" in key_movie.type:
            for key_news in keywords_news:
                if "PERSON" in key_news.type
                    key_movie.word = key_news.word
                    break
    
    return
    