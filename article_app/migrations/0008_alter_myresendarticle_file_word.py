# Generated by Django 4.0.4 on 2022-09-19 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_app', '0007_alter_article_options_remove_article_message_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myresendarticle',
            name='file_word',
            field=models.FileField(blank=True, max_length=255, upload_to='files/', verbose_name='Word Fayl'),
        ),
    ]