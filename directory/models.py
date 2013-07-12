from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=60, blank=False,
                            verbose_name="Category Name")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Category"


class SubCategory(models.Model):
    category = models.ForeignKey('Category',
                                 related_name='category',
                                 verbose_name='Category Id')

    name = models.CharField(max_length=125, blank=False)
    content_1 = models.CharField(max_length=125, blank=True)
    content_2 = models.CharField(max_length=125, blank=True)
    content_3 = models.CharField(max_length=125, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Sub Category"
