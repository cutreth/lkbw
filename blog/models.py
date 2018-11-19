from django import forms
from django.utils.functional import cached_property
from django.db import models
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils.html import format_html
from django.utils.safestring import mark_safe

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from wagtail.search.models import Query

from wagtailgeowidget.blocks import GeoBlock

from blog.do import geosgeometry_str_to_struct

import json
import six

try:
    from django.contrib.gis.geos.point import Point
except:
    Point = None

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


class Gallery(blocks.StructBlock):
    pictures = blocks.ListBlock(ImageChooserBlock())

    class Meta:
        template = 'blog/blocks/gallery.html'
        icon = 'image'


class Picture(blocks.StructBlock):
    picture = ImageChooserBlock()

    class Meta:
        template = 'blog/blocks/picture.html'
        icon = 'image'


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
    location = GeoBlock(address_field='address')
    zoom = blocks.IntegerBlock(required=False, min_value=0, max_value=19, default=8)
    satellite = blocks.BooleanBlock(required=False)

    class Meta:
        template = 'blog/blocks/location.html'
        icon = 'site'
        value_class = LocationStructValue


class PlaceField(forms.HiddenInput):
    address_field = None
    id_prefix = 'id_'
    srid = None

    def __init__(self, *args, **kwargs):
        self.address_field = kwargs.pop('address_field', self.address_field)
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

        data = {
            'sourceSelector': source_selector,
            'defaultLocation': settings.GEO_WIDGET_DEFAULT_LOCATION,
            'addressSelector': address_selector,
            'latLngDisplaySelector': '#_id_{}_latlng'.format(name),
            'zoom': self.zoom,
            'srid': self.srid,
        }

        if value and isinstance(value, six.string_types):
            result = geosgeometry_str_to_struct(value)
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
    def __init__(self, address_field=None, required=True, help_text=None,
                 **kwargs):
        self.field_options = {}
        self.address_field = address_field
        super(PlaceBlock, self).__init__(**kwargs)

    @cached_property
    def field(self):
        field_kwargs = {'widget': PlaceField(
            srid=4326,
            id_prefix='',
            address_field=self.address_field,
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

        value = geosgeometry_str_to_struct(value)
        value = {
            'lat': value['y'],
            'lng': value['x'],
            'srid': value['srid'],
        }

        return super(PlaceBlock, self).to_python(value)


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
    place = blocks.CharBlock(required=False)
    location = PlaceBlock(place_field='place')
    zoom = blocks.IntegerBlock(required=False, min_value=0, max_value=19, default=8)
    satellite = blocks.BooleanBlock(required=False)

    # Place IDs should be prefixed with place_id

    class Meta:
        template = 'blog/blocks/place.html'
        icon = 'site'
        value_class = PlaceStructValue


def get_menu(page):
    homepage = page.get_site().root_page
    menupages = BlogSectionPage.objects.all().child_of(homepage).live().in_menu().order_by('order')
    return menupages


class BlogHomePage(Page):
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    promote_panels = [
                         ImageChooserPanel('banner_image'),
                     ] + Page.promote_panels

    parent_page_types = []

    def get_context(self, request):
        context = super().get_context(request)

        blogsection = self.get_first_child()
        blogpages = blogsection.get_children().live().type(BlogPostPage).order_by('-blogpostpage__post_date', 'title')

        paginator = Paginator(blogpages, 2)

        page = request.GET.get('page')
        try:
            blogpages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            blogpages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            blogpages = paginator.page(paginator.num_pages)

        context['blogpages'] = blogpages

        homepage = self.get_site().root_page
        menupages = BlogSectionPage.objects.all().child_of(homepage).live().in_menu().order_by('order')

        context['homepage'] = homepage
        context['menupages'] = menupages

        return context


class BlogSearchPage(Page):
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    promote_panels = [
                         ImageChooserPanel('banner_image'),
                     ] + Page.promote_panels

    parent_page_types = [BlogHomePage]

    def get_context(self, request):
        context = super().get_context(request)

        search_query = request.GET.get('query', None)
        search_page = request.GET.get('page', 1)

        # Search
        if search_query:
            search_results = Page.objects.live().type(BlogPostPage).search(search_query)
            query = Query.get(search_query)

            # Record hit
            query.add_hit()
        else:
            search_results = Page.objects.none()

        # Pagination
        paginator = Paginator(search_results, 2)
        try:
            search_results = paginator.page(search_page)
        except PageNotAnInteger:
            search_results = paginator.page(1)
        except EmptyPage:
            search_results = paginator.page(paginator.num_pages)

        context['search_page'] = search_page
        context['search_results'] = search_results
        context['search_query'] = search_query

        homepage = self.get_site().root_page
        menupages = BlogSectionPage.objects.all().child_of(homepage).live().in_menu().order_by('order')

        context['homepage'] = homepage
        context['menupages'] = menupages

        return context


class BlogSectionPage(Page):
    order = models.PositiveIntegerField()
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
    ]

    content_panels = Page.content_panels + [
        FieldPanel('order'),
    ]

    promote_panels = [
                         ImageChooserPanel('banner_image'),
                     ] + Page.promote_panels

    settings_panels = [

                      ] + Page.settings_panels

    parent_page_types = [BlogHomePage]

    def get_context(self, request):
        context = super().get_context(request)

        blogpages = self.get_children().live().type(BlogPostPage).order_by('-blogpostpage__post_date', 'title')

        paginator = Paginator(blogpages, 2)

        sect_page = request.GET.get('page')

        try:
            blogpages = paginator.page(sect_page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            blogpages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            blogpages = paginator.page(paginator.num_pages)

        context['sect_page'] = sect_page
        context['blogpages'] = blogpages

        homepage = self.get_site().root_page
        menupages = BlogSectionPage.objects.all().child_of(homepage).live().in_menu().order_by('order')

        context['homepage'] = homepage
        context['menupages'] = menupages

        return context


class BlogPostPage(Page):
    post_date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )


    body = StreamField([
        ('header', Header()),
        ('date', Date()),
        ('text', Text()),
        ('aside', Aside()),
        ('caption', Caption()),
        ('gallery', Gallery()),
        ('picture', Picture()),
        ('location', Location()),
        ('place', Place()),
    ], null=True, blank=True)

    parent_page_types = [BlogSectionPage]

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('post_date'),
        StreamFieldPanel('body'),
    ]

    promote_panels = [
                         ImageChooserPanel('banner_image'),
                     ] + Page.promote_panels

    settings_panels = Page.settings_panels + [

    ]

    def get_context(self, request):
        context = super().get_context(request)

        sect_page = request.GET.get('sect_page')
        context['sect_page'] = sect_page

        search_page = request.GET.get('search_page')
        search_query = request.GET.get('search_query')

        context['search_page'] = search_page
        context['search_query'] = search_query

        homepage = self.get_site().root_page
        menupages = BlogSectionPage.objects.all().child_of(homepage).live().in_menu().order_by('order')

        context['homepage'] = homepage
        context['menupages'] = menupages

        return context
