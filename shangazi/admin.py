from django.contrib import admin
from shangazi.models import Shangazi
from django import forms


class ShangaziAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        # Overiding the page CharField widget to Text Area
        formfield = super(ShangaziAdmin, self).formfield_for_dbfield(db_field, **kwargs)

        if db_field.name in['page_1', 'page_2', 'page_3', 'page_4']:
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield

# Registering the Shangazi model with the admin
admin.site.register(Shangazi, ShangaziAdmin)
