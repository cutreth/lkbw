from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponse
from django.views.generic.base import RedirectView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from blog import views as blog_views
from quiz import urls as quiz_urls

favicon_view = RedirectView.as_view(url='/static/favicon/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),

    url(r'^lkbw-admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^quiz/', include(quiz_urls)),
    url(r'^api/deploy/$', blog_views.deploy, name='deploy'),
    url(r'^api/email/$', blog_views.email, name='email'),
    url(r'^robots.txt', lambda x: HttpResponse("User-Agent: *\nDisallow:", content_type="text/plain"), name="robots_file"),
    url(r'^favicon.ico', favicon_view),
    url(r'^unsubscribe/$', blog_views.unsubscribe, name='unsubscribe'),
    url(r'^subscribe/$', blog_views.subscribe, name='subscribe'),
    url(r'^contact/$', blog_views.contact, name='contact'),
    url(r'^rss/$', blog_views.rss(), name='rss'),


    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
