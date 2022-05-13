# Generated by Django 4.0.4 on 2022-05-13 05:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article_app', '0009_delete_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ManyToManyField(blank=True, null=True, related_name='article_authors', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
    ]