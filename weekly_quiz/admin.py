from django.contrib import admin
from models import (WeeklyQuizId,
                    WeeklyQuizQuestion,
                    WeeklyQuizAnswer)
from django import forms
from django.forms.models import BaseInlineFormSet


class WeeklyQuizQuestionAdminForm(forms.ModelForm):
    """
    This form checks to see if there are any uncompleted quizzes
    (< 3 questions), if so sets current ID to the uncompleted quiz_id.
    If editing sets the current quiz id  to be edited
    """
    def __init__(self, *args, **kwargs):
        super(WeeklyQuizQuestionAdminForm, self).__init__(*args, **kwargs)
        choices = []
        query = (WeeklyQuizId.objects.all().
                 filter(completed=False).order_by('pk'))

        if 'question' in self.initial:
            weeklyquiz = WeeklyQuizId.objects.get(pk=
                                                  self.initial['quiz_id'])
            choices.append((self.initial['quiz_id'], weeklyquiz.name))
        else:
            if query.exists():
                for item in range(len(query)):
                    choices.append((query[item].pk, query[item].name))

        self.fields['quiz_id'].choices = choices


class WeeklyQuizIdAdminForm(forms.ModelForm):
    """
    This form checks if there are 3 questions in quiz before it can be activated
    """
    class Meta:
        model = WeeklyQuizId

    def clean(self, *args, **kwargs):
        cleaned_data = super(WeeklyQuizIdAdminForm, self).clean(*args, **kwargs)

        if cleaned_data['active']:
            query = (WeeklyQuizQuestion.objects.
                     all().filter(quiz_id_id=self.instance.id))
            if len(query) != 3:
                raise forms.ValidationError("This quiz has less than 3 "
                                            "questions, finish questions to "
                                            "activate")
        return cleaned_data


class WeeklyQuizAnswerFormset(BaseInlineFormSet):
    """
    This class:
        - Checks if answers have been included
        - Checks if responses have been included
        - Checks the max_length for the questions and answers
        - Checks the max_length for the responses
        - If 3 questions have been added toggles to complete
    """

    def clean(self):
        """
        Overiding the clean function so that the max length can be checked
        also checks if the answer has been submitted and Foreign key has
        been included
        """
        super(WeeklyQuizAnswerFormset, self).clean()
        char_limit_answer = len(self.instance.question)
        char_limit_response = 0
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue

            if ("answer" not in form.cleaned_data):
                raise forms.ValidationError("You need to complete the answers")

            else:
                char_limit_answer = char_limit_answer + len(form.cleaned_data['answer'])

                if char_limit_answer > 160:
                    raise forms.ValidationError("You have gone beyond the"
                                                " character limit"
                                                " please shorten questions"
                                                " and/or answers")

            if ("response" not in form.cleaned_data):
                raise forms.ValidationError("You need to complete the responses")

            else:
                char_limit_response = char_limit_response + len(form.cleaned_data['response'])
                if char_limit_response > 160:
                    raise forms.ValidationError("You have gone beyond the"
                                                " character limit"
                                                " please shorten the responses")

        try:
        # Checking if Foreign ID has been included otherwise gives
        # an DoesNotExist exception at which point it skips
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
    """
    This class sets the answers to be on the same page as the parent question
    """
    model = WeeklyQuizAnswer
    extra = 3  # Number of initial answers fields
    max_num = 3  # Number of maximum answer fields
    formset = WeeklyQuizAnswerFormset


class WeeklyQuizIdAdmin(admin.ModelAdmin):
    """
    This class sets handles extra functionality for QuizID Admin section
    """
    list_display = ["name", "active", "completed"]
    form = WeeklyQuizIdAdminForm


class WeeklyQuizQuestionAdmin(admin.ModelAdmin):
    """
    This class sets handles extra functionality for Question Admin section
    """
    inlines = [WeeklyQuizAnswerInline]
    form = WeeklyQuizQuestionAdminForm
    list_display = ["question", "quiz_id"]


admin.site.register(WeeklyQuizId, WeeklyQuizIdAdmin)
admin.site.register(WeeklyQuizQuestion, WeeklyQuizQuestionAdmin)
