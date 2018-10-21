from django.db import models
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index

from wagtailgmaps.edit_handlers import MapFieldPanel
from wagtailgeowidget.blocks import GeoBlock


class Header (blocks.StructBlock):

	header = blocks.CharBlock()

	class Meta:
		template = 'blog/blocks/header.html'
		icon = 'title'


class Text (blocks.StructBlock):

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

	@staticmethod
	def zoom():
		return settings.GEO_WIDGET_ZOOM

	def center(self):
		return self.get('latt_long')["lat"] + ',' + self.get('latt_long')["lng"]


class Location(blocks.StructBlock):

	address = blocks.CharBlock(required=False)
	latt_long = GeoBlock(address_field='address')

	class Meta:
		template = 'blog/blocks/location.html'
		icon = 'site'
		value_class = LocationStructValue


class PlaceStructValue(blocks.StructValue):

	@staticmethod
	def key():
		return settings.GOOGLE_MAPS_V3_APIKEY

	@staticmethod
	def zoom():
		return settings.GEO_WIDGET_ZOOM


class Place(blocks.StructBlock):

	q = blocks.CharBlock()

	class Meta:
		template = 'blog/blocks/place.html'
		icon = 'site'
		value_class = PlaceStructValue


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

	def get_context(self, request):
		context = super().get_context(request)
		blogsection = self.get_first_child()
		blogpages = blogsection.get_children().live().order_by('-first_published_at')
		context['blogpages'] = blogpages
		return context


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
		('gallery', Gallery()),
		('picture', Picture()),
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
