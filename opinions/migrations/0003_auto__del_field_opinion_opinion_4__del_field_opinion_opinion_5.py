# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Opinion.opinion_4'
        db.delete_column(u'opinions_opinion', 'opinion_4')

        # Deleting field 'Opinion.opinion_5'
        db.delete_column(u'opinions_opinion', 'opinion_5')


    def backwards(self, orm):
        # Adding field 'Opinion.opinion_4'
        db.add_column(u'opinions_opinion', 'opinion_4',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=125),
                      keep_default=False)

        # Adding field 'Opinion.opinion_5'
        db.add_column(u'opinions_opinion', 'opinion_5',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=125),
                      keep_default=False)


    models = {
        u'opinions.opinion': {
            'Meta': {'object_name': 'Opinion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opinion_1': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'opinion_2': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'opinion_3': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
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
            'active': ('django.db.models.fields.BooleanField', [], {}),
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