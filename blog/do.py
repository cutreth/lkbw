import re
from wagtail.core import hooks

geos_ptrn = re.compile(
    "^SRID=([0-9]{1,});POINT\((-?[0-9\.]{1,})\s(-?[0-9\.]{1,})\)$"
)


def geosgeometry_str_to_struct(value):
    '''
    Parses a geosgeometry string into struct.

    Example:
        SRID=5432;POINT(12.0 13.0)
    Returns:
        >> [5432, 12.0, 13.0]
    '''

    result = geos_ptrn.match(value)

    if not result:
        return None

    return {
        'srid': result.group(1),
        'x': result.group(2),
        'y': result.group(3),
    }


@hooks.register('after_create_page')
@hooks.register('after_edit_page')
def trigger_email(request, page):

    from mailin import Mailin
    from django.conf import settings
    from blog.models import BlogEmailPage, Profile
    from django.template.loader import render_to_string
    from django.http import HttpRequest
    from datetime import datetime

    is_email = bool(True) if page.specific_class == BlogEmailPage else bool(False)
    if not is_email:
        return None

    is_publishing = bool(request.POST.get('action-publish'))
    if is_publishing is False:
        return None

    is_sent = bool(False) if page.sent_date is None else bool(True)
    if is_sent is True:
        return None

    request = HttpRequest()
    request.method = 'GET'

    template = page.get_template(request)
    context = page.get_context(request)

    recipients = Profile.objects.filter(active=True)

    for receiver in recipients:
        to = receiver.first_name + ' ' + receiver.last_name
        email = receiver.email

        '''
        if to != 'Preston Davis':
            continue
        '''

        subject = page.title
        context['secret_key'] = receiver.secret_key

        body = render_to_string(template, context)

        m = Mailin("https://api.sendinblue.com/v2.0", settings.EMAIL_KEY)
        data = {"to": {email: to},
                "from": ["email@hannahandkevin.net", "H&K Away"],
                "replyto": ["reply@hannahandkevin.net", "H&K Away"],
                "subject": subject,
                "html": body,
                }
        result = m.send_email(data)

    page = page.specific
    page.sent_date = datetime.now()
    page.save()

    return None
