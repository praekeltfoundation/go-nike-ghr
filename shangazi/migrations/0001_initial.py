# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Shangazi'
        db.create_table(u'shangazi_shangazi', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page_1', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('page_2', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('page_3', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('page_4', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('publish', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('publish_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'shangazi', ['Shangazi'])


    def backwards(self, orm):
        # Deleting model 'Shangazi'
        db.delete_table(u'shangazi_shangazi')


    models = {
        u'shangazi.shangazi': {
            'Meta': {'object_name': 'Shangazi'},
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

    complete_apps = ['shangazi']