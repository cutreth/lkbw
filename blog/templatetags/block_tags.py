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

    if aws_url:
        old_url = settings.MEDIA_URL + '/images/'
        value = value.replace(old_url, aws_url)

    return value
