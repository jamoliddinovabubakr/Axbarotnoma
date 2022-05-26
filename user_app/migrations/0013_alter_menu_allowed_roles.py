# Generated by Django 4.0.4 on 2022-05-23 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0012_remove_menu_allow_analyst_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='allowed_roles',
            field=models.ManyToManyField(blank=True, null=True, related_name='allowed_role_menus', to='user_app.role'),
        ),
    ]