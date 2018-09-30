# lkbw

Enable automatic image cropping [lose 10% all around] and quality update [85] for original file
Need to figure out flow to prevent double cropping when editing existing images (maybe inject into image rendition code?)
-https://willow.readthedocs.io/en/latest/guide/operations.html
-http://docs.wagtail.io/en/v2.2.2/advanced_topics/images/custom_image_model.html
-https://docs.djangoproject.com/en/2.1/topics/db/models/
-https://stackoverflow.com/questions/4269605/django-override-save-for-model

Think about bulk image upload strategy
-https://stackoverflow.com/questions/48976797/how-to-make-image-gallery-from-zip-archive-in-wagtail
-https://stackoverflow.com/questions/43178845/create-collection-with-python-code
-https://gist.github.com/eyesee1/1ea8e1b90bfe632cd31f5a90afc0370c
-https://groups.google.com/forum/#!msg/wagtail/NGEPyEbTUHA/Z5J49yY5AwAJ

Update presentation of images on posts to optionally include caption (image title)
Adjust header stream block with toggles for control over head type (reference CSS for options)
Adjust date stream block to be centered with control over formatting (header, body, etc.)
Clean up header and footer: comment out and remove cruft
Wire up menus (based on other children from root: blog feed, contact us, about us, subscribe)
-https://github.com/rkhleics/wagtailmenus
-https://www.tivix.com/blog/working-with-wagtail-menus

Clean up templates by removing if statements in stream block; define explicit templates instead

Finish static migration
-Shorten directory name for template CSS
-Add "collectstatic" as a deployment step in PRD
-Update static mappings in PRD to just point to root directory
-Remove manual static entries for both mapping modules

Build out stream block for embedded mapping
Investigate combined block with multiple elements
Remove dev environment references to wagtailgeowidget and wagtailgmaps(models.py, dev. py), delete manually copied static files
Create new admin widget for mapping
Create new HTML tempate for mapping
-https://github.com/Frojd/wagtail-geo-widget [only reference this for use injecting widgets within streamfields]
-https://github.com/springload/wagtailgmaps [copy this functionality in total]
-https://github.com/UWKM/uwkm_streamfields
-https://developers.google.com/maps/documentation/javascript/adding-a-google-map

Wire up SendInBlue emails against either a blog post page with added fields or a new child "email" related page

python3 ~/lkbw/manage.py <xxx> --settings=lkbw.settings.production

https://help.pythonanywhere.com/pages/DjangoStaticFiles
https://help.pythonanywhere.com/pages/environment-variables-for-web-apps
