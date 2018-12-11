from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.search.models import Query

import blog.blocks as blocks


class BlogHomePage(Page):
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    body = StreamField([
        ('header', blocks.Header()),
        ('date', blocks.Date()),
        ('text', blocks.Text()),
        ('aside', blocks.Aside()),
        ('caption', blocks.Caption()),
        ('flickity', blocks.Flickity()),
        ('gallery', blocks.Gallery()),
        ('picture', blocks.Picture()),
        ('location', blocks.Location()),
        ('place', blocks.Place()),
    ], null=True, blank=True)

    content_panels = Page.content_panels +\
                     [
                         StreamFieldPanel('body'),
                     ]

    promote_panels = [
                         ImageChooserPanel('banner_image'),
                     ] + Page.promote_panels

    parent_page_types = []

    def get_context(self, request):
        context = super().get_context(request)

        blogpages = self.get_descendants().live().type(BlogPostPage).order_by('-blogpostpage__post_date', 'title')

        paginator = Paginator(blogpages, 10)

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
        paginator = Paginator(search_results, 10)
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
    hide_date = models.BooleanField(default=False)
    hide_intro = models.BooleanField(default=False)
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
        FieldPanel('hide_date'),
        FieldPanel('hide_intro'),
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

        paginator = Paginator(blogpages, 10)

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
        ('header', blocks.Header()),
        ('date', blocks.Date()),
        ('text', blocks.Text()),
        ('aside', blocks.Aside()),
        ('caption', blocks.Caption()),
        ('flickity', blocks.Flickity()),
        ('gallery', blocks.Gallery()),
        ('picture', blocks.Picture()),
        ('location', blocks.Location()),
        ('place', blocks.Place()),
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

        hide_date = self.get_parent().specific.hide_date
        hide_intro = self.get_parent().specific.hide_intro

        context['hide_date'] = hide_date
        context['hide_intro'] = hide_intro

        return context
