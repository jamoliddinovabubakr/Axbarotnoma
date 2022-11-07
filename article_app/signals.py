# from django.db.models.signals import pre_save, post_save
# from django.dispatch import receiver
#
# from article_app.models import Submission, Notification, NotificationStatus
#
#
# @receiver(post_save, sender=Submission)
# def create_article(sender, instance, created, **kwargs):
#     if created:
#         Notification.objects.create(
#             submission_id=instance.id,
#             from_user_id=instance.author_id,
#             to_user_id=instance.editor_id,
#             message="",
#             notification_status_id=NotificationStatus.objects.get_or_create(name="unread"),
#         )
