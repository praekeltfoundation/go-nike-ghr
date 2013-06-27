# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.utils import timezone


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Article.created'
        db.delete_column(u'articles_article', 'created')

        # Deleting field 'Article.date_published'
        db.delete_column(u'articles_article', 'date_published')

        # Adding field 'Article.publish_at'
        db.add_column(u'articles_article', 'publish_at',
                      self.gf('django.db.models.fields.DateTimeField')(default=timezone.now()),
                      keep_default=False)

        # Adding field 'Article.created_at'
        db.add_column(u'articles_article', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=timezone.now(), blank=True),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Article.created'
        raise RuntimeError("Cannot reverse this migration. 'Article.created' and its values cannot be restored.")
        # Adding field 'Article.date_published'
        db.add_column(u'articles_article', 'date_published',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 25, 0, 0)),
                      keep_default=False)

        # Deleting field 'Article.publish_at'
        db.delete_column(u'articles_article', 'publish_at')

        # Deleting field 'Article.created_at'
        db.delete_column(u'articles_article', 'created_at')


    models = {
        u'articles.article': {
            'Meta': {'object_name': 'Article'},
            'article': ('django.db.models.fields.CharField', [], {'max_length': '480'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 27, 0, 0)'})
        }
    }

    complete_apps = ['articles']