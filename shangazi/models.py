from django.db import models
from django.utils import timezone

class string_with_title(str):
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self


class Shangazi(models.Model):
    # This class is for the Ndabaga model.
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

    class Meta:
        verbose_name = "What would Shangazi Do?"
        verbose_name_plural = "What would Shangazi Do?"
        app_label = string_with_title("shangazi", "Shangazi's Advice")
