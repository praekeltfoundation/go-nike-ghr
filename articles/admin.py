from django.contrib import admin
from articles.models import Article, MonitorAndLearningQuizId, MonitorAndLearningQuizQuestion, MonitorAndLearningQuizAnswer


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

admin.site.register(Article, ArticleAdmin)
admin.site.register(MonitorAndLearningQuizId, MonitorAndLearningQuizIdAdmin)
admin.site.register(MonitorAndLearningQuizQuestion, MonitorAndLearningQuizQuestionAdmin)
