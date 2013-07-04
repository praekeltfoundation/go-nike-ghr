from django.db import models


class Opinion(models.Model):
    # This class is for the Article model.
    opinion_1 = models.CharField(max_length=125)
    opinion_2 = models.CharField(max_length=125)
    opinion_3 = models.CharField(max_length=125)
    opinion_4 = models.CharField(max_length=125)
    opinion_5 = models.CharField(max_length=125)
    updated_at = models.DateTimeField(auto_now_add=True,
                                      blank=False,
                                      editable=False)

    def __unicode__(self):
        return self.opinion_1

    class Meta:
        verbose_name_plural = "User Opinions"
