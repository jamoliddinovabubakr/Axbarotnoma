from ast import Not
from tkinter.messagebox import NO
from turtle import title
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .models import Article
from user_app.models import Notification


@receiver(post_save, sender=Article)
def create_article(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
        article = instance,
        title = instance.title,
        description='Yangi maqola',
    )