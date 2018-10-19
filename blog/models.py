from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index

from wagtailgmaps.edit_handlers import MapFieldPanel


class Header (blocks.StructBlock):

	header = blocks.CharBlock()

	class Meta:
		template = 'blog/header.html'


class Text (blocks.StructBlock):

	text = blocks.RichTextBlock()

	class Meta:
		template = 'blog/text.html'


class Pictures(blocks.StructBlock):

	pictures = blocks.ListBlock(ImageChooserBlock())

	class Meta:
		template = 'blog/pictures.html'


class Aside(blocks.StructBlock):

	aside = blocks.BlockQuoteBlock()

	class Meta:
		template = 'blog/aside.html'


class Date(blocks.StructBlock):

	date = blocks.DateBlock()

	class Meta:
		template = 'blog/date.html'


class Caption(blocks.StructBlock):

	caption = blocks.CharBlock()

	class Meta:
		template = 'blog/caption.html'


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
		('date', Date()),
		('pictures', Pictures()),
		('caption', Caption()),
		('aside', Aside()),
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
