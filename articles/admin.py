from django.contrib import admin
from articles.models import Article, MonitorQuizId, MonitorQuizQuestion, MonitorQuizAnswer

admin.site.register(Article)
admin.site.register(MonitorQuizId)
admin.site.register(MonitorQuizQuestion)
admin.site.register(MonitorQuizAnswer)
