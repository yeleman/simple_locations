#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from simple_locations.models import Area,Point
from django.conf import settings
from django.utils import simplejson
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from forms import LocationForm
from django.http import HttpResponseRedirect
from mptt.exceptions import InvalidMove
from django.views.decorators.cache import cache_control
from django.template.loader import get_template
from django.template.context import Context

import decimal

#firefox likes to aaggressively cache forms set cache control to false to override this
@cache_control(no_cache=True)
def simple_locations(request):
    MEDIA_URL = settings.MEDIA_URL
    form = LocationForm()
    nodes=Area.tree.all()
    # FIXME: MEDIA_URL may not need to be passed, check?
    return render_to_response(
          'simple_locations/index.html', 
          {'form' : form,
           'nodes':nodes, 
           'MEDIA_URL': MEDIA_URL},
          context_instance=RequestContext(request))

def add_location(req, parent_id=None):
    nodes = Area.tree.all()
        
    if req.method == 'POST':
        form = LocationForm(req.POST)
        if form.is_valid():
            #FIXME: do the actual add
            pass
    else:
        if (parent_id):
            default_data = {}            
            parent = get_object_or_404(Area, pk=parent_id)
            default_data['move_choice'] = True
            default_data['target'] = parent
            default_data['position'] = 'last-child'
            form = LocationForm(default_data)
        else:
            form = LocationForm()

    return render_to_response(
        'simple_locations/location_edit.html'
        ,{'form': form, 'nodes': nodes},
        context_instance=RequestContext(req))    
    pass

def edit_location(req, area_id):
    location = get_object_or_404(Area, pk=area_id)
    if req.method == 'POST':
        form = LocationForm(req.POST)
        if form.is_valid():
            # FIXME: update the existing location
            return render_to_response("simple_locations/location_edit.html", {"form":LocationForm(), 'nodes':Area.tree.all()}, context_instance=RequestContext(req))
        else:
            return render_to_response("simple_locations/location_edit.html", 
                                      { 'form': form, 'item': location },
                                      context_instance=RequestContext(req))
    else:
        default_data = {}
        default_data['pk'] = location.pk
        default_data['name'] = location.name
        default_data['move_choice'] = False
        if location.parent:
            default_data['target'] = location.parent
            default_data['position'] = 'last-child'
        if location.location:
            default_data['lat'] = location.location.latitude
            default_data['lon'] = location.location.longitude
        form = LocationForm(default_data)
        return render_to_response("simple_locations/location_edit.html", {'form':form, 'nodes':Area.tree.all(),'item':location}, context_instance=RequestContext(req))

# FIXME: use what is necessary of this, delete the rest
#    
#    if area_id is None:
#        if request.method == 'POST':
#            form = LocationForm(request.POST)
#            if form.is_valid():
#                area = Area.objects.get(pk=int(form.cleaned_data['pk']))
#                if form.cleaned_data['move_choice']:
#                    target = form.cleaned_data['target']
#                    position = str(form.cleaned_data['position'])
#                    try:
#                        Area.tree.move_node(area, target, position)
#                    except InvalidMove:
#                        pass
#
#                (latitude, longitude) = form.cleaned_data['point']
#                latitude=decimal.Decimal(str(latitude))
#                longitude= decimal.Decimal(str(longitude))
#                name = form.cleaned_data['name']
#                code = form.cleaned_data['code']
#                area.code=code
#                if area.location:
#                    area.location.latitude=latitude
#                    area.location.longitude=longitude
#                    area.location.save()
#                    area.save()
#                else:
#                    location=Point(latitude=latitude,longitude=longitude)
#                    location.save()
#                    area.location=location
#                    area.location.save()
#                    area.save()
#
#
#                try:
#                    area.name=name
#                    area.save()
#                except InvalidMove:
#                    pass
#                return HttpResponse(simplejson.dumps("success"))
#
#                #return HttpResponseRedirect("/")
#                return HttpResponse(r_temp)
#            else:
#                MEDIA_URL = settings.MEDIA_URL
#                form = LocationForm(request.POST)
#                nodes=Area.tree.all()
#
#                return render_to_response('simple_locations/location_edit.html'
#                                          , {'form': form, 'nodes': nodes, 'MEDIA_URL'
#                        : MEDIA_URL},
#                                          context_instance=RequestContext(request))
#    else:
#        if request.GET.get('new',None):
#            parent=Area.objects.get(pk=area_id)
#            import random
#
#            #create new area
#            name='new_'+str(random.randint(1,100))+'_child'
#            code='n_'+str(random.randint(1,100))+"_code"
#            area=Area.objects.create(name=name,parent=parent,code=code)
#
#            location=Point(latitude=parent.location.longitude,longitude=parent.location.latitude)
#            location.save()
#            area.location=location
#            area.location.save()
#
#        else:
#
#            area = Area.objects.get(pk=area_id)
#        try:
#            lat = float(area.location.latitude)
#            lon = float(area.location.longitude)
#        except:
#            lat = 0
#            lon = 0
#        area_as_dict = {
#            'name': area.name,
#            'lat': lat,
#            'lon': lon,
#            'code': area.code,
#            'pk': area.pk,
#
#
#        }
#
#        return HttpResponse(mark_safe(simplejson.dumps(area_as_dict)))

def delete_location(request, area_id):
    node = get_object_or_404(Area, pk=area_id)
    if request.method == 'POST':
        node.delete()

    return HttpResponseRedirect('/simple_locations/render_tree')

@cache_control(no_cache=True)
def render_location(request):
    nodes = Area.objects.all()
    return render_to_response('simple_locations/treepanel.html',{'nodes':nodes})