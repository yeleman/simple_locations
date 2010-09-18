#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


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
    code = models.CharField(max_length=50, blank=True, null=False)
    kind = models.ForeignKey('AreaType', blank=True, null=True)
    location = models.ForeignKey(Point, blank=True, null=True)
    parent = models.ForeignKey('Area', blank=True, null=True)

    def __unicode__(self):
        if not self.parent:
            return self.name
        else:
            return u"%(type)s de %(area)s" % {'type': self.kind.name, \
                                             'area': self.name}

    def save(self, *args, **kwargs):
        ''' generates a code if none provided '''
        if not self.code:
            # generate a uuid
            self.code = uuid.uuid1().hex
        super(Area, self).save(*args, **kwargs)
