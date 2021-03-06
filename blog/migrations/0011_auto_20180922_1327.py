# Generated by Django 2.0.8 on 2018-09-22 18:27

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20180917_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='body2',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('date', wagtail.core.blocks.DateBlock()), ('html', wagtail.core.blocks.RawHTMLBlock()), ('quote', wagtail.core.blocks.BlockQuoteBlock())]),
        ),
    ]
