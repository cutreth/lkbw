import os
import time
import threading
import pytz
import urllib.request

from datetime import datetime
from random import randrange
from instapy_cli import client
from blog.models import BlogPostPage
from django.conf import settings
from django.core.management.base import BaseCommand


def background_sleep():
    max_wait = 60 * 29
    actual_wait = randrange(0, 5)  # Don't forget to replace upper bound with max_wait
    time.sleep(actual_wait)


def check_time():
    time_ok = False
    hour = datetime.now(pytz.timezone("America/Chicago")).hour
    if (hour == 16) | True:  # Don't forget to reset flag to FALSE
        time_ok = True
    return time_ok


def get_post():
    post_list = BlogPostPage.objects.live().filter(insta_flag=True, insta_instant=None).order_by('post_date')
    if len(post_list):
        next_post = post_list[0]
    else:
        next_post = None
    return next_post


def publish_post(post):
    title = post.title
    intro = post.intro
    search_key = post.search_key
    caption = title + ': ' + intro + ' | ' + 'To read this post, click the link in my bio and search for: ' + search_key

    image = post.banner_image
    image_path = image.title
    rendition_url = image.get_rendition('max-1080x1080').url
    s3_url = 'https://lkbw.s3.amazonaws.com/images/'
    cf_url = 'https://d1e9v6y517kw0o.cloudfront.net/'
    image_url = rendition_url.replace(s3_url,cf_url)

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(image_url, image_path)

    username = settings.INSTA_KEY.split('|')[0]
    password = settings.INSTA_KEY.split('|')[1]
    cookie_file = settings.INSTA_KEY.split('|')[2]

    cookie_path = cookie_file

    with client(username, password, cookie_file=cookie_path, write_cookie_file=True) as cli:
        cli.upload(image_path, caption)

    now = datetime.now(pytz.timezone("America/Chicago"))
    post.insta_instant = now
    post.save_revision().publish()

    os.remove(image_path)


class Command(BaseCommand):

    def handle(self, *args, **options):
        if check_time():
            thread = threading.Thread(target=background_sleep)
            thread.start()
            thread.join()
            post = get_post()
            if post:
                publish_post(post)
        return None
