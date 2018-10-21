from django import template

from datetime import datetime

register = template.Library()


@register.simple_tag
def id_prefix():
    dt = datetime.now()
    ts = dt.microsecond
    return str(ts)
