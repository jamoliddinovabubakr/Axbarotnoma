# Generated by Django 4.0.4 on 2022-05-16 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article_app', '0004_alter_article_abstract_alter_article_references'),
    ]

    operations = [
        migrations.RenameField(
            model_name='authors',
            old_name='midlle_name',
            new_name='middle_name',
        ),
    ]
