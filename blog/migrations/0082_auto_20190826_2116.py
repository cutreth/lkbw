# Generated by Django 2.2.4 on 2019-08-26 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0081_auto_20190826_2103'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpostpage',
            old_name='insta_flg',
            new_name='insta_flag',
        ),
    ]
