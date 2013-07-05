from django.contrib import admin
from models import (MonitorAndLearningQuizId,
                    MonitorAndLearningQuizQuestion,
                    MonitorAndLearningQuizAnswer)
from django import forms
from django.forms.models import BaseInlineFormSet


class QuestionAdminForm(forms.ModelForm):
    """
    This form checks to see if there are any uncompleted quizzes
    (< 4 questions), if so sets current ID to the uncompleted quiz_id.
    If editing sets the current quiz id  to be edited
    """
    def __init__(self, *args, **kwargs):
        super(QuestionAdminForm, self).__init__(*args, **kwargs)
        choices = [self.fields["quiz_id"].choices.__iter__().next()]
        choices.pop()  # Removing empty choice so it defaults to empty
        query = (MonitorAndLearningQuizId.objects.all().
                 filter(completed=False).order_by('pk'))

        if 'question' in self.initial:
            get_quiz = MonitorAndLearningQuizId.objects.get(pk=
                                                            self.initial['quiz_id'])
            choices.append((self.initial['quiz_id'], get_quiz.name))
        else:
            if query.exists():
                for item in range(len(query)):
                    choices.append((query[item].pk, query[item].name))

        self.fields['quiz_id'].choices = choices


class QuizIdAdminForm(forms.ModelForm):
    """
    This form checks if there are 4 questions in quiz before it can be activated
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(QuizIdAdminForm, self).__init__(*args, **kwargs)

    class Meta:
        model = MonitorAndLearningQuizId

    def clean(self, *args, **kwargs):
        #  Checking the active field vs number of questions completed
        #  to see if quiz should be activated
        cleaned_data = super(QuizIdAdminForm, self).clean(*args, **kwargs)

        if cleaned_data['active']:
            query = (MonitorAndLearningQuizQuestion.objects.
                     all().filter(quiz_id_id=self.instance.id))
            if len(query) != 4:
                raise forms.ValidationError("This quiz has less than 4 "
                                            "questions, finish questions to "
                                            "activate")
        return cleaned_data


class MonitorAndLearningQuizAnswerFormset(BaseInlineFormSet):
    """
    This class:
        - Checks if answers have been included fails if < 2
        - Checks if responses have been included
        - Checks the max_length for the questions and answers
        - If 4 questions have been added toggles to complete
    """

    def clean(self):
        """
        Overiding the clean function so that the max length can be checked
        also checks if the answer has been submitted and Foreign key has
        been included
        """
        super(MonitorAndLearningQuizAnswerFormset, self).clean()
        i = 0
        char_limit = len(self.instance.question)
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue

            if "answer" in form.cleaned_data:
                i = i + 1

            if ("answer" not in form.cleaned_data and i < 2):
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
            query = (MonitorAndLearningQuizQuestion.objects.all().
                     filter(quiz_id=self.instance.quiz_id))
            if len(query) >= 3:
                query = (MonitorAndLearningQuizId.objects.
                         get(pk=self.instance.quiz_id.id))
                query.completed = True
                query.save()
        except:
            pass


class MonitorAndLearningQuizAnswerInline(admin.StackedInline):
    """
    This class sets the answers to be on the same page as the parent question
    """
    model = MonitorAndLearningQuizAnswer
    extra = 2
    formset = MonitorAndLearningQuizAnswerFormset


class MonitorAndLearningQuizIdAdmin(admin.ModelAdmin):
    """
    This class sets handles extra functionality for QuizID Admin section
    """
    list_display = ["name", "active", "completed"]
    form = QuizIdAdminForm


class MonitorAndLearningQuizQuestionAdmin(admin.ModelAdmin):
    """
    This class sets handles extra functionality for Question Admin section
    """
    inlines = [MonitorAndLearningQuizAnswerInline]
    form = QuestionAdminForm
    list_display = ["question", "quiz_id"]


admin.site.register(MonitorAndLearningQuizId, MonitorAndLearningQuizIdAdmin)
admin.site.register(MonitorAndLearningQuizQuestion,
                    MonitorAndLearningQuizQuestionAdmin)
