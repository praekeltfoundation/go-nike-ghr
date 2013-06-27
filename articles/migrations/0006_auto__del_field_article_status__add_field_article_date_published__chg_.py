# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.utils import timezone


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Article.status'
        db.delete_column(u'articles_article', 'status')

        # Adding field 'Article.date_published'
        db.add_column(u'articles_article', 'date_published',
                      self.gf('django.db.models.fields.DateTimeField')(default=timezone.now()),
                      keep_default=False)


        # Changing field 'Article.publish'
        db.delete_column(u'articles_article', 'status')
        db.add_column(u'articles_article', 'publish',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

    def backwards(self, orm):
        # Adding field 'Article.status'
        db.add_column(u'articles_article', 'status',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=8),
                      keep_default=False)

        # Deleting field 'Article.date_published'
        db.delete_column(u'articles_article', 'date_published')

        # Changing field 'Article.publish'
        db.delete_column(u'articles_article', 'publish')
        db.add_column(u'articles_article', 'status',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

    models = {
        u'articles.article': {
            'Meta': {'object_name': 'Article'},
            'article': ('django.db.models.fields.CharField', [], {'max_length': '480'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_published': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 25, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['articles']