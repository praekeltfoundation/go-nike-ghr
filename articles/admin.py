from django.contrib import admin
from articles.models import Article, MonitorAndLearningQuizId, MonitorAndLearningQuizQuestion, MonitorAndLearningQuizAnswer


class ArticleAdmin(admin.ModelAdmin):
    pass


class MonitorAndLearningQuizIdAdmin(admin.ModelAdmin):
    pass


class MonitorAndLearningQuizQuestionAdmin(admin.ModelAdmin):
    pass


class MonitorAndLearningQuizAnswerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Article, ArticleAdmin)
admin.site.register(MonitorAndLearningQuizId, MonitorAndLearningQuizIdAdmin)
admin.site.register(MonitorAndLearningQuizQuestion, MonitorAndLearningQuizQuestionAdmin)
admin.site.register(MonitorAndLearningQuizAnswer, MonitorAndLearningQuizAnswerAdmin)
