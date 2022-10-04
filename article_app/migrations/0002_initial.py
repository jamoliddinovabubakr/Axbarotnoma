# Generated by Django 4.0.4 on 2022-09-12 10:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article_app', '0001_initial'),
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='analyst',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_analyst', to=settings.AUTH_USER_MODEL, verbose_name='Tahlilchi'),
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_author', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='article_app.category', verbose_name='Kategoriya'),
        ),
        migrations.AddField(
            model_name='article',
            name='editor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_editor', to=settings.AUTH_USER_MODEL, verbose_name='Taxrirchi'),
        ),
        migrations.AddField(
            model_name='article',
            name='state_analysis',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_state_analysis', to='user_app.state'),
        ),
        migrations.AddField(
            model_name='article',
            name='state_edit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_state_edit', to='user_app.state'),
        ),
    ]