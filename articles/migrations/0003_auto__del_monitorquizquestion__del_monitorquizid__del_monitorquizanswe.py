# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'MonitorQuizQuestion'
        db.delete_table(u'articles_monitorquizquestion')

        # Deleting model 'MonitorQuizId'
        db.delete_table(u'articles_monitorquizid')

        # Deleting model 'MonitorQuizAnswer'
        db.delete_table(u'articles_monitorquizanswer')

        # Adding model 'MonitorAndLearningQuizAnswer'
        db.create_table(u'articles_monitorandlearningquizanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.MonitorAndLearningQuizQuestion'])),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=160)),
        ))
        db.send_create_signal(u'articles', ['MonitorAndLearningQuizAnswer'])

        # Adding model 'MonitorAndLearningQuizQuestion'
        db.create_table(u'articles_monitorandlearningquizquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quiz_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.MonitorAndLearningQuizId'])),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=160)),
        ))
        db.send_create_signal(u'articles', ['MonitorAndLearningQuizQuestion'])

        # Adding model 'MonitorAndLearningQuizId'
        db.create_table(u'articles_monitorandlearningquizid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'articles', ['MonitorAndLearningQuizId'])


    def backwards(self, orm):
        # Adding model 'MonitorQuizQuestion'
        db.create_table(u'articles_monitorquizquestion', (
            ('quiz_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.MonitorQuizId'])),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=160)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'articles', ['MonitorQuizQuestion'])

        # Adding model 'MonitorQuizId'
        db.create_table(u'articles_monitorquizid', (
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'articles', ['MonitorQuizId'])

        # Adding model 'MonitorQuizAnswer'
        db.create_table(u'articles_monitorquizanswer', (
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=160)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.MonitorQuizQuestion'])),
        ))
        db.send_create_signal(u'articles', ['MonitorQuizAnswer'])

        # Deleting model 'MonitorAndLearningQuizAnswer'
        db.delete_table(u'articles_monitorandlearningquizanswer')

        # Deleting model 'MonitorAndLearningQuizQuestion'
        db.delete_table(u'articles_monitorandlearningquizquestion')

        # Deleting model 'MonitorAndLearningQuizId'
        db.delete_table(u'articles_monitorandlearningquizid')


    models = {
        u'articles.article': {
            'Meta': {'object_name': 'Article'},
            'article': ('django.db.models.fields.CharField', [], {'max_length': '480'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'articles.monitorandlearningquizanswer': {
            'Meta': {'object_name': 'MonitorAndLearningQuizAnswer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['articles.MonitorAndLearningQuizQuestion']"})
        },
        u'articles.monitorandlearningquizid': {
            'Meta': {'object_name': 'MonitorAndLearningQuizId'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'articles.monitorandlearningquizquestion': {
            'Meta': {'object_name': 'MonitorAndLearningQuizQuestion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'quiz_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['articles.MonitorAndLearningQuizId']"})
        }
    }

    complete_apps = ['articles']