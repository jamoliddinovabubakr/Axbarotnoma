# Generated by Django 4.0.4 on 2022-05-13 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0008_user_author_order_user_work_place'),
        ('article_app', '0011_remove_article_url_alter_article_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='file',
            field=models.FileField(max_length=255, upload_to='files/', verbose_name='Fayl'),
        ),
        migrations.AlterField(
            model_name='article',
            name='state_analysis',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_state_analysis', to='user_app.state'),
        ),
        migrations.AlterField(
            model_name='article',
            name='state_edit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_state_edit', to='user_app.state'),
        ),
    ]
