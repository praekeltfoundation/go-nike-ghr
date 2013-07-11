# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'MonitorAndLearningQuizAnswer'
        db.delete_table(u'articles_monitorandlearningquizanswer')

        # Deleting model 'MonitorAndLearningQuizQuestion'
        db.delete_table(u'articles_monitorandlearningquizquestion')

        # Deleting model 'MonitorAndLearningQuizId'
        db.delete_table(u'articles_monitorandlearningquizid')


    def backwards(self, orm):
        # Adding model 'MonitorAndLearningQuizAnswer'
        db.create_table(u'articles_monitorandlearningquizanswer', (
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=160)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.MonitorAndLearningQuizQuestion'])),
        ))
        db.send_create_signal(u'articles', ['MonitorAndLearningQuizAnswer'])

        # Adding model 'MonitorAndLearningQuizQuestion'
        db.create_table(u'articles_monitorandlearningquizquestion', (
            ('quiz_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.MonitorAndLearningQuizId'])),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=160)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'articles', ['MonitorAndLearningQuizQuestion'])

        # Adding model 'MonitorAndLearningQuizId'
        db.create_table(u'articles_monitorandlearningquizid', (
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'articles', ['MonitorAndLearningQuizId'])


    models = {
        u'articles.article': {
            'Meta': {'object_name': 'Article'},
            'article': ('django.db.models.fields.CharField', [], {'max_length': '480'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        }
    }

    complete_apps = ['articles']