from django.contrib import admin
from opinions.models import (Opinion,
                             OpinionPollId,
                             OpinionPollOpinion,
                             OpinionPollChoices)
from django import forms
from django.forms.models import BaseInlineFormSet

class OpinionPollIdForms(forms.ModelForm):
    pass


class OpinionPollOpinionForms(forms.ModelForm):
    pass


class OpinionPollChoicesFormset(BaseInlineFormSet):
    pass


class OpinionPollChoicesInline(admin.StackedInline):
    model = OpinionPollChoices
    formset = OpinionPollChoicesFormset
    extra = 1


class OpinionAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        # Overiding the opinion CharField widget to Text Area
        formfield = super(OpinionAdmin, self).formfield_for_dbfield(db_field, **kwargs)

        if db_field.name in ['opinion_1', 'opinion_2', 'opinion_3',
                             'opinion_4', 'opinion_5']:
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield


class OpinionPollIdAdmin(admin.ModelAdmin):
    list_display = ["name", "active"]


class OpinionPollOpinionAdmin(admin.ModelAdmin):
    inlines = [OpinionPollChoicesInline]
    form = OpinionPollOpinionForms
    list_display = ["opinion"]

# Registering the Opinion with the admin
admin.site.register(Opinion, OpinionAdmin)
admin.site.register(OpinionPollId, OpinionPollIdAdmin)
admin.site.register(OpinionPollOpinion, OpinionPollOpinionAdmin)
