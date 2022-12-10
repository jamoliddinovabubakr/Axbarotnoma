from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from article_app.models import Article, Notification, NotificationStatus
from user_app.models import User, Role, Editor


@receiver(post_save, sender=Article)
def create_article(sender, instance, created, **kwargs):
    if created:
        print(123)
