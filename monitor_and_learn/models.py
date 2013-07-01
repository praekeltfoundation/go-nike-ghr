from django.db import models


class MonitorAndLearningQuizId(models.Model):
    active = models.BooleanField()
    completed = models.BooleanField()

    def __str__(self):
        return "quiz_%s" % self.pk

    class Meta:
        verbose_name_plural = "Monitor and Learning Quiz ID's"


class MonitorAndLearningQuizQuestion(models.Model):
    quiz_id = models.ForeignKey('MonitorAndLearningQuizId')
    question = models.CharField(max_length=160, blank=False)

    def __unicode__(self):
        return self.question

    class Meta:
        verbose_name = "Monitor and Learning Quiz Question"


class MonitorAndLearningQuizAnswer(models.Model):
    question_id = models.ForeignKey('MonitorAndLearningQuizQuestion')
    answer = models.CharField(max_length=160, blank=False)

    def __unicode__(self):
        return self.answer
