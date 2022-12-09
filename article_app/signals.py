from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from article_app.models import Article, Notification, NotificationStatus
from user_app.models import User, Role, Editor


@receiver(post_save, sender=Article)
def create_article(sender, instance, created, **kwargs):
    editor = Editor.objects.all().last()
    if created:
        print(123)
    else:
        if instance.article_status.id == 6:
            Notification.objects.create(
                article=instance,
                from_user=instance.author,
                to_user=editor.user,
                message=f"({editor.user.email})Assalomu aleykum. Yangi maqolamni yubordim!",
                notification_status=NotificationStatus.objects.get(id=1),
                is_update_article=True,
            )

        if instance.article_status.id == 8:
            Notification.objects.create(
                article=instance,
                from_user=instance.author,
                to_user=editor.user,
                message=f"({editor.user.email})Assalomu aleykum. Maqolamni to'g'irlab qayta yubordim!",
                notification_status=NotificationStatus.objects.get(id=1),
                is_update_article=True,
            )