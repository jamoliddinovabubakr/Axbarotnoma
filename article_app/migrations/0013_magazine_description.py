# Generated by Django 4.0.4 on 2022-06-29 07:26

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article_app', '0012_alter_article_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='magazine',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
