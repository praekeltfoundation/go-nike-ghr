# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MonitorAndLearningQuizId'
        db.create_table(u'monitor_and_learn_monitorandlearningquizid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'monitor_and_learn', ['MonitorAndLearningQuizId'])

        # Adding model 'MonitorAndLearningQuizQuestion'
        db.create_table(u'monitor_and_learn_monitorandlearningquizquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quiz_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monitor_and_learn.MonitorAndLearningQuizId'])),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=160)),
        ))
        db.send_create_signal(u'monitor_and_learn', ['MonitorAndLearningQuizQuestion'])

        # Adding model 'MonitorAndLearningQuizAnswer'
        db.create_table(u'monitor_and_learn_monitorandlearningquizanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monitor_and_learn.MonitorAndLearningQuizQuestion'])),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=160)),
        ))
        db.send_create_signal(u'monitor_and_learn', ['MonitorAndLearningQuizAnswer'])


    def backwards(self, orm):
        # Deleting model 'MonitorAndLearningQuizId'
        db.delete_table(u'monitor_and_learn_monitorandlearningquizid')

        # Deleting model 'MonitorAndLearningQuizQuestion'
        db.delete_table(u'monitor_and_learn_monitorandlearningquizquestion')

        # Deleting model 'MonitorAndLearningQuizAnswer'
        db.delete_table(u'monitor_and_learn_monitorandlearningquizanswer')


    models = {
        u'monitor_and_learn.monitorandlearningquizanswer': {
            'Meta': {'object_name': 'MonitorAndLearningQuizAnswer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitor_and_learn.MonitorAndLearningQuizQuestion']"})
        },
        u'monitor_and_learn.monitorandlearningquizid': {
            'Meta': {'object_name': 'MonitorAndLearningQuizId'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'monitor_and_learn.monitorandlearningquizquestion': {
            'Meta': {'object_name': 'MonitorAndLearningQuizQuestion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'quiz_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitor_and_learn.MonitorAndLearningQuizId']"})
        }
    }

    complete_apps = ['monitor_and_learn']