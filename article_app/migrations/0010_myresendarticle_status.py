# Generated by Django 4.0.4 on 2022-10-06 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_app', '0009_myresendarticle_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='myresendarticle',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
