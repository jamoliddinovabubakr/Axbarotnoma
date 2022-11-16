from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from article_app.models import Article, Notification, NotificationStatus
from user_app.models import User, Role, Editor


@receiver(post_save, sender=Article)
def create_article(sender, instance, created, **kwargs):
    if instance.article_status.id == 1:
        editor = Editor.objects.all().first()

        Notification.objects.create(
            article=instance,
            from_user=instance.author,
            to_user=editor.user,
            message="",
            notification_status=NotificationStatus.objects.get(id=1),
        )
