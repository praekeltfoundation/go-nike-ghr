# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MonitorQuizQuestion'
        db.create_table(u'articles_monitorquizquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quiz_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.MonitorQuizId'])),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=160)),
        ))
        db.send_create_signal(u'articles', ['MonitorQuizQuestion'])

        # Adding model 'MonitorQuizId'
        db.create_table(u'articles_monitorquizid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'articles', ['MonitorQuizId'])

        # Adding model 'MonitorQuizAnswer'
        db.create_table(u'articles_monitorquizanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.MonitorQuizQuestion'])),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=160)),
        ))
        db.send_create_signal(u'articles', ['MonitorQuizAnswer'])


    def backwards(self, orm):
        # Deleting model 'MonitorQuizQuestion'
        db.delete_table(u'articles_monitorquizquestion')

        # Deleting model 'MonitorQuizId'
        db.delete_table(u'articles_monitorquizid')

        # Deleting model 'MonitorQuizAnswer'
        db.delete_table(u'articles_monitorquizanswer')


    models = {
        u'articles.article': {
            'Meta': {'object_name': 'Article'},
            'article': ('django.db.models.fields.CharField', [], {'max_length': '480'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'articles.monitorquizanswer': {
            'Meta': {'object_name': 'MonitorQuizAnswer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['articles.MonitorQuizQuestion']"})
        },
        u'articles.monitorquizid': {
            'Meta': {'object_name': 'MonitorQuizId'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'articles.monitorquizquestion': {
            'Meta': {'object_name': 'MonitorQuizQuestion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'quiz_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['articles.MonitorQuizId']"})
        }
    }

    complete_apps = ['articles']