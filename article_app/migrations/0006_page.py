# Generated by Django 4.0.4 on 2022-05-17 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_app', '0005_rename_midlle_name_authors_middle_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveBigIntegerField(default=5, unique=True)),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
        ),
    ]