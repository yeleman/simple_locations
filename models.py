#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from code_generator.fields import CodeField
import mptt


class Point(models.Model):

    class Meta:
        verbose_name = _("Point")
        verbose_name_plural = _("Points")

    latitude = models.DecimalField(max_digits=13, decimal_places=10)
    longitude = models.DecimalField(max_digits=13, decimal_places=10)

    def __unicode__(self):
        return _(u"%(lat)s, %(lon)s") % {'lat': self.latitude, \
                                         'lon': self.longitude}


class AreaType(models.Model):

    class Meta:
        verbose_name = _("Area Type")
        verbose_name_plural = _("Area Types")

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.name


class Area(models.Model):

    class Meta:
        unique_together = ('code', 'kind')
        verbose_name = _("Area")
        verbose_name_plural = _("Areas")

    name = models.CharField(max_length=100)
    code = CodeField(max_length=50, prefix='A', default='0', \
                     min_length=3)
    kind = models.ForeignKey('AreaType', blank=True, null=True)
    location = models.ForeignKey(Point, blank=True, null=True)
    parent = models.ForeignKey('Area', blank=True, null=True, \
                               related_name='children')

    def __unicode__(self):
        ''' print Area name from its Kind

        Example: name=Bamako, kind=District => District of Bamako '''

        # don't add-in kind if kind name is already part of name.
        if not self.parent \
           or self.name.startswith(self.kind.name):
            return self.name
        else:
            return u"%(type)s of %(area)s" % {'type': self.kind.name, \
                                             'area': self.name}

mptt.register(Area, parent_attr='parent', order_insertion_by=['name'])
