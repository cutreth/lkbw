import json
import six

from django import forms
from django.conf import settings
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.utils.safestring import mark_safe

try:
    from django.contrib.gis.geos.point import Point
except:
    Point = None

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

import blog.do as do


class Header(blocks.StructBlock):
    header = blocks.CharBlock()

    class Meta:
        template = 'blog/blocks/header.html'
        icon = 'bold'


class Text(blocks.StructBlock):
    text = blocks.RichTextBlock()

    class Meta:
        template = 'blog/blocks/text.html'
        icon = 'doc-full'


class Aside(blocks.StructBlock):
    aside = blocks.BlockQuoteBlock()

    class Meta:
        template = 'blog/blocks/aside.html'
        icon = 'openquote'


class Date(blocks.StructBlock):
    date = blocks.DateBlock()

    class Meta:
        template = 'blog/blocks/date.html'
        icon = 'date'


class Caption(blocks.StructBlock):
    caption = blocks.CharBlock()

    class Meta:
        template = 'blog/blocks/caption.html'
        icon = 'form'


class Gallery(blocks.StructBlock):
    pictures = blocks.ListBlock(blocks.StructBlock(
        [
            ('image', ImageChooserBlock()),
            ('caption', blocks.CharBlock(required=False)),
            ('date', blocks.DateBlock(Required=False)),
        ]
    ))

    class Meta:
        template = 'blog/blocks/gallery.html'
        icon = 'image'


class Picture(blocks.StructBlock):
    picture = blocks.StructBlock(
        [
            ('image', ImageChooserBlock()),
            ('caption', blocks.CharBlock(required=False)),
            ('date', blocks.DateBlock(Required=False)),
        ]
    )

    class Meta:
        template = 'blog/blocks/picture.html'
        icon = 'image'


class PlaceField(forms.HiddenInput):
    address_field = None
    place_field = None
    id_prefix = 'id_'
    srid = None

    def __init__(self, *args, **kwargs):
        self.address_field = kwargs.pop('address_field', self.address_field)
        self.place_field = kwargs.pop('place_field', self.place_field)
        self.srid = kwargs.pop('srid', self.srid)
        self.id_prefix = kwargs.pop('id_prefix', self.id_prefix)
        self.zoom = kwargs.pop('zoom', settings.GEO_WIDGET_ZOOM)

        super(PlaceField, self).__init__(*args, **kwargs)

    class Media:
        css = {
            'all': ('widgets/place.css',)
        }

        js = (
            'widgets/place.js',
            'https://maps.google.com/maps/api/js?key={}&libraries=places&language={}'
            .format(
                settings.GOOGLE_MAPS_V3_APIKEY,
                'en',
            ),
        )

    def render(self, name, value, attrs=None):
        out = super(PlaceField, self).render(name, value, attrs)

        location = format_html(
            '<div class="input">'
            '<input id="_id_{}_latlng" class="geo-field-location" maxlength="250" type="text">'  # NOQA
            '</div>',
            name
        )

        if '-' in name:
            namespace = name.split('-')[:-1]
            namespace = '-'.join(namespace)
            namespace = '{}-'.format(namespace)
        else:
            namespace = ''

        source_selector = '#{}{}'.format(self.id_prefix, name)
        address_selector = '#{}{}{}'.format(self.id_prefix,
                                            namespace,
                                            self.address_field)
        place_selector = '#{}{}{}'.format(self.id_prefix,
                                            namespace,
                                            self.place_field)

        data = {
            'sourceSelector': source_selector,
            'defaultLocation': settings.GEO_WIDGET_DEFAULT_LOCATION,
            'addressSelector': address_selector,
            'placeSelector': place_selector,
            'latLngDisplaySelector': '#_id_{}_latlng'.format(name),
            'zoom': self.zoom,
            'srid': self.srid,
        }

        if value and isinstance(value, six.string_types):
            result = do.geosgeometry_str_to_struct(value)
            if result:
                data['defaultLocation'] = {
                    'lat': result['y'],
                    'lng': result['x'],
                }

        if value and Point and isinstance(value, Point):
            data['defaultLocation'] = {
                'lat': value.y,
                'lng': value.x,
            }

        json_data = json.dumps(data)
        data_id = 'geo_field_{}_data'.format(name)

        return mark_safe(
            '<script>window["{}"] = {};</script>'.format(data_id, json_data) +
            out +
            location +
            '<div class="geo-field" data-data-id="{}"></div>'.format(data_id) +
            """
            <script>
            (function(){
                if (document.readyState === 'complete') {
                    return initializeGeoFields();
                }

                $(window).on('load', function() {
                    initializeGeoFields();
                });
            })();
            </script>
            """
        )


class PlaceBlock(blocks.FieldBlock):
    def __init__(self, address_field=None, place_field=None, required=True, help_text=None,
                 **kwargs):
        self.field_options = {}
        self.address_field = address_field
        self.place_field = place_field
        super(PlaceBlock, self).__init__(**kwargs)

    @cached_property
    def field(self):
        field_kwargs = {'widget': PlaceField(
            srid=4326,
            id_prefix='',
            address_field=self.address_field,
            place_field=self.place_field,
        )}
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)

    def clean(self, value):
        if not value:
            value = "SRID={};POINT({} {})".format(
                4326,
                settings.GEO_WIDGET_DEFAULT_LOCATION['lng'],
                settings.GEO_WIDGET_DEFAULT_LOCATION['lat']
            )
        return super(PlaceBlock, self).clean(value)

    def render_form(self, value, prefix='', errors=None):
        if value and isinstance(value, dict):
            value = "SRID={};POINT({} {})".format(value['srid'],
                                                  value['lng'],
                                                  value['lat'])
        return super(PlaceBlock, self).render_form(value, prefix, errors)

    def to_python(self, value):
        if isinstance(value, dict):
            return value

        value = do.geosgeometry_str_to_struct(value)
        value = {
            'lat': value['y'],
            'lng': value['x'],
            'srid': value['srid'],
        }

        return super(PlaceBlock, self).to_python(value)


class LocationStructValue(blocks.StructValue):

    @staticmethod
    def key():
        return settings.GOOGLE_MAPS_V3_APIKEY

    def zoom_level(self):
        zoom_level = self.get('zoom')
        if not zoom_level:
            zoom_level = settings.GEO_WIDGET_ZOOM
        return zoom_level

    def center(self):
        return self.get('location')["lat"] + ',' + self.get('location')["lng"]


class Location(blocks.StructBlock):
    address = blocks.CharBlock(required=False)
    place = blocks.CharBlock(required=False)
    location = PlaceBlock(address_field='address', place_field='place')
    zoom = blocks.IntegerBlock(required=False, min_value=0, max_value=19, default=8)
    satellite = blocks.BooleanBlock(required=False)
    date = blocks.DateBlock(required=False)

    class Meta:
        template = 'blog/blocks/location.html'
        icon = 'site'
        value_class = LocationStructValue


class PlaceStructValue(blocks.StructValue):

    @staticmethod
    def key():
        return settings.GOOGLE_MAPS_V3_APIKEY

    def zoom_level(self):
        zoom_level = self.get('zoom')
        if not zoom_level:
            zoom_level = settings.GEO_WIDGET_ZOOM
        return zoom_level

    def q(self):
        return self.place


class Place(blocks.StructBlock):
    address = blocks.CharBlock(required=False)
    place = blocks.CharBlock(required=False)
    location = PlaceBlock(address_field='address', place_field='place')
    zoom = blocks.IntegerBlock(required=False, min_value=0, max_value=19, default=8)
    satellite = blocks.BooleanBlock(required=False)
    date = blocks.DateBlock(required=False)

    class Meta:
        template = 'blog/blocks/place.html'
        icon = 'site'
        value_class = PlaceStructValue
