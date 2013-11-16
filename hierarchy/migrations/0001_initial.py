# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Province'
        db.create_table(u'hierarchy_province', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'hierarchy', ['Province'])

        # Adding model 'District'
        db.create_table(u'hierarchy_district', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('district_province', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hierarchy.Province'])),
        ))
        db.send_create_signal(u'hierarchy', ['District'])

        # Adding model 'Sector'
        db.create_table(u'hierarchy_sector', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('sector_district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hierarchy.District'])),
        ))
        db.send_create_signal(u'hierarchy', ['Sector'])


    def backwards(self, orm):
        # Deleting model 'Province'
        db.delete_table(u'hierarchy_province')

        # Deleting model 'District'
        db.delete_table(u'hierarchy_district')

        # Deleting model 'Sector'
        db.delete_table(u'hierarchy_sector')


    models = {
        u'hierarchy.district': {
            'Meta': {'object_name': 'District'},
            'district_province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hierarchy.Province']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'hierarchy.province': {
            'Meta': {'object_name': 'Province'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'hierarchy.sector': {
            'Meta': {'object_name': 'Sector'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sector_district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hierarchy.District']"})
        }
    }

    complete_apps = ['hierarchy']