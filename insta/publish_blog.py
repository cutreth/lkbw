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


def background_sleep():
    max_wait = 60 * 29
    actual_wait = randrange(0, max_wait)
    time.sleep(actual_wait)


def check_time():
    time_ok = False
    hour = datetime.now(pytz.timezone("America/Chicago")).hour
    if (hour == 16) | True:  # Don't forget to reset flag to FALSE
        time_ok = True
    return time_ok


def get_post():
    next_post = BlogPostPage.objects.live().filter(insta_flag=True, insta_instant=None).order_by('post_date')[0]
    return next_post


def publish_post(post):
    title = post.title
    intro = post.intro
    search_key = post.search_key
    caption = title + ': ' + intro + ' | ' + 'To read this post, click the link in my bio and search for: ' + search_key

    image = post.banner_image
    image_path = 'temp/' + image.title
    rendition_url = image.get_rendition('max-1080x1080').url
    root_url = post.get_url_parts()[1]
    image_url = root_url + rendition_url

    urllib.request.urlretrieve(image_url, image_path)

    username = settings.INSTA_KEY.split('|')[0]
    password = settings.INSTA_KEY.split('|')[1]
    cookie_file = settings.INSTA_KEY.split('|')[2]

    with client(username, password, cookie_file=cookie_file, write_cookie_file=True) as cli:
        cli.upload(image_path, caption)

    now = datetime.now(pytz.timezone("America/Chicago"))
    post.insta_instant = now
    post.save_revision().publish()

    os.remove(image_path)


if check_time():
    thread = threading.Thread(target=background_sleep)
    thread.start()
    thread.join()
    post = get_post()
    publish_post(post)
