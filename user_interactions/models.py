from django.db import models


class UserInteraction(models.Model):
    # This class is for the User Interaction Model
    msisdn = models.CharField(max_length=20, blank=False)
    feature = models.CharField(max_length=30, blank=False)
    key = models.CharField(max_length=100, blank=False)
    value = models.CharField(max_length=200, blank=False)
    transport = models.CharField(max_length=5, blank=False)
    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=False,
                                      editable=False)

    def __unicode__(self):
        return self.msisdn
