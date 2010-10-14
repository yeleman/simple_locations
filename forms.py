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

class locationTreeWidget(Widget):
    """
        a widget to display a location tree
    """

    class Media:
        js = [settings.MEDIA_URL + 'simple_locations/javascripts/tree.js']
        css = {'all': [settings.MEDIA_URL + 'simple_locations/css/tree.css']}


    def __init__(
    self,
    language=None,
    attrs=None,
    **kwargs
    ):
        super(locationTreeWidget, self).__init__(attrs)

    def id_for_label(self, id):
        return id

    def render(
    self,
    name,
    value,
    attrs=None,
    ):
        if value is None:
            value = []
        nodes = Area.objects.all()
        data = {}
        template = get_template('simple_locations/tree.html')
        data.update(nodes=nodes)
        return template.render(Context(data))

    def value_from_datadict(
    self,
    data,
    files,
    name,
    ):
        try:
            d = [int(val) for val in dict(data)[name]]
        except KeyError:
            d = []
        return d


class LocationPickerWidget(forms.widgets.Widget):
    def __init__(self, *args, **kw):
        super(LocationPickerWidget, self).__init__(*args, **kw)
        self.inner_widget = forms.widgets.HiddenInput()

    def render(self, name, value, *args, **kwargs):
        try:
            Lat = settings.Lat
            Lon = settings.Lon
        except:
        ##default
            Lat, Lon = 1.0546279422758869, 31.9921875
        js = '''
        <script type="text/javascript">
            //<![CDATA[
            var %(name)s_marker ;
            $(document).ready(function () {
                if (GBrowserIsCompatible()) {
                    map = new GMap2(document.getElementById("map_%(name)s"));
                    map.setCenter(new GLatLng(%(Lat)f,%(Lon)f), 4);
                    %(name)s_marker = new GMarker(new GLatLng(%(Lat)f,%(Lon)f), {draggable: true});
                    map.addOverlay(%(name)s_marker);
                    map.addControl(new GLargeMapControl());
                    $('#%(name)s_id')[0].value = %(name)s_marker.getLatLng().lat() + "," + %(name)s_marker.getLatLng().lng();
                    GEvent.addListener(%(name)s_marker, "dragend", function() {
                        var point = %(name)s_marker.getLatLng();
                        $('#%(name)s_id')[0].value = point.lat() + "," + point.lng();
                        $('#lat')[0].value=point.lat();
                        $('#lon')[0].value=point.lng();
                        
                    });
                    GEvent.addListener(map, "moveend", function() {
                        var point = map.getCenter();
                        $('#%(name)s_id')[0].value = point.lat() + "," + point.lng();
                        %(name)s_marker.setLatLng(point);
                        $('#lat')[0].value=point.lat();
                        $('#lon')[0].value=point.lng();
                        
                    });
                }});
            $(document).unload(function () {GUnload()});
            //]]>
        </script>
        ''' % dict(name=name, Lat=Lat, Lon=Lon)
        html = self.inner_widget.render("%s" % name, None, dict(id='%s_id' % name))
        ##html+="Lat:<input type='textfield' name='lat' id='lat'>Lon:<input type='textfield' name='lon' id='lon'>"
        html += "<div id=\"map_%s\" style=\"width: 812px; height: 300px\"></div>" % name
        return mark_safe(js + html)



class LocationField(forms.Field):
    widget = LocationPickerWidget

    def clean(self, value):
        a, b = value.split(',')
        lat, lng = float(a), float(b)
        return lat, lng

class LocationForm(forms.Form):

    point = LocationField(required=False)
    name = forms.CharField(max_length=100)
    code = forms.CharField(max_length=50)
    pk = forms.CharField(widget=forms.HiddenInput(), required=False)
    target = TreeNodeChoiceField(queryset=Area.tree.all(),
                                 level_indicator=u'+--', required=False)
    position = forms.ChoiceField(choices=(('last-child', 'inside'), ('left', 'before'), ('right', 'after')),
                                 required=False)
    move_choice = forms.BooleanField(required=False)
    


