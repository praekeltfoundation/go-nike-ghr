# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Article.status'
        db.alter_column(u'articles_article', 'status', self.gf('django.db.models.fields.CharField')(max_length=8))

    def backwards(self, orm):

        # Changing field 'Article.status'
        db.alter_column(u'articles_article', 'status', self.gf('django.db.models.fields.BooleanField')())

    models = {
        u'articles.article': {
            'Meta': {'object_name': 'Article'},
            'article': ('django.db.models.fields.CharField', [], {'max_length': '480'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 25, 0, 0)'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        }
    }

    complete_apps = ['articles']