from django.db import models

from datetime import datetime

# Create your models here.
class GetOrNoneManager(models.Manager):
    """Manager which overrides Django's standard manager in all of the module's models.
    
    Adds utility functionality into the models.
    """
    def get_or_none(self, **kwargs):
        """Get model object or None is no object matching search criteria is found.
        """
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class Keyword(models.Model):
    # NN/JJ/VB/NE (POS or named entity)
    type = models.CharField(max_length = 20)    
    word = models.CharField(max_length = 100)
    weight = models.PositiveIntegerField(default = 0)
    objects = GetOrNoneManager()
    

class Alias(models.Model):
    name = models.CharField(max_length = 200)


class Person(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    birthday = models.DateField(blank = True, null = True)
    nationality = models.CharField(max_length = 100, blank = True, null = True)
    # (M)ale / (F)emale / (O)ther
    gender = models.CharField(max_length = 1, blank = True, null = True)
    # Positive talk points / attributes
    posattr = models.ManyToManyField(Keyword, related_name = 'posattr+')
    # Negative talk points / attributes
    negattr = models.ManyToManyField(Keyword, related_name = 'negattr+')
    aliases = models.ManyToManyField(Alias, related_name = 'alias+')
    last_usage = models.DateTimeField(auto_now = True, null = True)
    objects = GetOrNoneManager()
    
    
class Movie(models.Model):
    title = models.CharField(max_length = 300)
    short_summary = models.TextField(null = True)
    long_summary = models.TextField(blank = True, null = True)
    genre = models.CharField(max_length = 100)
    url = models.URLField(null = True)
    year = models.IntegerField(blank = True, null = True)
    toplist_pos = models.PositiveIntegerField(blank = True, null = True)
    # Persons who are played by the cast
    persons = models.ManyToManyField(Person, related_name = 'persons+')
    cast = models.ManyToManyField(Person, related_name = 'cast+')
    keywords = models.ManyToManyField(Keyword)
    objects = GetOrNoneManager()
    
    
class Article(models.Model):
    headline = models.CharField(max_length = 500)
    content = models.TextField(null = True)
    url = models.URLField()
    date = models.DateField()
    keywords = models.ManyToManyField(Keyword)
    used = models.BooleanField(default = False)
    objects = GetOrNoneManager()
    
    
class Tweet(models.Model):
    content = models.CharField(max_length = 200)
    date = models.DateTimeField(auto_now_add = True)
    

