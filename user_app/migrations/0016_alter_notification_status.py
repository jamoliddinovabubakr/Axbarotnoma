# Generated by Django 4.0.4 on 2022-05-25 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0015_alter_notification_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.CharField(blank=True, choices=[(0, "O'qilmadi"), (1, "O'qildi")], max_length=50, null=True),
        ),
    ]
