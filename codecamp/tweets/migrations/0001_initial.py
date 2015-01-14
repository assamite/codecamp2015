# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Keyword'
        db.create_table(u'tweets_keyword', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('word', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('weight', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'tweets', ['Keyword'])

        # Adding model 'Person'
        db.create_table(u'tweets_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=500)),
            ('birthday', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('nationality', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'tweets', ['Person'])

        # Adding M2M table for field posattr on 'Person'
        m2m_table_name = db.shorten_name(u'tweets_person_posattr')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'tweets.person'], null=False)),
            ('keyword', models.ForeignKey(orm[u'tweets.keyword'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'keyword_id'])

        # Adding M2M table for field negattr on 'Person'
        m2m_table_name = db.shorten_name(u'tweets_person_negattr')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'tweets.person'], null=False)),
            ('keyword', models.ForeignKey(orm[u'tweets.keyword'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'keyword_id'])

        # Adding model 'Movie'
        db.create_table(u'tweets_movie', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('short_summary', self.gf('django.db.models.fields.TextField')()),
            ('long_summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('genre', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('year', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('toplist_pos', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
        ))
        db.send_create_signal(u'tweets', ['Movie'])

        # Adding M2M table for field persons on 'Movie'
        m2m_table_name = db.shorten_name(u'tweets_movie_persons')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movie', models.ForeignKey(orm[u'tweets.movie'], null=False)),
            ('person', models.ForeignKey(orm[u'tweets.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['movie_id', 'person_id'])

        # Adding M2M table for field cast on 'Movie'
        m2m_table_name = db.shorten_name(u'tweets_movie_cast')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movie', models.ForeignKey(orm[u'tweets.movie'], null=False)),
            ('person', models.ForeignKey(orm[u'tweets.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['movie_id', 'person_id'])

        # Adding M2M table for field keywords on 'Movie'
        m2m_table_name = db.shorten_name(u'tweets_movie_keywords')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movie', models.ForeignKey(orm[u'tweets.movie'], null=False)),
            ('keyword', models.ForeignKey(orm[u'tweets.keyword'], null=False))
        ))
        db.create_unique(m2m_table_name, ['movie_id', 'keyword_id'])

        # Adding model 'Article'
        db.create_table(u'tweets_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('used', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'tweets', ['Article'])

        # Adding M2M table for field keywords on 'Article'
        m2m_table_name = db.shorten_name(u'tweets_article_keywords')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm[u'tweets.article'], null=False)),
            ('keyword', models.ForeignKey(orm[u'tweets.keyword'], null=False))
        ))
        db.create_unique(m2m_table_name, ['article_id', 'keyword_id'])


    def backwards(self, orm):
        # Deleting model 'Keyword'
        db.delete_table(u'tweets_keyword')

        # Deleting model 'Person'
        db.delete_table(u'tweets_person')

        # Removing M2M table for field posattr on 'Person'
        db.delete_table(db.shorten_name(u'tweets_person_posattr'))

        # Removing M2M table for field negattr on 'Person'
        db.delete_table(db.shorten_name(u'tweets_person_negattr'))

        # Deleting model 'Movie'
        db.delete_table(u'tweets_movie')

        # Removing M2M table for field persons on 'Movie'
        db.delete_table(db.shorten_name(u'tweets_movie_persons'))

        # Removing M2M table for field cast on 'Movie'
        db.delete_table(db.shorten_name(u'tweets_movie_cast'))

        # Removing M2M table for field keywords on 'Movie'
        db.delete_table(db.shorten_name(u'tweets_movie_keywords'))

        # Deleting model 'Article'
        db.delete_table(u'tweets_article')

        # Removing M2M table for field keywords on 'Article'
        db.delete_table(db.shorten_name(u'tweets_article_keywords'))


    models = {
        u'tweets.article': {
            'Meta': {'object_name': 'Article'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tweets.Keyword']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'used': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'tweets.keyword': {
            'Meta': {'object_name': 'Keyword'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'weight': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tweets.movie': {
            'Meta': {'object_name': 'Movie'},
            'cast': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'cast+'", 'symmetrical': 'False', 'to': u"orm['tweets.Person']"}),
            'genre': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tweets.Keyword']", 'symmetrical': 'False'}),
            'long_summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'persons': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'persons+'", 'symmetrical': 'False', 'to': u"orm['tweets.Person']"}),
            'short_summary': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'toplist_pos': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'year': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        u'tweets.person': {
            'Meta': {'object_name': 'Person'},
            'birthday': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500'}),
            'nationality': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'negattr': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'negattr+'", 'symmetrical': 'False', 'to': u"orm['tweets.Keyword']"}),
            'posattr': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'posattr+'", 'symmetrical': 'False', 'to': u"orm['tweets.Keyword']"})
        }
    }

    complete_apps = ['tweets']