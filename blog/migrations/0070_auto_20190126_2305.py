# Generated by Django 2.1.5 on 2019-01-27 05:05

import blog.blocks
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0069_auto_20190123_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloghomepage',
            name='body',
            field=wagtail.core.fields.StreamField([('header', wagtail.core.blocks.StructBlock([('header', wagtail.core.blocks.CharBlock())])), ('date', wagtail.core.blocks.StructBlock([('date', wagtail.core.blocks.DateBlock())])), ('text', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.RichTextBlock())])), ('aside', wagtail.core.blocks.StructBlock([('aside', wagtail.core.blocks.BlockQuoteBlock())])), ('caption', wagtail.core.blocks.StructBlock([('caption', wagtail.core.blocks.CharBlock())])), ('flickity', wagtail.core.blocks.StructBlock([('pictures', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.CharBlock(required=False)), ('date', wagtail.core.blocks.DateBlock(required=False))])))])), ('location', wagtail.core.blocks.StructBlock([('address', wagtail.core.blocks.CharBlock(required=False)), ('place', wagtail.core.blocks.CharBlock(required=False)), ('zoom', wagtail.core.blocks.CharBlock(required=False)), ('location', blog.blocks.PlaceBlock(address_field='address', place_field='place', zoom_field='zoom')), ('satellite', wagtail.core.blocks.BooleanBlock(required=False)), ('date', wagtail.core.blocks.DateBlock(required=False))])), ('place', wagtail.core.blocks.StructBlock([('address', wagtail.core.blocks.CharBlock(required=False)), ('place', wagtail.core.blocks.CharBlock()), ('zoom', wagtail.core.blocks.CharBlock(required=False)), ('location', blog.blocks.PlaceBlock(address_field='address', place_field='place', zoom_field='zoom')), ('satellite', wagtail.core.blocks.BooleanBlock(required=False)), ('date', wagtail.core.blocks.DateBlock(required=False))])), ('tracker', wagtail.core.blocks.StructBlock([('stops', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('address', wagtail.core.blocks.CharBlock(required=False)), ('place', wagtail.core.blocks.CharBlock(required=False)), ('spot', blog.blocks.PlaceBlock(address_field='address', place_field='place')), ('title', wagtail.core.blocks.CharBlock(required=False)), ('caption', wagtail.core.blocks.CharBlock(required=False)), ('page', wagtail.core.blocks.PageChooserBlock(required=False))])))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='blogpostpage',
            name='body',
            field=wagtail.core.fields.StreamField([('header', wagtail.core.blocks.StructBlock([('header', wagtail.core.blocks.CharBlock())])), ('date', wagtail.core.blocks.StructBlock([('date', wagtail.core.blocks.DateBlock())])), ('text', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.RichTextBlock())])), ('aside', wagtail.core.blocks.StructBlock([('aside', wagtail.core.blocks.BlockQuoteBlock())])), ('caption', wagtail.core.blocks.StructBlock([('caption', wagtail.core.blocks.CharBlock())])), ('flickity', wagtail.core.blocks.StructBlock([('pictures', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.CharBlock(required=False)), ('date', wagtail.core.blocks.DateBlock(required=False))])))])), ('location', wagtail.core.blocks.StructBlock([('address', wagtail.core.blocks.CharBlock(required=False)), ('place', wagtail.core.blocks.CharBlock(required=False)), ('zoom', wagtail.core.blocks.CharBlock(required=False)), ('location', blog.blocks.PlaceBlock(address_field='address', place_field='place', zoom_field='zoom')), ('satellite', wagtail.core.blocks.BooleanBlock(required=False)), ('date', wagtail.core.blocks.DateBlock(required=False))])), ('place', wagtail.core.blocks.StructBlock([('address', wagtail.core.blocks.CharBlock(required=False)), ('place', wagtail.core.blocks.CharBlock()), ('zoom', wagtail.core.blocks.CharBlock(required=False)), ('location', blog.blocks.PlaceBlock(address_field='address', place_field='place', zoom_field='zoom')), ('satellite', wagtail.core.blocks.BooleanBlock(required=False)), ('date', wagtail.core.blocks.DateBlock(required=False))])), ('tracker', wagtail.core.blocks.StructBlock([('stops', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('address', wagtail.core.blocks.CharBlock(required=False)), ('place', wagtail.core.blocks.CharBlock(required=False)), ('spot', blog.blocks.PlaceBlock(address_field='address', place_field='place')), ('title', wagtail.core.blocks.CharBlock(required=False)), ('caption', wagtail.core.blocks.CharBlock(required=False)), ('page', wagtail.core.blocks.PageChooserBlock(required=False))])))]))], blank=True, null=True),
        ),
    ]
