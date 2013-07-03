from django.contrib import admin
from opinions.models import Opinion
from django import forms


class OpinionAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        # Overiding the opinion CharField widget to Text Area
        formfield = super(OpinionAdmin, self).formfield_for_dbfield(db_field, **kwargs)

        if db_field.name in ['opinion_1', 'opinion_2', 'opinion_3',
                             'opinion_4', 'opinion_5']:
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield

# Registering the Article with the admin
admin.site.register(Opinion, OpinionAdmin)
