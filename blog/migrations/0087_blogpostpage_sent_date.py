# Generated by Django 2.2.4 on 2019-10-09 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0086_profile_email_per_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpostpage',
            name='sent_date',
            field=models.DateField(blank=True, null=True, verbose_name='Sent date'),
        ),
    ]
