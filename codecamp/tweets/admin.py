from django.contrib import admin

from models import Movie, Person, Article, Keyword
# Register your models here.

admin.site.register(Movie)
admin.site.register(Person)
admin.site.register(Article)
admin.site.register(Keyword)