from django.db import models
from django.utils import timezone


class Article(models.Model):
    # This class is for the Article model.
    page_1 = models.CharField(max_length=125, blank=False)
    page_2 = models.CharField(max_length=125, blank=False)
    page_3 = models.CharField(max_length=125, blank=False)
    page_4 = models.CharField(max_length=125, blank=False)
    publish = models.BooleanField()
    publish_at = models.DateTimeField(default=timezone.now, blank=False)
    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=False,
                                      editable=False)

    def __unicode__(self):
        return self.page_1
