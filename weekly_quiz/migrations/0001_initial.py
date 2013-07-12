# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WeeklyQuizId'
        db.create_table(u'weekly_quiz_weeklyquizid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'weekly_quiz', ['WeeklyQuizId'])

        # Adding model 'WeeklyQuizQuestion'
        db.create_table(u'weekly_quiz_weeklyquizquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quiz_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='weekly_quiz_question', to=orm['weekly_quiz.WeeklyQuizId'])),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=160)),
        ))
        db.send_create_signal(u'weekly_quiz', ['WeeklyQuizQuestion'])

        # Adding model 'WeeklyQuizAnswer'
        db.create_table(u'weekly_quiz_weeklyquizanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='weekly_quiz_answer', to=orm['weekly_quiz.WeeklyQuizQuestion'])),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=160)),
        ))
        db.send_create_signal(u'weekly_quiz', ['WeeklyQuizAnswer'])


    def backwards(self, orm):
        # Deleting model 'WeeklyQuizId'
        db.delete_table(u'weekly_quiz_weeklyquizid')

        # Deleting model 'WeeklyQuizQuestion'
        db.delete_table(u'weekly_quiz_weeklyquizquestion')

        # Deleting model 'WeeklyQuizAnswer'
        db.delete_table(u'weekly_quiz_weeklyquizanswer')


    models = {
        u'weekly_quiz.weeklyquizanswer': {
            'Meta': {'object_name': 'WeeklyQuizAnswer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'weekly_quiz_answer'", 'to': u"orm['weekly_quiz.WeeklyQuizQuestion']"})
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
            'quiz_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'weekly_quiz_question'", 'to': u"orm['weekly_quiz.WeeklyQuizId']"})
        }
    }

    complete_apps = ['weekly_quiz']