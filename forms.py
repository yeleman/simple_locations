#a tree form widget that
#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from django.forms import fields
from django.utils.safestring import mark_safe
from django.template.loader import get_template
from django.template.context import Context
from django.forms.widgets import Widget, Select
from simple_locations.models import Area
from django.conf import settings
from mptt.forms import TreeNodeChoiceField

class LocationForm(forms.Form):
    name = forms.CharField(max_length=100)
    code = forms.CharField(max_length=50) # FIXME: code shouldn't be required, but should rather be auto-generated if not provided
    pk = forms.CharField(widget=forms.HiddenInput(), required=False)
    target = TreeNodeChoiceField(queryset=Area.tree.all(),
                                 level_indicator=u'+--', required=False)
    lat = forms.DecimalField(required=False) # FIXME: if lat is provided, lon is required
    lon = forms.DecimalField(required=False) # FIXME: if lon is provided, lat is required
    move_choice = forms.BooleanField(required=False)
    position = forms.ChoiceField(choices=(('last-child', 'inside'), ('left', 'before'), ('right', 'after')),
                                 required=False)
    def clean_lat_lon(self):
        """ make sure that both lat and lon are provided. if lat is given then lon is also required and vice versa.  """
        lat=self.cleaned_data['lat']
        lon=self.cleaned_data['lon']
        if lat is None or lon is None:
            raise forms.ValidationError("Please provide both lat and lon")
           
        return (lat,lon)


