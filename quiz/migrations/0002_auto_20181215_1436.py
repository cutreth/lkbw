# Generated by Django 2.0.8 on 2018-12-15 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AlterField(
            model_name='question',
            name='ask_date',
            field=models.DateField(),
        ),
    ]
