from ast import Constant
from multiprocessing import context
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from user_app.decorators import allowed_users
from user_app.models import Notification, State, Step
from article_app.models import Article, Authors, MyResendArticle
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
    UQILMOQDA=State.objects.get(pk=1)

    notification = get_object_or_404(Notification, pk=pk)
    article = notification.article

    if notification.status == 'Tekshirilmadi':
        my_resends = MyResendArticle.objects.filter(article=article)
        my_resend_last = my_resends.last()
        my_resend_last.state = UQILMOQDA
        article.state = UQILMOQDA
        article.save()

        article.step_bosh_muharrir = get_object_or_404(Step, pk=2)
        article.save()

        my_resend_last.save()
        notification.status = 'Tekshirilmoqda'
        notification.save()

    authors = Authors.objects.filter(article=notification.article).order_by('author_order')
    return render(request, 'user_app/crud/view_notification.html', {"notification": notification, 'authors': authors})


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN', 'BOSH MUHARRIR'])
def reject_article(request, pk):
    RAD_ETILDI=State.objects.get(pk=2)
    notif = get_object_or_404(Notification, pk=pk)

    get_msg = request.GET.get('message_author')
    print(get_msg)

    article = get_object_or_404(Article, pk=notif.article.id)
    article.state = RAD_ETILDI
    article.step_bosh_muharrir = get_object_or_404(Step, pk=3)
    article.save()

    my_resends = MyResendArticle.objects.filter(article=article)
    my_resend_last = my_resends.last()

    my_resend_last.state = RAD_ETILDI
    my_resend_last.message = get_msg
    my_resend_last.save()

    notif.status = 'Tekshirildi'
    notif.save()

    return redirect('notifications')


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN', 'BOSH MUHARRIR'])
def confirm_article(request, pk):
    TASDIQLANDI=State.objects.get(pk=3)
    notif = get_object_or_404(Notification, pk=pk)

    article = get_object_or_404(Article, pk=notif.article.id)
    article.state = TASDIQLANDI
    article.step_bosh_muharrir = get_object_or_404(Step, pk=3)
    article.save()

    my_resends = MyResendArticle.objects.filter(article=article)
    my_resend_last = my_resends.last()
    my_resend_last.state = TASDIQLANDI
    my_resend_last.save()

    notif.status = 'Tekshirildi'
    notif.save()

    return redirect('notifications')


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN', 'BOSH MUHARRIR'])
def resend_a(request, pk):
    QAYTAYUBORISH=State.objects.get(pk=5)
    notif = get_object_or_404(Notification, pk=pk)

    article = get_object_or_404(Article, pk=notif.article.id)
    article.state = QAYTAYUBORISH
    article.step_bosh_muharrir = get_object_or_404(Step, pk=3)
    article.save()

    my_resends = MyResendArticle.objects.filter(article=article)
    my_resend_last = my_resends.last()
    my_resend_last.state = QAYTAYUBORISH
    my_resend_last.save()

    notif.status = 'Tekshirildi'
    notif.save()
    
    return redirect('notifications')