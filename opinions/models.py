from django.db import models


class Opinion(models.Model):
    # This class is for the Article model.
    opinion_1 = models.CharField(max_length=125)
    opinion_2 = models.CharField(max_length=125)
    opinion_3 = models.CharField(max_length=125)
    updated_at = models.DateTimeField(auto_now_add=True,
                                      blank=False,
                                      editable=False)

    def __unicode__(self):
        return self.opinion_1

    class Meta:
        verbose_name_plural = "User Opinions"


class OpinionPollId(models.Model):
    name = models.CharField(max_length=50, blank=False,
                            verbose_name="Name of Opinion")
    active = models.BooleanField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Opinion Poll Id"


class OpinionPollOpinion(models.Model):
    opinionpollid = models.ForeignKey('OpinionPollId',
                                      related_name='opinionpollid',
                                      verbose_name='Opinion Poll Opinion')
    opinion = models.CharField(max_length=160, blank=False,
                               verbose_name="Opinion")

    def __unicode__(self):
        return self.opinion

    class Meta:
        verbose_name_plural = "User Opinion Poll"


class OpinionPollChoices(models.Model):
    opinionpollopinion = models.ForeignKey('OpinionPollOpinion',
                                           related_name='opinionpollopinion',
                                           verbose_name='Opinion Poll Choices')
    choices = models.CharField(max_length=160)

    def __unicode__(self):
        return self.choices

    class Meta:
        verbose_name_plural = "Opinion Poll Choices"
