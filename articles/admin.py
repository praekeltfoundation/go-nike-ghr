from django.contrib import admin
from articles.models import Article, MonitorAndLearningQuizId, MonitorAndLearningQuizQuestion, MonitorAndLearningQuizAnswer
from django import forms


class MonitorAndLearningQuizAnswerInline(admin.StackedInline):
    model = MonitorAndLearningQuizAnswer
    extra = 3
    max_num = 3


class ArticleAdmin(admin.ModelAdmin):
    pass


class MonitorAndLearningQuizIdAdmin(admin.ModelAdmin):
    pass


class MonitorAndLearningQuizQuestionAdmin(admin.ModelAdmin):
    inlines = [MonitorAndLearningQuizAnswerInline]

    def save_formset(self, request, form, formset, change):
        char_limit = len(form.instance.question)
        for form_item in formset:
            char_limit = char_limit + len(form_item.cleaned_data['answer'])
            if char_limit > 160:
                raise forms.ValidationError("You have gone beyond the character limit"
                                            " please shorten questions and/or answers")
        formset.save()
        form.instance.save()


admin.site.register(Article, ArticleAdmin)
admin.site.register(MonitorAndLearningQuizId, MonitorAndLearningQuizIdAdmin)
admin.site.register(MonitorAndLearningQuizQuestion, MonitorAndLearningQuizQuestionAdmin)
