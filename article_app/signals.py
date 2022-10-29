from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import MyResendArticle
from user_app.models import Notification, User


@receiver(post_save, sender=MyResendArticle)
def create_article(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            article=instance.article,
            title=instance.id,
            description='Yangi maqola',
            my_resend=instance,
            user=User.objects.filter(role__id=3).last()
        )
