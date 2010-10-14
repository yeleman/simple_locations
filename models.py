#!/usr/bin/env python
# encoding=utf-8
# vim: ai ts=4 sts=4 et sw=4

import uuid

from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy as __
from code_generator.fields import CodeField
import mptt
from mptt.models import MPTTModel


class Point(models.Model):
    class Meta:
        verbose_name = __("Point")
        verbose_name_plural = __("Points")

    latitude = models.DecimalField(max_digits=13, decimal_places=10)
    longitude = models.DecimalField(max_digits=13, decimal_places=10)


    def __unicode__(self):
        return _(u"%(lat)s, %(lon)s") % {'lat': self.latitude, \
                                         'lon': self.longitude}


class AreaType(models.Model):
    class Meta:
        verbose_name = __("Area Type")
        verbose_name_plural = __("Area Types")

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return _(self.name)


class Area(MPTTModel):
    class Meta:
        unique_together = ('code', 'kind')
        verbose_name = __("Area")
        verbose_name_plural = __("Areas")

    class MPTTMeta:
        parent_attr = 'parent'
        order_insertion_by = ['name']

    name = models.CharField(max_length=100)
    code = CodeField(max_length=50, prefix='A', default='0', \
                     min_length=3)
    kind = models.ForeignKey('AreaType', blank=True, null=True)
    location = models.ForeignKey(Point, blank=True, null=True)
    parent = models.ForeignKey('Area', blank=True, null=True, \
                               related_name='children')

    def delete(self):
        super(Area, self).delete()


