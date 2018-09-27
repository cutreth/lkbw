# lkbw
  
Enable automatic image cropping [lose 10% all around] and quality update [85] for original file  
Need to figure out flow to prevent double cropping when editing existing images  
-https://willow.readthedocs.io/en/latest/guide/operations.html  
-http://docs.wagtail.io/en/v2.2.2/advanced_topics/images/custom_image_model.html  
-https://docs.djangoproject.com/en/2.1/topics/db/models/  
-https://stackoverflow.com/questions/4269605/django-override-save-for-model  
  
Update presentation of images on posts to optionally include caption (image title)  
Adjust header stream block with toggles for control over head type (reference CSS for options)  
Adjust date stream block to be centered with control over formatting (header, body, etc.)  
  
Enable emailing  
  
Clean up header and footer: comment out and remove cruft  
Wire up menus  
-https://github.com/rkhleics/wagtailmenus  
-https://www.tivix.com/blog/working-with-wagtail-menus  
  
Configure better static file system (collectstatic)  
Update core settings  
-https://docs.wagtail.io/en/v2.2.2/advanced_topics/settings.html  
Configure recurring tasks (publish posts, garbage cleanup, etc.)  
-https://docs.wagtail.io/en/v2.2.2/reference/management_commands.html  
  
Enable caching and searching  
-https://docs.wagtail.io/en/v2.2.2/advanced_topics/performance.html  
Reconfigure tagging  
-http://docs.wagtail.io/en/v2.2.2/reference/pages/model_recipes.html#tagging  
  
Build out stream block for embedded mapping  
-https://github.com/Frojd/wagtail-geo-widget  
-https://github.com/springload/wagtailgmaps  
-https://github.com/UWKM/uwkm_streamfields  
-https://developers.google.com/maps/documentation/javascript/adding-a-google-map  
  
python3 ~/lkbw/manage.py <xxx> --settings=lkbw.settings.production  
  
https://help.pythonanywhere.com/pages/DjangoStaticFiles  
https://help.pythonanywhere.com/pages/environment-variables-for-web-apps  
