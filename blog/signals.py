from wagtail.core.signals import page_published
from blog.models import BlogPostPage, BlogEmailPage


def post_send(sender, **kwargs):

    from mailin import Mailin
    from django.conf import settings
    from blog.models import Profile
    from django.template.loader import render_to_string
    from datetime import datetime

    page = kwargs['instance']
    subject = page.title + ' | ' + page.intro
    banner_image = page.banner_image
    banner_image_url = banner_image.get_rendition('fill-580x280').url
    homepage_url = "https://www.hannahandkevin.net" + "?utm_source=post-send&utm_medium=email"
    post_url = page.full_url + "?utm_source=post-send&utm_medium=email"

    context = {"banner_image_url": banner_image_url, "banner_image": banner_image, "homepage_url": homepage_url, "post_url": post_url}

    body = render_to_string('post_email.html', context)

    recipients = Profile.objects.filter(active=True, email_per_post=True)

    for receiver in recipients:

        to = receiver.first_name + ' ' + receiver.last_name
        email = receiver.email

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

    pass


def email_send(sender, **kwargs):

    print(sender)

    pass


page_published.connect(post_send, sender=BlogPostPage)
page_published.connect(email_send, sender=BlogEmailPage)
