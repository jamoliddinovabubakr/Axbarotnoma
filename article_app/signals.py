from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


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