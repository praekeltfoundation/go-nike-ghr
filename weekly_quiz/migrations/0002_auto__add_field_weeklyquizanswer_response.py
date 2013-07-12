# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'WeeklyQuizAnswer.response'
        db.add_column(u'weekly_quiz_weeklyquizanswer', 'response',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=160),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'WeeklyQuizAnswer.response'
        db.delete_column(u'weekly_quiz_weeklyquizanswer', 'response')


    models = {
        u'weekly_quiz.weeklyquizanswer': {
            'Meta': {'object_name': 'WeeklyQuizAnswer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wq_question_id'", 'to': u"orm['weekly_quiz.WeeklyQuizQuestion']"}),
            'response': ('django.db.models.fields.CharField', [], {'max_length': '160'})
        },
        u'weekly_quiz.weeklyquizid': {
            'Meta': {'object_name': 'WeeklyQuizId'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'weekly_quiz.weeklyquizquestion': {
            'Meta': {'object_name': 'WeeklyQuizQuestion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'quiz_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wq_quiz_id'", 'to': u"orm['weekly_quiz.WeeklyQuizId']"})
        }
    }

    complete_apps = ['weekly_quiz']