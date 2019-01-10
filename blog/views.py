import subprocess
import json
import hmac
from hashlib import sha1

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError, Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import force_bytes


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

    payload = json.loads(request.body)

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
                return redirect('https://www.lilkevbigworld.com')
            else:
                if (profile.first_name == form.cleaned_data.get('first_name')) & (profile.last_name == form.cleaned_data.get('last_name')):
                    profile.active = True
                    profile.save()
                else:
                    error = 'Name mismatch'
                    context = {'error': error}
                    return render(request, 'error.html', context)
            return redirect('https://www.lilkevbigworld.com')

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
                    error = 'Key mismatch'
                    context = {'error': error}
                    return render(request, 'error.html', context)
            else:
                error = 'Profile not found'
                context = {'error': error}
                return render(request, 'error.html', context)
            return redirect('https://www.lilkevbigworld.com')

    else:
        form = UnsubscribeForm()

    return render(request, 'unsubscribe.html', {'form': form})
