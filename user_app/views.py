from article_app.models import Journal, Notification, Article, NotificationStatus, ExtraAuthor, ArticleStatus, ArticleFile
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from user_app.decorators import unauthenticated_user, password_reset_authentification
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from user_app.forms import CreateUserForm, AddReviewerForm
from user_app.models import *
import os
from user_app.models import User
from django.db.models.query_utils import Q
from user_app.forms import UpdateUserForm
from django.http import HttpResponse, JsonResponse
from user_app.models import Region
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group, Permission
from user_app.decorators import allowed_users
from user_app.models import Menu, ReviewerArticle, StatusReview
from django.utils.translation import get_language_from_request
from . import utils


def logout_user(request):
    logout(request)
    return redirect('main_page')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@unauthenticated_user
def login_page(request):
    if request.method == 'POST' and is_ajax(request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_page')
        else:
            return JsonResponse({"message": "Username or password incorrect!"})
    return render(request, "user_app/register/login.html")


@unauthenticated_user
def register_page(request):
    if request.method == 'POST' and is_ajax(request):
        form = CreateUserForm(request.POST)
        lname = request.POST.get('last_name')
        fname = request.POST.get('first_name')
        mname = request.POST.get('middle_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if form.is_valid() and len(lname) != 0 and len(fname) != 0 and len(mname) != 0:
            res_username = utils.validate_username(username)
            if not res_username['success']:
                return JsonResponse({"message": res_username['reason']})
            
            res_email = utils.validate_email(email)
            if not res_email['success']:
                return JsonResponse({"message": res_email['reason']})
            
            user = form.save(commit=False)
            user.save()

            user_group, created = Group.objects.get_or_create(name='Author')
            if not user.groups.filter(name__in=['Author']).exists():
                user_group.user_set.add(user)

            roles = Role.objects.filter(pk=4)
            if roles.count() > 0:
                user.roles.add(roles.first())

            user = authenticate(request, username=user.username,
                                password=request.POST['password1'])

            if user is not None:
                login(request, user)
                return redirect('main_page')
            else:
                return JsonResponse({"message": "Username or password incorrect!"})
        else:
            if len(lname) == 0:
                return JsonResponse({"message": " Please enter your Surname"})
            if len(fname) == 0:
                return JsonResponse({"message": " Please enter your Name"})
            if len(mname) == 0:
                return JsonResponse({"message": " Please enter your Middle name"})
            if len(username) == 0:
                return JsonResponse({"message": " Please enter your Username"})
            if len(email) == 0:
                return JsonResponse({"message": " Please enter your Email"})
            res_username = utils.validate_username(username)
            if not res_username['success']:
                return JsonResponse({"message": res_username['reason']})
            
            res_email = utils.validate_email(email)
            if not res_email['success']:
                return JsonResponse({"message": res_email['reason']})

    form = CreateUserForm()
    context = {
        'form': form,
    }
    return render(request, "user_app/register/register.html", context)


def choose_roles(request):
    if request.method == "POST":
        form = AddReviewerForm(request.POST, request.FILES)
        if form.is_valid():
            reviewer = form.save(commit=False)
            # if request.FILES:
            #     for f in request.FILES.getlist('mfile'):

            return redirect('main_page')
    context = {
        'user': User.objects.get(pk=request.user.id),
        'form': AddReviewerForm()
    }
    return render(request, "user_app/crud/choose_role.html", context=context)


# @login_required(login_url='login')
# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             messages.success(request, 'Parolingiz muvaffaqiyatli o\'zgartirildi!')
#             r = 1
#             return render(request, 'user_app/register/change_password.html', {'result': r})
#         else:
#             r = -1
#             messages.error(request, 'Please correct the error below.')
#     else:
#         r = 2
#         form = PasswordChangeForm(request.user)
#     return render(request, 'user_app/register/change_password.html', {
#         'form': form,
#         'result': r,
#     })
#
#
# @password_reset_authentification
# def password_reset(request):
#     if request.method == "POST":
#         password_reset_form = PasswordResetForm(request.POST)
#         if password_reset_form.is_valid():
#             data = password_reset_form.cleaned_data['email']
#             associated_users = User.objects.filter(Q(email=data))
#             if associated_users.exists():
#                 for user in associated_users:
#                     subject = "Password Reset Requested"
#                     email_template_name = "user_app/register/password_reset_email.txt"
#                     c = {
#                         "email": user.email,
#                         # 'domain': '127.0.0.1:443',
#                         # 'site_name': '127.0.0.1:443',
#                         "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                         "user": user,
#                         'token': default_token_generator.make_token(user),
#                         # 'protocol': 'http',
#                     }
#                     email = render_to_string(email_template_name, c)
#                     try:
#                         send_mail(subject, email, 'admin123@gmail.com', [user.email], fail_silently=False)
#                     except BadHeaderError:
#                         return HttpResponse('Invalid header found.')
#                     return redirect("password_reset_done")
#     password_reset_form = PasswordResetForm()
#     return render(request=request, template_name="user_app/register/password_reset.html",
#                   context={"password_reset_form": password_reset_form})
#
#


@login_required(login_url='login')
# @allowed_users(menu_url='profile_page')
def dashboard(request):
    user = request.user
    myqueues = Article.objects.filter(author=user).filter(Q(article_status_id=1) | Q(article_status_id=4) | Q(article_status_id=5) | Q(article_status_id=6) | Q(article_status_id=7) | Q(article_status_id=8)).order_by(
        '-updated_at')
    myarchives = Article.objects.filter(author=user).filter(Q(article_status_id=2) | Q(article_status_id=3)).order_by(
        '-updated_at')

    context = {
        'myqueues': myqueues,
        'myarchives': myarchives,
    }
    return render(request, "user_app/user_dashboard.html", context=context)


@login_required(login_url='login')
# @allowed_users(menu_url='profile_page')
def editor_dashboard(request):
    user = User.objects.get(id=request.user.id)
    role_e = Role.objects.get(id=2)

    if role_e.id not in user.get_roles:
        return render(request, 'user_app/not_access.html')
    return render(request, "user_app/editor_dashboard.html")



@login_required(login_url='login')
# @allowed_users(menu_url='profile_page')
def reviewer_dashboard(request):
    user = User.objects.get(id=request.user.id)
    role_r = Role.objects.get(id=3)

    if role_r.id not in user.get_roles:
        return render(request, 'user_app/not_access.html')
    return render(request, "user_app/reviewer_dashboard.html")



@login_required(login_url='login')
# @allowed_users(menu_url='profile_page')
def editor_notifications(request):
    user = User.objects.get(id=request.user.id)

    uncheck_notifications = Notification.objects.filter(to_user=user).filter(is_update_article=True).filter(
        Q(notification_status_id=1) | Q(notification_status_id=2)).order_by('-created_at')

    check_notifications = Notification.objects.filter(to_user=user).filter(is_update_article=True).filter(
        notification_status_id=3).order_by('-created_at')

    data = {
        "uncheck_notifications": list(uncheck_notifications.values(
            'id', 'created_at', 'article__id', 'article__title', 'notification_status__id', 'notification_status__name',
            'article__author__email', 'is_update_article'
        )),
        "check_notifications": list(check_notifications.values(
            'id', 'created_at', 'article__id', 'article__title', 'notification_status__id', 'notification_status__name',
            'article__author__email', 'is_update_article'
        ))
    }

    return JsonResponse(data)



@login_required(login_url='login')
# @allowed_users(menu_url='profile_page')
def reviewer_notifications(request):
    user = User.objects.get(id=request.user.id)

    uncheck_notifications = Notification.objects.filter(to_user=user).filter(is_update_article=True).filter(
        Q(notification_status_id=1) | Q(notification_status_id=2)).order_by('-created_at')

    check_notifications = Notification.objects.filter(to_user=user).filter(is_update_article=True).filter(
        notification_status_id=3).order_by('-created_at')

    data = {
        "uncheck_notifications": list(uncheck_notifications.values(
            'id', 'created_at', 'article__id', 'article__title', 'notification_status__id', 'notification_status__name', 'is_update_article', 'from_user__email', 'message'
        )),
        "check_notifications": list(check_notifications.values(
            'id', 'created_at', 'article__id', 'article__title', 'notification_status__id', 'notification_status__name', 'is_update_article', 'from_user__email', 'message'
        ))
    }

    return JsonResponse(data)


@login_required(login_url='login')
# @allowed_users(menu_url='notifications')
def author_vs_editor_vs_reviewer(request, pk):
    article = Article.objects.get(pk=pk)
    user = get_object_or_404(User, pk=request.user.id)
    current_user_id = user.id
    author_id = article.author.id

    if request.method == "GET" and is_ajax(request):
        current_user_from = Notification.objects.filter(
            article_id=pk).filter(from_user_id=current_user_id)


        current_user_to = Notification.objects.filter(
            article_id=pk).filter(to_user_id=current_user_id)

        notifications = current_user_from.union(
            current_user_to).order_by('created_at')

        messages = Notification.objects.filter(
            article=article).filter(is_update_article=False)

        for item in messages:
            item.notification_status = NotificationStatus.objects.get(pk=3)
            item.save()

        data = {
            "article_title": article.title,
            "current_user_id": current_user_id,
            "author_id": author_id,
            "is_visible_comment": True,
            "notifications": list(
                notifications.values(
                    'id', 'article__id', 'from_user__username', 'from_user__email', 'from_user__id', 'message',
                    'to_user__username', 'to_user__email', 'to_user__id', 'created_at',
                )
            ),
        }
        return JsonResponse(data)


@login_required(login_url='login')
def load_notification(request):
    if request.method == 'GET':
        user = User.objects.get(pk=request.user.id)

        uncheck_notifications = Notification.objects.all().order_by("-created_at").filter(to_user=user).filter(
            Q(notification_status_id=1) | Q(notification_status_id=2))
        check_notifications = Notification.objects.all().order_by("-created_at").filter(to_user=user).filter(
            Q(notification_status_id=3))

        data = {
            "uncheck_notifications": list(uncheck_notifications.values(
                'id', 'from_user__avatar', 'from_user__first_name', 'from_user__last_name',
                'created_at'
            )),
            "check_notifications": list(check_notifications.values(
                'id', 'from_user__avatar', 'from_user__first_name', 'from_user__last_name',
                'created_at'
            ))
        }

        return JsonResponse(data)
    else:
        return JsonResponse("Error")


@login_required(login_url='login')
def count_notification(request):
    if request.method == 'GET':
        user = User.objects.get(pk=request.user.id)

        unread_notifications = Notification.objects.all().order_by("-created_at").filter(to_user=user).filter(
            notification_status_id=1)
        count_unread_notifications = unread_notifications.count()
        notifications = unread_notifications[:5]

        return JsonResponse(
            {"count_unread_notifications": count_unread_notifications,
             "notifications": list(notifications.values(
                 'id', 'from_user__avatar', 'from_user__first_name', 'from_user__last_name',
                 'created_at'
             ))})


@login_required(login_url='login')
def editor_check_article(request, pk):
    user = get_object_or_404(User, pk=request.user.id)
    objs = Editor.objects.filter(user=user)
    if objs.count() != 1:
         return render(request, 'user_app/not_access.html')
     
    notifification = get_object_or_404(Notification, pk=pk)
    notifification.notification_status = NotificationStatus.objects.get(id=2)
    notifification.save()
    article = Article.objects.get(pk=notifification.article.id)

    file = ArticleFile.objects.filter(article=article).filter(file_status=1).last()
    article_reviews = ReviewerArticle.objects.filter(article=article).filter(editor=objs.first())
    
    is_ready_publish : bool = True
    for item in article_reviews:
        if item.status.id != 3:
            is_ready_publish = False
    
        
    context = {
        "article": article,
        "article_reviews": article_reviews,
        "article_file": file,
        "is_ready_publish": is_ready_publish,
    }
    return render(request, 'user_app/check_article_by_editor.html', context=context)



@login_required(login_url='login')
def reviewer_check_article(request, pk):
    user = get_object_or_404(User, pk=request.user.id)
    objs = Reviewer.objects.filter(user=user).filter(is_reviewer=True)
    if objs.count() != 1:
         return render(request, 'user_app/not_access.html')
     
    notifification = get_object_or_404(Notification, pk=pk)
    notifification.notification_status = NotificationStatus.objects.get(id=2)
    notifification.save()
    
    reviewer = get_object_or_404(Reviewer, user=user)
    article = Article.objects.get(pk=notifification.article.id)

    article_reviews = ReviewerArticle.objects.filter(article=article).filter(reviewer=objs.first())
    
    if article_reviews.count() == 1:
        article_review = article_reviews.first()
        if article_review.status.id == 1:
            article_review.status = StatusReview.objects.get(pk=2)
            article_review.save()
        context = {
        "article": article,
        "notifification": notifification,
        "editor": article_review.editor,
        "article_review": article_review,
        }
        return render(request, 'user_app/check_article_by_reviewer.html', context=context)
    else:
        return HttpResponse("Error")



@login_required(login_url='login')
def load_reviewers(request):
    reviewers = Reviewer.objects.filter(is_reviewer=True)

    data = {
        "reviewers": list(reviewers.values(
            'id', 'user__id', 'user__first_name', 'user__last_name', 'user__email'
        ))
    }
    return JsonResponse(data=data)


@login_required(login_url='login')
def reviewer_confirmed(request):
    if request.method == 'POST' and is_ajax(request):
        review_id = request.POST.get('review_article_id')
        comment = request.POST.get('comment')
        
        review = ReviewerArticle.objects.get(pk=int(review_id))
        review.comment = comment
        review.status = StatusReview.objects.get(pk=3)
        review.save()

        data = {
        "message":  "Success Article Cinfirmed!",
        }
        return JsonResponse(data=data)
    else:
        return HttpResponse("Not Fount Page!")
    
  
@login_required(login_url='login')
def reviewer_resubmit(request):
    if request.method == 'POST' and is_ajax(request):
        review_id = request.POST.get('review_article_id')
        comment = request.POST.get('comment')
        
        review = ReviewerArticle.objects.get(pk=int(review_id))
        review.comment = comment
        review.status = StatusReview.objects.get(pk=5)
        review.save()
        
        article = get_object_or_404(Article, pk=review.article.id)
        article.article_status = get_object_or_404(ArticleStatus, pk=8)
        article.save()
        
        Notification.objects.create(
            article=article,
            from_user=review.reviewer.user,
            to_user=review.editor.user,
            message=comment,
            notification_status=NotificationStatus.objects.get(id=1),
        )
        

        data = {
            "message":  "Resubmit Article!",
            }
        return JsonResponse(data=data)
    else:
        return HttpResponse("Not Fount Page!")
    
    
@login_required(login_url='login')
def reviewer_rejected(request):
    if request.method == 'POST' and is_ajax(request):
        review_id = request.POST.get('review_article_id')
        comment = request.POST.get('comment')
        
        review = ReviewerArticle.objects.get(pk=int(review_id))
        review.comment = comment
        review.status = StatusReview.objects.get(pk=4)
        review.save()
        
        article = get_object_or_404(Article, pk=review.article.id)
        
        Notification.objects.create(
            article=article,
            from_user=review.reviewer.user,
            to_user=review.editor.user,
            message=comment,
            notification_status=NotificationStatus.objects.get(id=1),
        )
        

        data = {
            "message":  "Success Article Cinfirmed!",
            }
        return JsonResponse(data=data)
    else:
        return HttpResponse("Not Fount Page!")
    


@login_required(login_url='login')
def sending_reviewer(request):   #Tanlangan taqrizchilarga maqolani yuborish
    user = get_object_or_404(User, pk=request.user.id)
    if request.method == 'POST':
        selected = request.POST.getlist('reviewers[]')
        token = request.POST['csrfmiddlewaretoken']
        article_id = request.POST['article_id']

        if len(selected) > 0 and token and article_id:
            article = Article.objects.get(pk=int(article_id))
            editor = get_object_or_404(Editor, user=user)
            for item in selected:
                reviewer = get_object_or_404(Reviewer, pk=int(item))
                reviewer_user = get_object_or_404(User, pk=reviewer.user.id)
                
                Notification.objects.create(
                    article=article,
                    from_user=user,
                    to_user=reviewer_user,
                    message=f"({reviewer_user.email}).Hurmatli taqrizchi sizga maqola yuborildi.",
                    notification_status=NotificationStatus.objects.get(id=1),
                    is_update_article=True,
                )

                ReviewerArticle.objects.create(
                    article=article,
                    editor=editor,
                    reviewer=reviewer,
                    status=StatusReview.objects.get(pk=1),
                    comment="",
                )

            article.article_status = get_object_or_404(ArticleStatus, pk=4)
            article.save()
            data = {
                "is_valid": True,
                "message": "Taqrizchilarga muvaffaqiyatli yuborildi!",
            }
            return JsonResponse(data=data)
        else:
            data = {
                "is_valid": False,
                "message": "Taqrizchilarni to'liq tanlang!",
            }
            return JsonResponse(data=data)


# @login_required(login_url='login')
# def profile(request):
#     context = {
#
#     }
#     return render(request, "user_app/profile_page.html", context=context)
#
#
# @login_required(login_url='login')
# def handler404(request, exception):
#     return render(request, 'user_app/error_404.html')
#
#
# @login_required(login_url='login')
# @allowed_users(menu_url='roles')
# def get_roles(request):
#     roles = Role.objects.filter(status=True)
#     context = {
#         'roles': roles
#     }
#     return render(request, "user_app/settings/roles_page.html", context=context)
#
#
# @login_required(login_url='login')
# @allowed_users(perm='add_role')
# def create_role(request):
#     if request.method == "POST":
#         form = CreateRoleForm(request.POST)
#         if form.is_valid():
#             role = form.save(commit=False)
#             role.save()
#             return redirect('roles')
#     else:
#         context = {
#             'form': CreateRoleForm(),
#         }
#         return render(request, 'user_app/crud/add_role.html', context)
#
#
# @login_required(login_url='login')
# @allowed_users(perm='change_role')
# def edit_role(request, pk):
#     role = get_object_or_404(Role, pk=pk)
#     if request.method == 'POST':
#         form = CreateRoleForm(request.POST, instance=role)
#         form.save()
#         return redirect('roles')
#
#     else:
#         form = CreateRoleForm(instance=role)
#         return render(request, 'user_app/crud/edit_role.html', {"role": role, 'form': form})
#
#
# @login_required(login_url='login')
# @allowed_users(perm='delete_role')
# def delete_role(request, pk):
#     role = get_object_or_404(Role, pk=pk)
#     if request.method == "POST":
#         role.delete()
#         return redirect('roles')
#     else:
#         return render(request, 'user_app/crud/delete_role.html', {'role': role})
#
#
# @login_required(login_url='login')
# @allowed_users(menu_url='states')
# def get_states(request):
#     states = State.objects.filter(status=True)
#     context = {
#         'states': states
#     }
#     return render(request, "user_app/settings/states_page.html", context=context)
#
#
# @login_required(login_url='login')
# @allowed_users(perm='add_state')
# def create_state(request):
#     if request.method == "POST":
#         form = CreateStateForm(request.POST)
#         if form.is_valid():
#             state = form.save(commit=False)
#             state.save()
#             return redirect('states')
#     else:
#         context = {
#             'form': CreateStateForm(),
#         }
#         return render(request, 'user_app/crud/add_state.html', context)
#
#
# @login_required(login_url='login')
# @allowed_users(perm='change_state')
# def edit_state(request, pk):
#     state = get_object_or_404(State, pk=pk)
#     if request.method == 'POST':
#         form = CreateStateForm(request.POST, instance=state)
#         form.save()
#         return redirect('states')
#
#     else:
#         form = CreateStateForm(instance=state)
#         return render(request, 'user_app/crud/edit_state.html', {"state": state, 'form': form})
#
#
# @login_required(login_url='login')
# @allowed_users(perm='delete_state')
# def delete_state(request, pk):
#     state = get_object_or_404(State, pk=pk)
#     if request.method == "POST":
#         state.delete()
#         return redirect('states')
#     else:
#         return render(request, 'user_app/crud/delete_state.html', {'state': state})
#
#
# @login_required(login_url='login')
# @allowed_users(menu_url='admins')
# def admins(request):
#     adminlar = User.objects.filter(Q(role__name="MASTER") | Q(role__name="ADMIN"))
#     context = {
#         'admins': adminlar
#     }
#     return render(request, "user_app/admins_page.html", context=context)
#
#
# @login_required(login_url='login')
# @allowed_users(menu_url='users')
# def users(request):
#     userlar = User.objects.all()
#     context = {
#         'users': userlar
#     }
#     return render(request, "user_app/users_page.html", context=context)
#
#
# @login_required(login_url='login')
# @allowed_users(perm='view_user')
# def view_user(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     return render(request, 'user_app/crud/view_user.html', {'user': user})
#
#
@login_required(login_url='login')
def edit_profile(request):
    user = request.user
    if request.method == 'POST' and is_ajax(request):
        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        print(form)
        if not form.has_changed():
            return JsonResponse({'status':False, "message": "Form hasn't change"})
        if form.is_valid():
            form.save()
            return JsonResponse({'status':True, "message": "Your changes saved successfully."})
        else:
            return JsonResponse({'status':False, "message": "Form invalid"})
    else:
        form = UpdateUserForm(instance=user)
        return render(request, 'user_app/register/edit_profile.html', {"user": user, 'form': form})


def change_group(user, new_gr):
    if user.groups.exists():
        user.groups.clear()
    new_group = Group.objects.get(name=new_gr)
    new_group.user_set.add(user)
#
#
# @login_required(login_url='login')
# @allowed_users(perm='change_user')
# def update_user(request, pk):
#     MASTER = 'MASTER'
#     ADMIN = 'ADMIN'
#     USER = 'USER'
#     BOSH_MUHARRIR = 'BOSH MUHARRIR'
#     TAHRIRCHI = 'TAHRIRCHI'
#     user = get_object_or_404(User, pk=pk)
#     if request.method == 'POST':
#         form = UpdateUserForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#
#             if user.role.name == MASTER:
#                 if not user.groups.exists():
#                     new_group, created = Group.objects.get_or_create(name=MASTER)
#                     new_group.user_set.add(user)
#
#             if user.role.name == ADMIN:
#                 change_group(user, ADMIN)
#
#             if user.role.name == USER:
#                 change_group(user, USER)
#
#             if user.role.name == TAHRIRCHI:
#                 change_group(user, TAHRIRCHI)
#
#             if user.role.name == BOSH_MUHARRIR:
#                 change_group(user, BOSH_MUHARRIR)
#
#             if request.FILES.get('avatar', None) is not None:
#                 try:
#                     os.remove(user.avatar.url)
#                 except Exception as e:
#                     print('Exception in removing old profile image: ', e)
#                 user.avatar = request.FILES['avatar']
#                 user.save()
#             return redirect('users')
#         else:
#             return HttpResponse("Forma valid emas!")
#
#     else:
#         form = UpdateUserForm(instance=user)
#         return render(request, 'user_app/crud/edit_user.html', {"user": user, 'form': form})
#
#
# @login_required(login_url='login')
# @allowed_users(perm='delete_user')
# def delete_user(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     if request.method == "POST":
#         user.delete()
#         return redirect('users')
#     else:
#         return render(request, 'user_app/crud/delete_user.html', {'user': user})
#
#
# @login_required(login_url='login')
# @allowed_users(menu_url='regions')
# def get_regions(request):
#     regions = Region.objects.all()
#     context = {
#         'regions': regions
#     }
#     return render(request, "user_app/settings/region_page.html", context=context)
#
#
# @login_required(login_url='login')
# @allowed_users(perm='add_region')
# def create_region(request):
#     if request.method == "POST":
#         form = CreateRegionForm(request.POST)
#         if form.is_valid():
#             region = form.save(commit=False)
#             region.save()
#             return redirect('regions')
#     else:
#         context = {
#             'form': CreateRegionForm(),
#         }
#         return render(request, 'user_app/crud/add_region.html', context)
#
#
# @login_required(login_url='login')
# @allowed_users(perm='change_region')
# def edit_region(request, pk):
#     region = get_object_or_404(Region, pk=pk)
#     if request.method == 'POST':
#         form = CreateRegionForm(request.POST, instance=region)
#         form.save()
#         return redirect('regions')
#
#     else:
#         form = CreateRegionForm(instance=region)
#         return render(request, 'user_app/crud/edit_region.html', {"region": region, 'form': form})
#
#
# @login_required(login_url='login')
# @allowed_users(perm='delete_region')
# def delete_region(request, pk):
#     region = get_object_or_404(Region, pk=pk)
#     if request.method == "POST":
#         region.delete()
#         return redirect('regions')
#     else:
#         return render(request, 'user_app/crud/delete_region.html', {'region': region})


# Glavniy redaktor
