import subprocess
import json
import hmac
from hashlib import sha1

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import force_bytes

from django.contrib.syndication.views import Feed
from blog.models import BlogHomePage, BlogPostPage


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
            profile = Profile.objects.filter(email=form.cleaned_data.get('email'), first_name=form.cleaned_data.get('first_name'), last_name=form.cleaned_data.get('last_name')).first()
            if profile is not None:
                secret_key = request.GET.get('key')
                if secret_key == profile.secret_key:
                    profile.active = False
                    profile.save()
                else:
                    error = 'Your subscription key does not match. Please try again, navigating to this page via the "Unsubscribe" link in the most recent email that you have received.'
                    context = {'error': error}
                    return render(request, 'error.html', context)
            else:
                error = 'An existing subscription matching your email address and names cannot be found. Please try again with the same information that you used to subscribe originally.'
                context = {'error': error}
                return render(request, 'error.html', context)
            return redirect('https://www.hannahandkevin.net')

    else:
        form = UnsubscribeForm()

    return render(request, 'unsubscribe.html', {'form': form})


def contact(request):

    from mailin import Mailin
    from django.conf import settings

    from blog.forms import ContactForm
    from django.shortcuts import render, redirect

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            to = {'kevin@hannahandkevin.net': 'Kevin', 'hannah@hannahanekevin.net': 'Hannah'}
            from_name = form.cleaned_data.get('name')
            from_email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            body = form.cleaned_data.get('message')

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
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


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
