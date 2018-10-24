# Generated by Django 2.0.8 on 2018-10-24 02:25

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtailgeowidget.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0028_blogsearchpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpostpage',
            name='body',
            field=wagtail.core.fields.StreamField([('header', wagtail.core.blocks.StructBlock([('header', wagtail.core.blocks.CharBlock())])), ('text', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.RichTextBlock())])), ('aside', wagtail.core.blocks.StructBlock([('aside', wagtail.core.blocks.BlockQuoteBlock())])), ('caption', wagtail.core.blocks.StructBlock([('caption', wagtail.core.blocks.CharBlock())])), ('quote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.CharBlock())])), ('date', wagtail.core.blocks.StructBlock([('date', wagtail.core.blocks.DateBlock())])), ('gallery', wagtail.core.blocks.StructBlock([('pictures', wagtail.core.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock()))])), ('picture', wagtail.core.blocks.StructBlock([('picture', wagtail.images.blocks.ImageChooserBlock())])), ('location', wagtail.core.blocks.StructBlock([('address', wagtail.core.blocks.CharBlock(required=False)), ('latt_long', wagtailgeowidget.blocks.GeoBlock(address_field='address'))])), ('place', wagtail.core.blocks.StructBlock([('q', wagtail.core.blocks.CharBlock())]))], blank=True, null=True),
        ),
    ]