#!/usr/bin/env python
# encoding=utf-8
# maintainer rgaudin

from django.contrib import admin
from models import Point, AreaType, Area


class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude')


class AreaTypeAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')


class AreaAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'kind', 'location', 'code', 'parent')
    search_fields = ['code', 'name']
    list_filter = ('kind',)

admin.site.register(Point, PointAdmin)
admin.site.register(AreaType, AreaTypeAdmin)
admin.site.register(Area, AreaAdmin)