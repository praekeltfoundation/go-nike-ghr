from django.db import models
from django.utils import timezone


class Article(models.Model):
    # This class is for the Article model.
    opinion_1 = models.CharField(max_length=125)
    opinion_2 = models.CharField(max_length=125)
    opinion_3 = models.CharField(max_length=125)
    opinion_4 = models.CharField(max_length=125)
    opinion_5 = models.CharField(max_length=125)
    updated_at = models.DateTimeField(default=timezone.now,
                                      blank=False,
                                      editable=False)

    def __unicode__(self):
        return self.opinion_1
