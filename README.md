# lkbw

Enable automatic image cropping [lose 10% all around] and quality update [85] for original file
Need to figure out flow to prevent double cropping when editing existing images
  https://willow.readthedocs.io/en/latest/guide/operations.html
  http://docs.wagtail.io/en/v2.2.2/advanced_topics/images/custom_image_model.html
  https://docs.djangoproject.com/en/2.1/topics/db/models/
  https://stackoverflow.com/questions/4269605/django-override-save-for-model

Configure section/post pages to use defined header images
Update presentation of images on posts to optionally include caption (image title)
Adjust header stream block with toggles for control over head type (reference CSS for options)
Build out stream block for embedded mapping

Test other Wagtail packages
  https://github.com/jaydensmith/wagtailfroala
  https://github.com/Frojd/wagtail-geo-widget
  https://github.com/springload/wagtailgmaps
  https://github.com/heymonkeyriot/wagtailclearstream
  https://github.com/UWKM/uwkm_streamfields

python3 ~/lkbw/manage.py <xxx> --settings=lkbw.settings.production

https://help.pythonanywhere.com/pages/DjangoStaticFiles
https://help.pythonanywhere.com/pages/environment-variables-for-web-apps
