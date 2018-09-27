from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from wagtail.snippets.models import register_snippet

class BlogSectionPage(Page):

	post_date = models.DateField("Post date", null=True, blank=True)
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
		ImageChooserPanel('banner_image'),
	]
	
	promote_panels = Page.promote_panels + [
	]
	
	settings_panels = Page.settings_panels + [
		FieldPanel('post_date'),
	]

	def get_context(self, request):
		context = super().get_context(request)
		blogpages = self.get_children().live().order_by('-first_published_at')
		context['blogpages'] = blogpages
		return context
		
class BlogPostPage(Page):

	post_date = models.DateField("Post date", null=True, blank=True)
	intro = models.CharField(max_length=250)
	banner_image = models.ForeignKey(
		'wagtailimages.Image',
		null=True, blank=True,
		on_delete=models.SET_NULL,
		related_name='+'
	)
	
	body = StreamField([
		('heading', blocks.CharBlock(classname="full title")),
		('paragraph', blocks.RichTextBlock()),
		('image', ImageChooserBlock()),
		('date', blocks.DateBlock()),
		('html', blocks.RawHTMLBlock()),
		('quote', blocks.BlockQuoteBlock()),
	])

	search_fields = Page.search_fields + [
		index.SearchField('intro'),
		index.SearchField('body'),
	]
	
	content_panels = Page.content_panels + [
		FieldPanel('intro'),
		ImageChooserPanel('banner_image'),
		StreamFieldPanel('body'),
	]
	
	promote_panels = Page.promote_panels + [
	]

	settings_panels = Page.settings_panels + [
		FieldPanel('post_date'),
	]	
