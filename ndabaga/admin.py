from django.contrib import admin
from ndabaga.models import Ndabaga
from django import forms


class NdabagaAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        # Overiding the page CharField widget to Text Area
        formfield = super(NdabagaAdmin, self).formfield_for_dbfield(db_field, **kwargs)

        if db_field.name in['page_1', 'page_2', 'page_3', 'page_4']:
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield

# Registering the Ndabaga model with the admin
admin.site.register(Ndabaga, NdabagaAdmin)
