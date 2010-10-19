#a tree form widget that
#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from django.forms import fields
from django.utils.safestring import mark_safe
from django.template.loader import get_template
from django.template.context import Context
from django.forms.widgets import Widget, Select
from simple_locations.models import Area,AreaType
from django.conf import settings
from mptt.forms import TreeNodeChoiceField


class LocationForm(forms.Form):
    name = forms.CharField(max_length=100)
    code = forms.CharField(max_length=50) 
    pk = forms.CharField(widget=forms.HiddenInput(), required=False)
    target = TreeNodeChoiceField(queryset=Area.tree.all(),
                                 level_indicator=u'+--', required=False)
    lat = forms.DecimalField(required=False) 
    lon = forms.DecimalField(required=False) 
    kind=forms.ChoiceField(required=False,choices=(('','-----'),)+tuple([(int(w.pk),w.name) for w in AreaType.objects.all() ]))
    move_choice = forms.BooleanField(required=False)
    position = forms.ChoiceField(choices=(('last-child', 'inside'), ('left', 'before'), ('right', 'after')),
                                 required=False)
    def clean(self):
        """ make sure that both lat and lon are provided. if lat is given then lon is also required and vice versa.  """
        lat=self.cleaned_data['lat']
        lon=self.cleaned_data['lon']
        if not lat and lon:
            raise forms.ValidationError("Please provide both lat and lon")
        elif lat and not lon:
            raise forms.ValidationError("Please provide both lat and lon")
          
        return self.cleaned_data
    
    
   
    
    
            
            
    


