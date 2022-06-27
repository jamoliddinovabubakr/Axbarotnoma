from multiprocessing import context
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from user_app.decorators import allowed_users
from user_app.models import Notification, State
from article_app.models import Article, Authors
from user_app.forms import CreateNotificationForm


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN', 'BOSH MUHARRIR'])
def get_notifications(request):
    notifications = Notification.objects.order_by("-created_at")
    notif_count = notifications.count()
    context = {
        'notifications': notifications,
        'notif_count': notif_count,
    }
    return render(request, "user_app/settings/notification_page.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN', 'BOSH MUHARRIR'])
def view_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification.status = 'Read'
    notification.save()
    authors = Authors.objects.filter(article=notification.article).order_by('author_order')
    return render(request, 'user_app/crud/view_notification.html', {"notification": notification, 'authors': authors})


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN', 'BOSH MUHARRIR'])
def reject_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.state_edit = State.objects.get(pk=3)
    article.save()
    return redirect('notifications')


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN', 'BOSH MUHARRIR'])
def confirm_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.state_edit = State.objects.get(pk=2)
    article.save()
    return redirect('notifications')