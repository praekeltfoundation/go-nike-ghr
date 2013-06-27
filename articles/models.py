from django.db import models
from django.utils import timezone


class Article(models.Model):
    article = models.CharField(max_length=480, blank=False)
    publish = models.BooleanField()
    publish_at = models.DateTimeField(blank=False, default=timezone.now())
    created_at = models.DateTimeField(auto_now_add=True, blank=False, editable=False)

    def __unicode__(self):
        return self.article
