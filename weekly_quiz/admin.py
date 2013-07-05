from django.contrib import admin
from models import (WeeklyQuizId,
                    WeeklyQuizQuestion,
                    WeeklyQuizAnswer)
from django import forms
from django.forms.models import BaseInlineFormSet


class WeeklyQuizQuestionAdminForm(forms.ModelForm):
    # This form checks to see if there are any uncompleted quizzes
    #  (< 4 questions), if so sets current ID to the uncompleted quiz_id.
    # If editing sets the current quiz id  to be edited
    def __init__(self, *args, **kwargs):
        super(WeeklyQuizQuestionAdminForm, self).__init__(*args, **kwargs)
        choices = [self.fields["quiz_id"].choices.__iter__().next()]
        choices.pop()
        query = (WeeklyQuizId.objects.all().
                 filter(completed=False).order_by('pk'))

        if 'question' in self.initial:
            get = query = WeeklyQuizId.objects.get(pk=
                                                   self.initial['quiz_id'])
            choices.append((self.initial['quiz_id'], get.name))
        else:
            if query.exists():
                for item in range(len(query)):
                    choices.append((query[item].pk, query[item].name))

        self.fields['quiz_id'].choices = choices


class WeeklyQuizIdAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(WeeklyQuizIdAdminForm, self).__init__(*args, **kwargs)

    class Meta:
        model = WeeklyQuizId

    def clean(self, *args, **kwargs):
        #  Checking the active field vs number of questions completed
        #  to see if quiz should be activated
        cleaned_data = super(WeeklyQuizIdAdminForm, self).clean(*args, **kwargs)

        if cleaned_data['active']:
            query = (WeeklyQuizQuestion.objects.
                     all().filter(quiz_id_id=self.instance.id))
            print query
            if len(query) != 3:
                raise forms.ValidationError("This quiz has less than 3 "
                                            "questions, finish questions to "
                                            "activate")
        return cleaned_data


class WeeklyQuizAnswerFormset(BaseInlineFormSet):
    # This class validates the formset model and checks for max_length

    def clean(self):
        # Overiding the clean function so that the max length can be chekced
        # also checks if the answer has been submitted and Foreign key has
        # been included
        super(WeeklyQuizAnswerFormset, self).clean()
        char_limit = len(self.instance.question)
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue

            if ("answer" not in form.cleaned_data):
                raise forms.ValidationError("You need to complete the answers")
            else:
                if "answer" in form.cleaned_data:
                    char_limit = char_limit + len(form.cleaned_data['answer'])

                    if char_limit > 160:
                        raise forms.ValidationError("You have gone beyond the"
                                                    " character limit"
                                                    " please shorten questions"
                                                    " and/or answers")

        try:
        # Checking if Foreign ID has been included otherwise gives
        # an DoesNotExist exception, despite the validation been active
            query = (WeeklyQuizQuestion.objects.all().
                     filter(quiz_id=self.instance.quiz_id))
            if len(query) >= 2:
                query = (WeeklyQuizId.objects.
                         get(pk=self.instance.quiz_id.id))
                query.completed = True
                query.save()
        except:
            pass


class WeeklyQuizAnswerInline(admin.StackedInline):
    # This class sets the answers to be on the same page as the parent question
    model = WeeklyQuizAnswer
    extra = 3
    max_num = 3
    formset = WeeklyQuizAnswerFormset


class WeeklyQuizIdAdmin(admin.ModelAdmin):
    list_display = ["name", "active", "completed"]
    form = WeeklyQuizIdAdminForm


class WeeklyQuizQuestionAdmin(admin.ModelAdmin):
    # The admin class that adds extra fields to the QuestionAdmin Section
    inlines = [WeeklyQuizAnswerInline]
    form = WeeklyQuizQuestionAdminForm
    list_display = ["question", "quiz_id"]


admin.site.register(WeeklyQuizId, WeeklyQuizIdAdmin)
admin.site.register(WeeklyQuizQuestion, WeeklyQuizQuestionAdmin)
