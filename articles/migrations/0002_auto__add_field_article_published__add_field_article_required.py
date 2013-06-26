# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.utils import timezone


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Article.published'
        db.add_column(u'articles_article', 'published',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=timezone.now(), blank=True),
                      keep_default=False)

        # Adding field 'Article.required'
        db.add_column(u'articles_article', 'required',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Article.published'
        db.delete_column(u'articles_article', 'published')

        # Deleting field 'Article.required'
        db.delete_column(u'articles_article', 'required')


    models = {
        u'articles.article': {
            'Meta': {'object_name': 'Article'},
            'article': ('django.db.models.fields.CharField', [], {'max_length': '480'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['articles']