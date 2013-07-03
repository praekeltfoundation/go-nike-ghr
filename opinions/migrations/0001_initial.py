# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Article'
        db.create_table(u'opinions_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('opinion_1', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('opinion_2', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('opinion_3', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('opinion_4', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('opinion_5', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'opinions', ['Article'])


    def backwards(self, orm):
        # Deleting model 'Article'
        db.delete_table(u'opinions_article')


    models = {
        u'opinions.article': {
            'Meta': {'object_name': 'Article'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opinion_1': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'opinion_2': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'opinion_3': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'opinion_4': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'opinion_5': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        }
    }

    complete_apps = ['opinions']