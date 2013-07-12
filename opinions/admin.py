from django.contrib import admin
from opinions.models import (Opinion,
                             OpinionPollId,
                             OpinionPollOpinion,
                             OpinionPollChoices)
from django import forms
from django.forms.models import BaseInlineFormSet


class OpinionPollChoicesFormset(BaseInlineFormSet):
    """
    This class handles data that has been cleaned by teh formset
    """
    def clean(self):
        """
        Overiding clean function to check combined char length
        """
        super(OpinionPollChoicesFormset, self).clean()
        char_lim_op = len(self.instance.opinion)  # opinion char length

        number_of_choices = 0  # Variable to ensure atleast one choice is entered
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue

            if ("choices" not in form.cleaned_data and number_of_choices < 1):
                raise forms.ValidationError("You need at least one opinion")
            else:
                if ("choices" in form.cleaned_data):
                    char_lim_op = char_lim_op + len(form.cleaned_data['choices'])
                    if char_lim_op > 160:
                        raise forms.ValidationError("You have gone beyond the"
                                                    " character limit"
                                                    " please shorten opinions"
                                                    " and/or choices")
            number_of_choices = + 1


class OpinionPollChoicesInline(admin.StackedInline):
    model = OpinionPollChoices
    formset = OpinionPollChoicesFormset
    extra = 1


class OpinionAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Overiding the opinion CharField widget to Text Area
        """
        formfield = super(OpinionAdmin, self).formfield_for_dbfield(db_field, **kwargs)

        if db_field.name in ['opinion_1', 'opinion_2', 'opinion_3',
                             'opinion_4', 'opinion_5']:
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield


class OpinionPollIdAdmin(admin.ModelAdmin):
    list_display = ["name", "active"]


class OpinionPollOpinionAdmin(admin.ModelAdmin):
    inlines = [OpinionPollChoicesInline]
    list_display = ["opinion"]

# Registering the Opinion with the admin
admin.site.register(Opinion, OpinionAdmin)
admin.site.register(OpinionPollId, OpinionPollIdAdmin)
admin.site.register(OpinionPollOpinion, OpinionPollOpinionAdmin)
