def assess_quality (keywords):
    quality = 0
    for key in keywords:
        if "PERS" in key.tag:
            quality =1
            break
    
    return quality
