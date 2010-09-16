#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Point(models.Model):

    latitude = models.DecimalField(max_digits=13, decimal_places=10)
    longitude = models.DecimalField(max_digits=13, decimal_places=10)

    def __unicode__(self):
        return _(u"%(lat)s, %(lon)s") % {'lat': self.latitude, \
                                         'lon': self.longitude}


class AreaType(models.Model):

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.name


class Area(models.Model):

    name = models.CharField(max_length=100)
    location = models.ForeignKey(Point, blank=True, null=True)
    parent = models.ForeignKey('Area', blank=True, null=True)

    def __unicode__(self):
        return self.name


class CodedArea(Area):

    class Meta:
        unique_together = ('code', 'kind')

    kind = models.ForeignKey('AreaType', blank=True, null=True)
    code = models.CharField(max_length=30)


class FreeArea(Area):

    code = models.CharField(max_length=30, null=True, blank=True)
    kind = models.ForeignKey('AreaType', blank=True, null=True)
