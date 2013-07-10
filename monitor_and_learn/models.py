from django.db import models


class MonitorAndLearningQuizId(models.Model):
    # The quiz class which forms the Foreign Key for the
    # questions, contains an active field
    # where the quize can be set to active and a completed
    # field where if 4 questions are it changes to complete = True
    name = models.CharField(max_length=50, blank=False,
                            verbose_name="Name of Quiz")
    active = models.BooleanField()
    completed = models.BooleanField()

    def __unicode__(self):
        # Provides a User friendly name
        return self.name

    class Meta:
        verbose_name_plural = "Monitor and Learning Quiz ID's"


class MonitorAndLearningQuizQuestion(models.Model):
    # This class stores the questions to be asked
    quiz_id = models.ForeignKey('MonitorAndLearningQuizId',
                                related_name='quiz_ids',
                                verbose_name='Quiz Name')
    question = models.CharField(max_length=160, blank=False)

    def __unicode__(self):
        return self.question

    class Meta:
        verbose_name = "Monitor and Learning Quiz Question"


class MonitorAndLearningQuizAnswer(models.Model):
    # This class stores the answers.
    question_id = models.ForeignKey('MonitorAndLearningQuizQuestion',
                                    related_name="question_ids")
    answer = models.CharField(max_length=160)

    def __unicode__(self):
        return self.answer
