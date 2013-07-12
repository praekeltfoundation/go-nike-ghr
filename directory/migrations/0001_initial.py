# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'directory_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal(u'directory', ['Category'])

        # Adding model 'SubCategory'
        db.create_table(u'directory_subcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='category', to=orm['directory.Category'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('content_1', self.gf('django.db.models.fields.CharField')(max_length=125)),
        ))
        db.send_create_signal(u'directory', ['SubCategory'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'directory_category')

        # Deleting model 'SubCategory'
        db.delete_table(u'directory_subcategory')


    models = {
        u'directory.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'directory.subcategory': {
            'Meta': {'object_name': 'SubCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'category'", 'to': u"orm['directory.Category']"}),
            'content_1': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '125'})
        }
    }

    complete_apps = ['directory']