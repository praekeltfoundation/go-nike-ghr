from django.db import models


class WeeklyQuizId(models.Model):
    # The quiz class which forms the Foreign Key for the
    # questions, contains an active field
    # where the quize can be set to active and a completed
    # field where if 4 questions are it changes to complete = True
    name = models.CharField(max_length=50, blank=False,
                            verbose_name="Name of Quiz")
    active = models.BooleanField()
    completed = models.BooleanField(editable=False)

    def __str__(self):
        # Provides a User friendly name
        return self.name

    class Meta:
        verbose_name_plural = "Weekly Quiz Status"


class WeeklyQuizQuestion(models.Model):
    # This class stores the questions to be asked
    quiz_id = models.ForeignKey('WeeklyQuizId',
                                related_name='wq_quiz_id',
                                verbose_name='Weekly Quiz Name')
    question = models.CharField(max_length=160, blank=False)

    def __unicode__(self):
        return self.question

    class Meta:
        verbose_name = "Weekly Quiz Question"


class WeeklyQuizAnswer(models.Model):
    # This class stores the answers.
    question_id = models.ForeignKey('WeeklyQuizQuestion',
                                    related_name="wq_question_id")
    answer = models.CharField(max_length=160)
    response = models.CharField(max_length=160)

    def __unicode__(self):
        return self.answer
