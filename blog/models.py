from django.db import models
from django.conf import settings

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index

from wagtailgmaps.edit_handlers import MapFieldPanel
from wagtailgeowidget.blocks import GeoBlock
from wagtailgeowidget.helpers import geosgeometry_str_to_struct


class Header (blocks.StructBlock):

	header = blocks.CharBlock()

	class Meta:
		template = 'blog/header.html'
		icon = 'title'


class Text (blocks.StructBlock):

	text = blocks.RichTextBlock()

	class Meta:
		template = 'blog/text.html'
		icon = 'doc-full'


class Pictures(blocks.StructBlock):

	pictures = blocks.ListBlock(ImageChooserBlock())

	class Meta:
		template = 'blog/pictures.html'
		icon = 'image'


class Aside(blocks.StructBlock):

	aside = blocks.BlockQuoteBlock()

	class Meta:
		template = 'blog/aside.html'
		icon = 'openquote'


class Date(blocks.StructBlock):

	date = blocks.DateBlock()

	class Meta:
		template = 'blog/date.html'
		icon = 'date'


class Caption(blocks.StructBlock):

	caption = blocks.CharBlock()

	class Meta:
		template = 'blog/caption.html'
		icon = 'form'


class LocationStructValue(blocks.StructValue):

	def latt(self):
		self.point = geosgeometry_str_to_struct(self.get('latt_long'))
		return self.point['y']

	def long(self):
		self.point = geosgeometry_str_to_struct(self.get('latt_long'))
		return self.point['x']

	def key(self):
		return settings.GOOGLE_MAPS_V3_APIKEY

	def zoom(self):
		return settings.GEO_WIDGET_ZOOM

	def center(self):
		coords = self.latt() + ',' + self.long()
		return coords


class Location(blocks.StructBlock):

	address = blocks.CharBlock(required=False)
	latt_long = GeoBlock(address_field='address')

	class Meta:
		template = 'blog/location.html'
		icon = 'site'
		value_class = LocationStructValue


class PlaceStructValue(blocks.StructBlock):

	def key(self):
		return settings.GOOGLE_MAPS_V3_APIKEY

	def zoom(self):
		return settings.GEO_WIDGET_ZOOM


class Place(blocks.StructBlock):

	q = blocks.CharBlock()

	class Meta:
		template = 'blog/place.html'
		icon = 'site'
		value_class = PlaceStructValue


class BlogSectionPage(Page):

	post_date = models.DateField("Post date")
	intro = models.CharField(max_length=250)
	banner_image = models.ForeignKey(
		'wagtailimages.Image',
		null=True, blank=True,
		on_delete=models.SET_NULL,
		related_name='+'
	)
	
	search_fields = Page.search_fields + [
	]
	
	content_panels = Page.content_panels + [
		FieldPanel('intro'),
		FieldPanel('post_date'),

	]
	
	promote_panels = [
		ImageChooserPanel('banner_image'),
	] + Page.promote_panels
	
	settings_panels = [

	] + Page.settings_panels

	def get_context(self, request):
		context = super().get_context(request)
		blogpages = self.get_children().live().order_by('-first_published_at')
		context['blogpages'] = blogpages
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
	
	formatted_address = models.CharField(max_length=250, blank=True, null=True)
	latlng_address = models.CharField(max_length=250, blank=True, null=True)

	body = StreamField([
		('header', Header()),
		('text', Text()),
		('aside', Aside()),
		('caption', Caption()),
		('pictures', Pictures()),
		('date', Date()),
		('location', Location()),
		('place', Place()),
	], null=True, blank=True)

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
		MapFieldPanel('formatted_address'),
	] + Page.promote_panels

	settings_panels = Page.settings_panels + [
	]	
