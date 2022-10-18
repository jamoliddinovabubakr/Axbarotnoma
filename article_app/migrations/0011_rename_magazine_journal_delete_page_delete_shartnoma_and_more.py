# Generated by Django 4.0.4 on 2022-10-18 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_app', '0010_myresendarticle_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Magazine',
            new_name='Journal',
        ),
        migrations.DeleteModel(
            name='Page',
        ),
        migrations.DeleteModel(
            name='Shartnoma',
        ),
        migrations.RemoveField(
            model_name='article',
            name='analyst',
        ),
        migrations.RemoveField(
            model_name='article',
            name='editor',
        ),
        migrations.RemoveField(
            model_name='article',
            name='payed',
        ),
        migrations.RemoveField(
            model_name='article',
            name='status',
        ),
        migrations.RemoveField(
            model_name='article',
            name='step_bosh_muharrir',
        ),
        migrations.RemoveField(
            model_name='article',
            name='step_taqriz',
        ),
        migrations.RemoveField(
            model_name='category',
            name='key',
        ),
        migrations.AlterField(
            model_name='authors',
            name='email',
            field=models.EmailField(max_length=255, verbose_name='Email'),
        ),
    ]