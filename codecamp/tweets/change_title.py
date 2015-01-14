def change_title (keywords_movie,keywords_news):   
    for key_movie in keywords_movie:
        if "PERS" in key_movie.tag:
            for key_news in keywords_news:
                if "PERS" in key_news.tag
                    key_movie.word = key_news.word
                    break
    
    return
    