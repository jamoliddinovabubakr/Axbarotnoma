# Generated by Django 4.0.4 on 2022-05-10 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article_app', '0005_shartnoma_remove_article_shartnoma'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shartnoma',
            old_name='shartnoma',
            new_name='body',
        ),
    ]