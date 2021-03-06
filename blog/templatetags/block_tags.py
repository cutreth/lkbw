from django import template
from django.conf import settings

from datetime import datetime

register = template.Library()


@register.simple_tag
def id_prefix():
    dt = datetime.now()
    ts = dt.microsecond
    return str(ts)


@register.filter
def cdn_url(value):
    aws_url = settings.AWS_CLOUDFRONT_URL

    if aws_url != '':
        old_url = settings.MEDIA_URL + 'images/'
        value = value.replace(old_url, aws_url)

    return value


@register.filter
def spotify_uri(value):

    value = value.replace("spotify:","")
    value = value.replace(":","/")
    return value


@register.filter
def email_source(value, arg):

    start = arg.find("/search/") + len("/search/")
    end = arg.rfind("/")
    value = value + "?utm_source=" + arg[start:end] + "&utm_medium=email"
    return value
