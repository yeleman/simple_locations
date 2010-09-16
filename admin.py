#!/usr/bin/env python
# encoding=utf-8
# maintainer rgaudin

from django.contrib import admin
from models import Point, AreaType, Area, CodedArea, FreeArea


class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude')


class AreaTypeAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')


class CodedAreaAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'kind', 'parent', 'location')
    search_fields = ['code', 'name']
    list_filter = ('parent', 'kind')


class AreaAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'parent', 'location')
    search_fields = ['name']
    list_filter = ('parent',)

admin.site.register(Point, PointAdmin)
admin.site.register(AreaType, AreaTypeAdmin)
admin.site.register(CodedArea, CodedAreaAdmin)
admin.site.register(FreeArea, CodedAreaAdmin)
admin.site.register(Area, AreaAdmin)
