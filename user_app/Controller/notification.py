from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from user_app.decorators import allowed_users
from user_app.models import Notification
from article_app.models import Authors
from user_app.forms import CreateNotificationForm


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def get_notifications(request):
    notifications = Notification.objects.order_by("-created_at").filter(status='Unread')
    notif_count = notifications.count()
    context = {
        'notifications': notifications,
        'notif_count': notif_count,
    }
    return render(request, "user_app/settings/notification_page.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def view_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    authors = Authors.objects.filter(article=notification.article).order_by('author_order')
    return render(request, 'user_app/crud/view_notification.html', {"notification": notification, 'authors': authors})
