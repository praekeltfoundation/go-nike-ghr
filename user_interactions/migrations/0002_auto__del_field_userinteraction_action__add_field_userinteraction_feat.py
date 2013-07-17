# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'UserInteraction.action'
        db.delete_column(u'user_interactions_userinteraction', 'action')

        # Adding field 'UserInteraction.feature'
        db.add_column(u'user_interactions_userinteraction', 'feature',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30),
                      keep_default=False)

        # Adding field 'UserInteraction.key'
        db.add_column(u'user_interactions_userinteraction', 'key',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'UserInteraction.value'
        db.add_column(u'user_interactions_userinteraction', 'value',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'UserInteraction.action'
        db.add_column(u'user_interactions_userinteraction', 'action',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)

        # Deleting field 'UserInteraction.feature'
        db.delete_column(u'user_interactions_userinteraction', 'feature')

        # Deleting field 'UserInteraction.key'
        db.delete_column(u'user_interactions_userinteraction', 'key')

        # Deleting field 'UserInteraction.value'
        db.delete_column(u'user_interactions_userinteraction', 'value')


    models = {
        u'user_interactions.userinteraction': {
            'Meta': {'object_name': 'UserInteraction'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feature': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'msisdn': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'transport': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['user_interactions']