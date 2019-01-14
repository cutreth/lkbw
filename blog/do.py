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


# @hooks.register('after_create_page')
def seed_email(request, page):

    from blog.models import BlogEmailPage

    is_email = bool(True) if page.specific_class == BlogEmailPage else bool(False)
    if not is_email:
        return None

    page = page.specific

    is_publishing = bool(request.POST.get('action-publish'))
    if is_publishing is True:
        return None

    is_sent = bool(False) if page.sent_date is None else bool(True)
    if is_sent is True:
        return None

    if (page.post_one is True) & (page.post_one_page is not None):

        post_one = page.post_one_page.specific

        for block in post_one.body:
            if block.block_type == 'text':
                rtf = block.value['text'].source
                rtf = rtf[:250] if len(rtf) >250 else rtf
                page.post_one_intro = rtf
                page.save()
                # id=19: page.body[0].value['text'].source
                # this needs to be converted from RTF and then shrunk to 250 characters
                break

        for block in post_one.body:
            if block.block_type == 'flickity':
                img_one = block.value['pictures'][0]['image']
                page.post_one_img_tall = img_one
                page.save()
                # id=19: page.body[7].value['pictures'] (this is a list; add [0], etc. to iterate)
                # page.body[7].value['pictures'][0]['image'] links to the core picture
                break

    return None


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

        subject = page.title
        context['secret_key'] = receiver.secret_key

        body = render_to_string(template, context)

        m = Mailin("https://api.sendinblue.com/v2.0", settings.EMAIL_KEY)
        data = {"to": {email: to},
                "from": ["email@lilkevbigworld.com", "Lil Kev Big World"],
                "replyto": ["reply@lilkevbigworld.com", "Lil Kev Big World"],
                "subject": subject,
                "html": body,
                }
        result = m.send_email(data)

    page = page.specific
    page.sent_date = datetime.now()
    page.save()

    return None
