from django.contrib import admin
from models import MonitorAndLearningQuizId, MonitorAndLearningQuizQuestion, MonitorAndLearningQuizAnswer
from django import forms
from django.forms.models import BaseInlineFormSet


class QuestionAdminForm(forms.ModelForm):
    # quiz_id = forms.CharField(max_length=255, initial="quiz_1",
    #                           widget=forms.TextInput(attrs={"readonly": "readonly"}))
    # print dir(forms.CharField(max_length=255))
    def __init__(self, *args, **kwargs):
        super(QuestionAdminForm, self).__init__(*args, **kwargs)
        choices = [self.fields["quiz_id"].choices.__iter__().next()]
        choices.pop()

        choices.append((1, "quiz_1"))
        self.fields['quiz_id'].choices = choices


class MonitorAndLearningQuizAnswerFormset(BaseInlineFormSet):
    # Validating the formset data

    def clean(self):
        super(MonitorAndLearningQuizAnswerFormset, self).clean()

        char_limit = len(self.instance.question)
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            form.cleaned_data['answer']
            char_limit = char_limit + len(form.cleaned_data['answer'])

            if char_limit > 160:
                raise forms.ValidationError("You have gone beyond the character limit"
                                            " please shorten questions and/or answers")


class MonitorAndLearningQuizAnswerInline(admin.StackedInline):
    model = MonitorAndLearningQuizAnswer
    extra = 3
    max_num = 3
    formset = MonitorAndLearningQuizAnswerFormset


class MonitorAndLearningQuizIdAdmin(admin.ModelAdmin):
    pass


class MonitorAndLearningQuizQuestionAdmin(admin.ModelAdmin):
    inlines = [MonitorAndLearningQuizAnswerInline]
    form = QuestionAdminForm


admin.site.register(MonitorAndLearningQuizId, MonitorAndLearningQuizIdAdmin)
admin.site.register(MonitorAndLearningQuizQuestion, MonitorAndLearningQuizQuestionAdmin)
