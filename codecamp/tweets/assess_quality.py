from models import Keyword

def assess_quality (keywords):
    quality = 0
    for key in keywords:
        if "PERSON" in key.type:
            quality =1
            break
    
    return quality
