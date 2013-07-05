# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Article.article'
        db.delete_column(u'articles_article', 'article')

        # Adding field 'Article.page_1'
        db.add_column(u'articles_article', 'page_1',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=125),
                      keep_default=False)

        # Adding field 'Article.page_2'
        db.add_column(u'articles_article', 'page_2',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=125),
                      keep_default=False)

        # Adding field 'Article.page_3'
        db.add_column(u'articles_article', 'page_3',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=125),
                      keep_default=False)

        # Adding field 'Article.page_4'
        db.add_column(u'articles_article', 'page_4',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=125),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Article.article'
        db.add_column(u'articles_article', 'article',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=480),
                      keep_default=False)

        # Deleting field 'Article.page_1'
        db.delete_column(u'articles_article', 'page_1')

        # Deleting field 'Article.page_2'
        db.delete_column(u'articles_article', 'page_2')

        # Deleting field 'Article.page_3'
        db.delete_column(u'articles_article', 'page_3')

        # Deleting field 'Article.page_4'
        db.delete_column(u'articles_article', 'page_4')


    models = {
        u'articles.article': {
            'Meta': {'object_name': 'Article'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_1': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'page_2': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'page_3': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'page_4': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        }
    }

    complete_apps = ['articles']