# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.utils import timezone


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Article.published'
        db.delete_column(u'articles_article', 'published')

        # Adding field 'Article.publish'
        db.add_column(u'articles_article', 'publish',
                      self.gf('django.db.models.fields.DateTimeField')(default=timezone.now()),
                      keep_default=False)

        # Adding field 'Article.created'
        db.add_column(u'articles_article', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=timezone.now(), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Article.published'
        db.add_column(u'articles_article', 'published',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=timezone.now(), blank=True),
                      keep_default=False)

        # Deleting field 'Article.publish'
        db.delete_column(u'articles_article', 'publish')

        # Deleting field 'Article.created'
        db.delete_column(u'articles_article', 'created')


    models = {
        u'articles.article': {
            'Meta': {'object_name': 'Article'},
            'article': ('django.db.models.fields.CharField', [], {'max_length': '480'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['articles']