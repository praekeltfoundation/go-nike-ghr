# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OpinionPollChoices'
        db.create_table(u'opinions_opinionpollchoices', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('opinionpollopinion', self.gf('django.db.models.fields.related.ForeignKey')(related_name='opinionpollopinion', to=orm['opinions.OpinionPollOpinion'])),
            ('choices', self.gf('django.db.models.fields.CharField')(max_length=160)),
        ))
        db.send_create_signal(u'opinions', ['OpinionPollChoices'])

        # Adding model 'OpinionPollOpinion'
        db.create_table(u'opinions_opinionpollopinion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('opinionpollid', self.gf('django.db.models.fields.related.ForeignKey')(related_name='opinionpollid', to=orm['opinions.OpinionPollId'])),
            ('opinion', self.gf('django.db.models.fields.CharField')(max_length=160)),
        ))
        db.send_create_signal(u'opinions', ['OpinionPollOpinion'])

        # Adding model 'OpinionPollId'
        db.create_table(u'opinions_opinionpollid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'opinions', ['OpinionPollId'])


    def backwards(self, orm):
        # Deleting model 'OpinionPollChoices'
        db.delete_table(u'opinions_opinionpollchoices')

        # Deleting model 'OpinionPollOpinion'
        db.delete_table(u'opinions_opinionpollopinion')

        # Deleting model 'OpinionPollId'
        db.delete_table(u'opinions_opinionpollid')


    models = {
        u'opinions.opinion': {
            'Meta': {'object_name': 'Opinion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opinion_1': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'opinion_2': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'opinion_3': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'opinion_4': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'opinion_5': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'opinions.opinionpollchoices': {
            'Meta': {'object_name': 'OpinionPollChoices'},
            'choices': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opinionpollopinion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'opinionpollopinion'", 'to': u"orm['opinions.OpinionPollOpinion']"})
        },
        u'opinions.opinionpollid': {
            'Meta': {'object_name': 'OpinionPollId'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'opinions.opinionpollopinion': {
            'Meta': {'object_name': 'OpinionPollOpinion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opinion': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'opinionpollid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'opinionpollid'", 'to': u"orm['opinions.OpinionPollId']"})
        }
    }

    complete_apps = ['opinions']