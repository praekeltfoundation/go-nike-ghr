from django.db import models
from django.utils import timezone


class Article(models.Model):
    article = models.CharField(max_length=480, blank=False)
    publish = models.BooleanField()
    publish_at = models.DateTimeField(default=timezone.now, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, editable=False)

    def __unicode__(self):
        return self.article


class MonitorAndLearningQuizId(models.Model):
    active = models.BooleanField()


class MonitorAndLearningQuizQuestion(models.Model):
    quiz_id = models.ForeignKey('MonitorAndLearningQuizId')
    question = models.CharField(max_length=160, blank=False)

    def __unicode__(self):
        return self.question


class MonitorAndLearningQuizAnswer(models.Model):
    question_id = models.ForeignKey('MonitorAndLearningQuizQuestion')
    answer = models.CharField(max_length=160, blank=False)

    def __unicode__(self):
        return self.answer
