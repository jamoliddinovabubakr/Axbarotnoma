# Generated by Django 4.0.4 on 2022-05-13 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article_app', '0008_author_oreder'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Author',
        ),
    ]