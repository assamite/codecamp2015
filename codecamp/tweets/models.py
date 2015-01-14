from django.db import models

# Create your models here.

class Keyword(models.Model):
    # NN/JJ/VB/NE (POS or named entity)
    type = models.CharField(max_length = 20)    
    word = models.CharField(max_length = 100)
    weight = models.PositiveIntegerField(default = 0)


class Person(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    birthday = models.DateField(blank = True)
    nationality = models.CharField(max_length = 100, blank = True)
    # (M)ale / (F)emale / (O)ther
    gender = models.CharField(max_length = 1)
    # Positive talk points / attributes
    posattr = models.ManyToManyField(Keyword, related_name = 'posattr+')
    # Negative talk points / attributes
    negattr = models.ManyToManyField(Keyword, related_name = 'negattr+')
    
    
class Movie(models.Model):
    title = models.CharField(max_length = 300)
    short_summary = models.TextField()
    long_summary = models.TextField(blank = True)
    genre = models.CharField(max_length = 100)
    url = models.URLField()
    year = models.IntegerField(blank = True)
    toplist_pos = models.PositiveIntegerField(blank = True)
    # Persons who are played by the cast
    persons = models.ManyToManyField(Person, related_name = 'persons+')
    cast = models.ManyToManyField(Person, related_name = 'cast+')
    keywords = models.ManyToManyField(Keyword)
    
    
class Article(models.Model):
    headline = models.CharField(max_length = 500)
    content = models.TextField()
    url = models.URLField()
    date = models.DateField()
    keywords = models.ManyToManyField(Keyword)
    used = models.BooleanField(default = False)
    
