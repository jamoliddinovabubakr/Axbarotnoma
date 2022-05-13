# Generated by Django 4.0.4 on 2022-05-13 10:44

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article_app', '0010_remove_article_author_article_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='url',
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=ckeditor.fields.RichTextField(max_length=255, verbose_name='Title'),
        ),
    ]
