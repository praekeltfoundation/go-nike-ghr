from django.db import models
from django.utils import timezone


class Opinion(models.Model):
    # This class is for the Article model.
    opinion_1 = models.CharField(max_length=125, blank=False)
    opinion_2 = models.CharField(max_length=125, blank=False)
    opinion_3 = models.CharField(max_length=125, blank=False)
    opinion_4 = models.CharField(max_length=125, blank=False)
    opinion_5 = models.CharField(max_length=125, blank=False)
    updated_at = models.DateTimeField(default=timezone.now,
                                      blank=False,
                                      editable=False)

    def __unicode__(self):
        return self.opinion_1
