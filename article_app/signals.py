from turtle import title
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .models import Article
from user_app.models import Notification


@receiver(post_save, sender=Article)
def update_article(sender, instance, created, **kwargs):
    notif = get_object_or_404(Notification, article=instance)
    if not created and notif is None :
        Notification.objects.create(
            article = instance,
            title = instance.title,
            description='Yangi maqola',
        )