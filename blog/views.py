import subprocess
import json
import hmac
from hashlib import sha1

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError, Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import force_bytes
from django.shortcuts import render

from django.contrib.syndication.views import Feed
from wagtail.images.models import Image
from wagtail.core.models import Collection, CollectionMember
from blog.models import BlogHomePage, BlogPostPage, BlogInstaPage, BlogSectionPage


@csrf_exempt
def deploy(request):

    # Verify the request signature
    header_signature = request.META.get('HTTP_X_HUB_SIGNATURE')
    if header_signature is None:
        return HttpResponseForbidden('Permission denied.')

    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha1':
        return HttpResponseServerError('Operation not supported.', status=501)

    mac = hmac.new(force_bytes(settings.GITHUB_WEBHOOK_KEY), msg=force_bytes(request.body), digestmod=sha1)
    if not hmac.compare_digest(force_bytes(mac.hexdigest()), force_bytes(signature)):
        return HttpResponseForbidden('Permission denied.')

    # If request reached this point we are in a good shape

    payload = json.loads(request.body)
    ref = payload["ref"]
    
    if ref == 'refs/heads/master':
        p = subprocess.Popen("~/scripts/deploy.sh", shell=True)
        return HttpResponse('Deploying')
    else:
        return HttpResponse('Not master')


@csrf_exempt
def email(request):

    from mailin import Mailin
    from django.conf import settings

    to = 'Lil Kev'
    email = 'email@hannahandkevin.net'

    subject = 'SiB Web Hook'
    body = str(request.body)

    m = Mailin("https://api.sendinblue.com/v2.0", settings.EMAIL_KEY)
    data = {"to": {email: to},
            "from": ["email@hannahandkevin.net", "H&K Away"],
            "replyto": ["reply@hannahandkevin.net", "H&K Away"],
            "subject": subject,
            "html": body,
            }
    result = m.send_email(data)

    return HttpResponse('OK')


def subscribe(request):

    from blog.models import Profile
    from blog.forms import SubscribeForm
    from django.shortcuts import render, redirect

    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            profile = Profile.objects.filter(email=form.cleaned_data.get('email')).first()
            if profile is None:
                form.save()
                return redirect('https://www.hannahandkevin.net')
            else:
                if (profile.first_name == form.cleaned_data.get('first_name')) & (profile.last_name == form.cleaned_data.get('last_name')):
                    profile.active = True
                    profile.save()
                else:
                    error = 'An existing subscription with that email address already exists but the names you entered do not match. Please try again with the same names that you subscribed with originally.'
                    context = {'error': error}
                    return render(request, 'error.html', context)
            return redirect('https://www.hannahandkevin.net')

    else:
        form = SubscribeForm()

    return render(request, 'subscribe.html', {'form': form})


def unsubscribe(request):

    from blog.models import Profile
    from blog.forms import UnsubscribeForm
    from django.shortcuts import render, redirect

    if request.method == 'POST':
        form = UnsubscribeForm(request.POST)
        if form.is_valid():
            profile = Profile.objects.filter(email=form.cleaned_data.get('email')).first()
            if profile is not None:
                form_first = form.cleaned_data.get('first_name')
                form_last = form.cleaned_data.get('last_name')
                profile_first = profile.first_name
                profile_last = profile.last_name
                if (form_first == profile_first) & (form_last == profile_last):
                    profile.active = False
                    profile.save()
                else:
                    error = 'An existing subscription matching that email address and name cannot be found. Hint: match the email recipient name.'
                    context = {'error': error}
                    return render(request, 'error.html', context)
            else:
                error = 'An existing subscription matching that email address cannot be found.'
                context = {'error': error}
                return render(request, 'error.html', context)
            return redirect('https://www.hannahandkevin.net')

    else:
        form = UnsubscribeForm()

    return render(request, 'unsubscribe.html', {'form': form})


def contact(request):

    import time
    import requests
    from mailin import Mailin
    from django.conf import settings

    from blog.forms import ContactForm
    from django.shortcuts import render, redirect
    from django.utils.html import linebreaks

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.CAPTCHA_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' End reCAPTCHA validation '''

            now = time.time()
            last_comment = request.session.get('last_comment', 0)
            request.session['last_comment'] = now

            if not result['success']:
                error = 'Are you a robot? Google seems to think so...'
                context = {'error': error}
                return render(request, 'error.html', context)

            if now - last_comment > 60:
                to = {'kevin@hannahandkevin.net': 'Kevin', 'hannah@hannahandkevin.net': 'Hannah'}
                from_name = form.cleaned_data.get('name')
                from_email = form.cleaned_data.get('email')
                subject = form.cleaned_data.get('subject')
                body = linebreaks(form.cleaned_data.get('message'))

                m = Mailin("https://api.sendinblue.com/v2.0", settings.EMAIL_KEY)
                data = {"to": to,
                        "from": ["email@hannahandkevin.net", from_name],
                        "replyto": [from_email, from_name],
                        "subject": subject,
                        "html": body,
                        }
                result = m.send_email(data)
                return redirect('https://www.hannahandkevin.net')
            else:
                error = 'There is a one minute wait timer between sends. Please go back, wait a moment, and try again.'
                context = {'error': error}
                return render(request, 'error.html', context)

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def unused(request):

    if not request.user.id:
        raise Http404

    published_sections = BlogSectionPage.objects.live()
    published_posts = BlogPostPage.objects.live()

    collection_filter = request.GET.get('collection')

    if collection_filter:
        collection = Collection.objects.filter(id=collection_filter)
    else:
        collection = None

    if collection:
        image_list = list(Image.objects.filter(collection__in=collection))
        collection = collection.first()
    else:
        image_list = list(Image.objects.all())

    for section in published_sections:
        image = section.banner_image
        if image in image_list:
            image_list.remove(image)

    for post in published_posts:
        image = post.banner_image
        if image in image_list:
            image_list.remove(image)

        for block in post.body.stream_data:
            if block['type'] == 'flickity':
                for picture in block['value']['pictures']:
                    image_id = picture['image']
                    image = Image.objects.get(pk=image_id)
                    if image in image_list:
                        image_list.remove(image)

    context = {'unused_images': image_list, 'collection': collection}
    return render(request, 'unused.html', context)


def insta(request):

    if not request.user.id:
        raise Http404

    post_list = BlogPostPage.objects.live().filter(insta_flag=True, insta_instant=None).order_by('post_date')
    image_list = BlogInstaPage.objects.live().filter(insta_flag=True, insta_instant=None)

    context = {'post_list': post_list, 'image_list': image_list}
    return render(request, 'insta.html', context)


class rss(Feed):
    title = 'H&K Away'
    link = ''
    description = ''

    def items(self):
        homepage = BlogHomePage.objects.all()[0]
        blogpages = homepage.get_descendants().live().type(BlogPostPage).order_by('-blogpostpage__post_date', 'title')
        return blogpages

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.specific.intro

    def item_link(self, item):
        return item.url
