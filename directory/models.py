from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=60, blank=False,
                            verbose_name="Category Name")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Category"


class SubCategory(models.Model):
    # This class stores the questions to be asked
    category = models.ForeignKey('WeeklyQuizId',
                                 related_name='category',
                                 verbose_name='Category Id')

    name = models.CharField(max_length=125)
    content_1 = models.CharField(max_length=125)
    content_1 = models.CharField(max_length=125)
    content_1 = models.CharField(max_length=125)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Sub Category"
