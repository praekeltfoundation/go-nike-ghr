from django.contrib import admin
from models import MonitorAndLearningQuizId, MonitorAndLearningQuizQuestion, MonitorAndLearningQuizAnswer
from django import forms
from django.forms.models import BaseInlineFormSet


class QuestionAdminForm(forms.ModelForm):
    # This form checks to see if there are any uncompleted quizes (< 4 questions),
    # if so sets current ID to the uncompleted quiz_id
    def __init__(self, *args, **kwargs):
        super(QuestionAdminForm, self).__init__(*args, **kwargs)
        choices = [self.fields["quiz_id"].choices.__iter__().next()]
        choices.pop()
        query = MonitorAndLearningQuizId.objects.all().filter(completed=False)
        print query
        if query.exists():
            choices.append((query[0].pk, 'Quiz %s' % query[0].pk.__str__()))

        self.fields['quiz_id'].choices = choices


class MonitorAndLearningQuizAnswerFormset(BaseInlineFormSet):
    # This class validates the formset model

    def clean(self):
        # Overiding the clean function so that the max length can be chekced
        super(MonitorAndLearningQuizAnswerFormset, self).clean()

        char_limit = len(self.instance.question)
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            if "answer" not in form.cleaned_data:
                raise forms.ValidationError("You need to complete the answers")

            form.cleaned_data['answer']
            char_limit = char_limit + len(form.cleaned_data['answer'])

            if char_limit > 160:
                raise forms.ValidationError("You have gone beyond the character limit"
                                            " please shorten questions and/or answers")

        query = MonitorAndLearningQuizQuestion.objects.all().filter(quiz_id=self.instance.quiz_id)
        print self.instance.quiz_id

        if len(query) >= 3:
            query = MonitorAndLearningQuizId.objects.get(pk=self.instance.quiz_id.id)
            query.completed = True
            query.save()


class MonitorAndLearningQuizAnswerInline(admin.StackedInline):
    # This class sets the answers to be on the same page as teh parent question
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
