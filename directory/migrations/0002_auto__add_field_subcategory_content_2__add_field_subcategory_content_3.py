# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SubCategory.content_2'
        db.add_column(u'directory_subcategory', 'content_2',
                      self.gf('django.db.models.fields.CharField')(default='C', max_length=125),
                      keep_default=False)

        # Adding field 'SubCategory.content_3'
        db.add_column(u'directory_subcategory', 'content_3',
                      self.gf('django.db.models.fields.CharField')(default='D', max_length=125),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SubCategory.content_2'
        db.delete_column(u'directory_subcategory', 'content_2')

        # Deleting field 'SubCategory.content_3'
        db.delete_column(u'directory_subcategory', 'content_3')


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
            'content_2': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'content_3': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '125'})
        }
    }

    complete_apps = ['directory']