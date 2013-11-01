from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name=u'Name of Province')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "1. Province"


class District(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name=u'Name of District')
    district_province = models.ForeignKey(Province,
                                          related_name='district_province',
                                          verbose_name=u'Province')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "2. District"



class Sector(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Name of Zone')
    sector_district = models.ForeignKey(District,
                                        related_name='sector_district',
                                        verbose_name=u'District')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "3. Sector"
