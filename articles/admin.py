from django.contrib import admin
from articles.models import Article, MonitorAndLearningQuizId, MonitorAndLearningQuizQuestion, MonitorAndLearningQuizAnswer
from django import forms
from django.forms.models import BaseInlineFormSet


class MonitorAndLearningQuiz(BaseInlineFormSet):
    # Validating the formset data

    def clean(self):
        super(MonitorAndLearningQuiz, self).clean()

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
    formset = MonitorAndLearningQuiz


class ArticleAdmin(admin.ModelAdmin):
    pass


class MonitorAndLearningQuizIdAdmin(admin.ModelAdmin):
    pass


class MonitorAndLearningQuizQuestionAdmin(admin.ModelAdmin):
    inlines = [MonitorAndLearningQuizAnswerInline]


admin.site.register(Article, ArticleAdmin)
admin.site.register(MonitorAndLearningQuizId, MonitorAndLearningQuizIdAdmin)
admin.site.register(MonitorAndLearningQuizQuestion, MonitorAndLearningQuizQuestionAdmin)
