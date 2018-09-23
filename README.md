# lkbw


Notes

pip install Wagtail==2.2.2
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

python3 ~/lkbw/manage.py <xxx> --settings=lkbw.settings.production

To Do

-Get mysql working in PRD
-Update PRD blog pages to render real content and remove sample content
-Eventually delete PRD sqlite db
-Add automatic site refresh to deploy script
-Update Wagtail max image size
-Enable automatic image cropping and compression
-Tie images back to Lightroom (for updates after posting) and figure out metadata/watermarks
-Update model and admin page for Blog and Blog Index (change to Blog Section)

Blog Section
-Title
-Intro
-Banner Image

Blog Page
-Title
-Intro
-Banner Image
-Stream



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