# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserInteraction'
        db.create_table(u'user_interactions_userinteraction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('msisdn', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('transport', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'user_interactions', ['UserInteraction'])


    def backwards(self, orm):
        # Deleting model 'UserInteraction'
        db.delete_table(u'user_interactions_userinteraction')


    models = {
        u'user_interactions.userinteraction': {
            'Meta': {'object_name': 'UserInteraction'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'msisdn': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'transport': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        }
    }

    complete_apps = ['user_interactions']