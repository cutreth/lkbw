# Generated by Django 2.0.8 on 2018-10-20 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_bloghomepage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloghomepage',
            name='q',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]