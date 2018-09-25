# lkbw


Notes

pip install Wagtail==2.2.2
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

python3 ~/lkbw/manage.py <xxx> --settings=lkbw.settings.production

To Do

-Add automatic site refresh to deploy script

-Update Wagtail max image size

-Enable automatic image cropping and compression

-Tie images back to Lightroom (for updates after posting) and figure out metadata/watermarks

-Update model and admin page for Blog and Blog Index (change to Blog Section), duplicate existing templates

-Pull "home" directory from Wagtail master, re-enable app in Settings
---https://github.com/wagtail/wagtail/tree/master/wagtail/project_template/home


Links

https://github.com/jaydensmith/wagtailfroala
https://github.com/Frojd/wagtail-geo-widget
https://github.com/springload/wagtailgmaps
https://github.com/heymonkeyriot/wagtailclearstream
https://github.com/UWKM/uwkm_streamfields

https://help.pythonanywhere.com/pages/API [set as part of deploy script]
https://help.pythonanywhere.com/pages/DjangoStaticFiles
https://help.pythonanywhere.com/pages/environment-variables-for-web-apps

https://www.pythonanywhere.com/forums/topic/89/
https://blog.pythonanywhere.com/155/
https://help.pythonanywhere.com/pages/API/
