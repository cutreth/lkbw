# Generated by Django 2.0.8 on 2018-10-30 02:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0033_blogsectionpage_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogsectionpage',
            name='intro',
        ),
    ]
