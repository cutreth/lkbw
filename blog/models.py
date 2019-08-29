from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.signals import post_save
from django.dispatch import receiver

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, PageChooserPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.search.models import Query

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

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
        ('location', blocks.Location()),
        ('place', blocks.Place()),
        ('tracker', blocks.Tracker()),
        ('spotify', blocks.Spotify()),
        ('embed', blocks.Embed()),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
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
            search_results = BlogPostPage.objects.live().search(search_query)
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


class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey('blog.BlogPostPage', on_delete=models.CASCADE, related_name='tagged_posts')


class BlogPostPage(Page):
    post_date = models.DateField("Post date")
    intro = models.CharField(max_length=250, null=True, blank=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    insta_flag = models.BooleanField(default=False)
    insta_instant = models.DateTimeField(null=True, blank=True)
    insta_comment = models.CharField(max_length=1500, null=True, blank=True)
    insta_tags = models.CharField(max_length=250, null=True, blank=True)
    search_key = models.CharField(max_length=250, null=True, blank=True)

    body = StreamField([
        ('header', blocks.Header()),
        ('date', blocks.Date()),
        ('text', blocks.Text()),
        ('aside', blocks.Aside()),
        ('caption', blocks.Caption()),
        ('flickity', blocks.Flickity()),
        ('location', blocks.Location()),
        ('place', blocks.Place()),
        ('tracker', blocks.Tracker()),
        ('spotify', blocks.Spotify()),
        ('embed', blocks.Embed()),
    ], null=True, blank=True)

    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)

    parent_page_types = [BlogSectionPage]

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
        index.SearchField('search_key', boost=20),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('post_date'),
        StreamFieldPanel('body'),
    ]

    promote_panels = [
                         ImageChooserPanel('banner_image'),
                         FieldPanel('insta_flag'),
                         FieldPanel('insta_comment'),
                         FieldPanel('insta_tags'),
                         FieldPanel('insta_instant'),
                         FieldPanel('tags'),
                     ] + Page.promote_panels

    settings_panels = Page.settings_panels + [
        FieldPanel('search_key'),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        blogpages = self.get_parent().get_children().live().type(BlogPostPage).order_by('-blogpostpage__post_date', 'title')

        index = 0
        for page in blogpages:
            if page.specific == self:
                break
            index += 1

        try:
            older_page = blogpages[index + 1]
        except:
            older_page = ''

        try:
            newer_page = blogpages[index - 1]
        except:
            newer_page = ''

        context['older_page'] = older_page
        context['newer_page'] = newer_page

        homepage = self.get_site().root_page
        menupages = BlogSectionPage.objects.all().child_of(homepage).live().in_menu().order_by('order')

        context['homepage'] = homepage
        context['menupages'] = menupages

        hide_date = self.get_parent().specific.hide_date
        hide_intro = self.get_parent().specific.hide_intro

        context['hide_date'] = hide_date
        context['hide_intro'] = hide_intro

        return context


@receiver(post_save, sender=BlogPostPage)
def update_search_key(sender, instance, **kwargs):
    search_key = '*' + str(instance.pk)
    if instance.search_key != search_key:
        instance.search_key = search_key
        instance.save_revision()


class BlogEmailPage(Page):

    sent_date = models.DateField("Sent date", null=True, blank=True)
    debug_mode = models.BooleanField(default=False)
    intro = models.CharField(max_length=1000)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    post_one = models.BooleanField(default=False)
    post_two = models.BooleanField(default=False)
    post_three = models.BooleanField(default=False)
    post_four = models.BooleanField(default=False)
    post_five = models.BooleanField(default=False)

    post_one_intro = models.CharField(max_length=1000, null=True, blank=True)
    post_two_intro = models.CharField(max_length=1000, null=True, blank=True)
    post_three_intro = models.CharField(max_length=1000, null=True, blank=True)
    post_four_intro = models.CharField(max_length=1000, null=True, blank=True)
    post_five_intro = models.CharField(max_length=1000, null=True, blank=True)


    post_one_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    post_two_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    post_three_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    post_four_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    post_five_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    post_one_img_tall = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    post_one_img_wide_a = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    post_one_img_wide_b = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    post_two_img_wide_a = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    post_two_img_wide_b = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    post_three_img_tall_a = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    post_three_img_tall_b = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    post_three_img_tall_c = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    post_four_img_wide_a = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    post_four_img_wide_b = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    post_four_img_tall = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    post_five_img_wide = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    post_five_img_square = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    parent_page_types = [BlogSearchPage]

    search_fields = Page.search_fields + [

    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('banner_image'),
        FieldPanel('intro'),
        MultiFieldPanel(
            [
                FieldPanel('post_one'),
                PageChooserPanel('post_one_page', 'blog.BlogPostPage'),
                FieldPanel('post_one_intro'),
                ImageChooserPanel('post_one_img_tall'),
                ImageChooserPanel('post_one_img_wide_a'),
                ImageChooserPanel('post_one_img_wide_b'),
            ],
            heading='Post One',
            classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                FieldPanel('post_two'),
                PageChooserPanel('post_two_page', 'blog.BlogPostPage'),
                FieldPanel('post_two_intro'),
                ImageChooserPanel('post_two_img_wide_a'),
                ImageChooserPanel('post_two_img_wide_b'),
            ],
            heading='Post Two',
            classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                FieldPanel('post_three'),
                PageChooserPanel('post_three_page', 'blog.BlogPostPage'),
                FieldPanel('post_three_intro'),
                ImageChooserPanel('post_three_img_tall_a'),
                ImageChooserPanel('post_three_img_tall_b'),
                ImageChooserPanel('post_three_img_tall_c'),
            ],
            heading='Post Three',
            classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                FieldPanel('post_four'),
                PageChooserPanel('post_four_page', 'blog.BlogPostPage'),
                FieldPanel('post_four_intro'),
                ImageChooserPanel('post_four_img_wide_a'),
                ImageChooserPanel('post_four_img_wide_b'),
                ImageChooserPanel('post_four_img_tall'),
            ],
            heading='Post Four',
            classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                FieldPanel('post_five'),
                PageChooserPanel('post_five_page', 'blog.BlogPostPage'),
                FieldPanel('post_five_intro'),
                ImageChooserPanel('post_five_img_wide'),
                ImageChooserPanel('post_five_img_square'),
            ],
            heading='Post Five',
            classname='collapsible collapsed'
        ),

    ]

    promote_panels = [
                         FieldPanel('sent_date'),
                         FieldPanel('debug_mode'),
                     ] + Page.promote_panels

    settings_panels = Page.settings_panels + [

    ]

    def get_context(self, request):
        context = super().get_context(request)

        root_url = 'https://www.hannahandkevin.net'

        context['homepage_url'] = root_url
        context['email_url'] = root_url + self.get_url()

        if (self.post_one is True) & (self.post_one_page is not None):
            context['post_one_url'] = root_url + self.post_one_page.get_url()
        if (self.post_two is True) & (self.post_two_page is not None):
            context['post_two_url'] = root_url + self.post_two_page.get_url()
        if (self.post_three is True) & (self.post_three_page is not None):
            context['post_three_url'] = root_url + self.post_three_page.get_url()
        if (self.post_four is True) & (self.post_four_page is not None):
            context['post_four_url'] = root_url + self.post_four_page.get_url()
        if (self.post_five is True) & (self.post_five_page is not None):
            context['post_five_url'] = root_url + self.post_five_page.get_url()

        return context


class BlogInstaPage(Page):
    insta_flag = models.BooleanField(default=False)
    insta_instant = models.DateTimeField(null=True, blank=True)
    insta_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    insta_comment = models.CharField(max_length=2000, null=True, blank=True)

    parent_page_types = [BlogSearchPage]

    content_panels = Page.content_panels + [
        FieldPanel('insta_flag'),
        FieldPanel('insta_instant'),
        ImageChooserPanel('insta_image'),
        FieldPanel('insta_comment'),

    ]

    promote_panels = [
                     ] + Page.promote_panels

    settings_panels = Page.settings_panels + [
    ]


class Profile(models.Model):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    secret_key = models.CharField(max_length=20, default='01234567899876543210')
    last_updated = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        from hashlib import blake2b
        data = bytearray()
        data.extend(map(ord, self.first_name + self.last_name + self.email + str(self.active)))
        secret_key = blake2b(data, digest_size=10).hexdigest()
        self.secret_key = secret_key
        super().save(*args, **kwargs)
