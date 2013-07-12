# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MonitorAndLearningQuizId.name'
        db.add_column(u'monitor_and_learn_monitorandlearningquizid', 'name',
                      self.gf('django.db.models.fields.CharField')(default='Old Quiz', max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MonitorAndLearningQuizId.name'
        db.delete_column(u'monitor_and_learn_monitorandlearningquizid', 'name')


    models = {
        u'monitor_and_learn.monitorandlearningquizanswer': {
            'Meta': {'object_name': 'MonitorAndLearningQuizAnswer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'question_ids'", 'to': u"orm['monitor_and_learn.MonitorAndLearningQuizQuestion']"})
        },
        u'monitor_and_learn.monitorandlearningquizid': {
            'Meta': {'object_name': 'MonitorAndLearningQuizId'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'monitor_and_learn.monitorandlearningquizquestion': {
            'Meta': {'object_name': 'MonitorAndLearningQuizQuestion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'quiz_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quiz_ids'", 'to': u"orm['monitor_and_learn.MonitorAndLearningQuizId']"})
        }
    }

    complete_apps = ['monitor_and_learn']