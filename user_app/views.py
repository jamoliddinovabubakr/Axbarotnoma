from article_app.models import Journal, Notification, Article
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
from user_app.models import Menu
from django.utils.translation import get_language_from_request


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_page')
        else:
            errors = messages.info(request, 'login yoki parol xato')
            return redirect('login')
    return render(request, "user_app/register/login.html")


@unauthenticated_user
def register_page(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            user_group, created = Group.objects.get_or_create(name='AUTHOR')
            if not user.groups.filter(name__in=['AUTHOR']).exists():
                user_group.user_set.add(user)
            Author.objects.create(user=user)
            rol = Role.objects.get(pk=4)
            user.role.add(rol)

            user = authenticate(request, username=user.username, password=request.POST['password1'])

            if user is not None:
                login(request, user)
                return redirect('main_page')
            else:
                messages.info(request, 'login yoki parol xato')
                return redirect('register')
        else:
            username = request.POST['username']
            email = request.POST['email']
            usr = authenticate(request, username=username, email=email, password=request.POST['password1'])
            error = "Formani to'g'ri to'ldiring!"
            if usr is not None:
                error = "Bu foydalanuvchi bor!"
            context = {
                    "error": error,
                    "form": form,
                }
            return render(request, "user_app/register/register.html", context=context)

    else:
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
def logout_user(request):
    logout(request)
    return redirect('main_page')


@login_required(login_url='login')
# @allowed_users(menu_url='profile_page')
def dashboard(request):
    user = request.user
    author = Author.objects.get(user=user)
    myqueues = Article.objects.filter(author=author).filter(Q(article_status_id=1) | Q(article_status_id=7)).order_by('-created_at')
    myarchives = Article.objects.filter(author=author).filter(Q(article_status_id=2) | Q(article_status_id=3)).order_by('-created_at')
    context = {
        'myqueues': myqueues,
        'myarchives': myarchives,
    }
    return render(request, "user_app/user_dashboard.html", context=context)


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
# @login_required(login_url='login')
# def edit_profile(request):
#     user = request.user
#     if request.method == 'POST':
#         form = UpdateUserForm(request.POST, instance=user)
#         if form.is_valid():
#             ob = form.save(commit=False)
#             ob.save()
#             if request.FILES.get('avatar', None) is not None:
#                 try:
#                     os.remove(user.avatar.url)
#                 except Exception as e:
#                     print('Exception in removing old profile image: ', e)
#                 user.avatar = request.FILES['avatar']
#                 user.save()
#             r = 1
#             return render(request, 'user_app/register/edit_profile.html', {"user": user, 'form': form, 'result': r})
#         else:
#             return redirect('profile')
#
#     else:
#         r = 0
#         form = UpdateUserForm(instance=user)
#         return render(request, 'user_app/register/edit_profile.html', {"user": user, 'form': form, 'result': r})
#
#
# def change_group(user, new_gr):
#     if user.groups.exists():
#         user.groups.clear()
#     new_group = Group.objects.get(name=new_gr)
#     new_group.user_set.add(user)
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
@login_required(login_url='login')
# @allowed_users(menu_url='notifications')
def get_notifications(request):
    return render(request, "user_app/settings/notification_page.html")


# def load_data_notif(request):
#     if request.method == 'GET':
#         notifications = Notification.objects.filter(user__role_id__in=[1, 2, 3]).order_by(
#             "-created_at")
#
#         return JsonResponse({"notifications": list(notifications.values(
#             'id', 'article_id', 'title', 'my_resend__author__email', 'description', 'status', 'created_at',
#         ))})


# def count_notif(request):
#     if request.method == 'GET':
#         user = User.objects.get(pk=request.user.id)
#         roles = []
#         for item in user.role.all():
#             roles.append(item.id)
#         if "Reviewer" in roles:
#             notifications = Notification.objects.all().order_by("-created_at").filter(user=user).filter(status="Tekshirilmadi")
#         else:
#             notifications = Notification.objects.all().order_by("-created_at").filter(roles in [1, 2]).filter(status="Tekshirilmadi")
#         return JsonResponse({"count_notif_notread": notifications.count(), "notifications": list(notifications.values(
#             'id', 'my_resend__author__avatar', 'my_resend__author__first_name', 'my_resend__author__last_name',
#             'created_at'
#         ))})


# @login_required(login_url='login')
# @allowed_users(perm='view_notification')
# def view_notification(request, pk):
#     reading = State.objects.get(pk=1)
#     notification = get_object_or_404(Notification, pk=pk)
#     article = notification.article
#
#     if notification.status == 'Tekshirilmadi':
#         my_resends = MyResendArticle.objects.filter(article=article)
#         my_resend_last = my_resends.last()
#         my_resend_last.state = reading
#         article.state = reading
#         article.save()
#
#         my_resend_last.save()
#         notification.status = 'Tekshirilmoqda'
#         notification.save()
#
#     authors = Authors.objects.filter(article=notification.article).order_by('author_order')
#     return render(request, 'user_app/crud/view_notification.html', {"notification": notification, 'authors': authors})
#
#
# # send sms to email
#
#
# # add gmail
# @login_required(login_url='login')
# @allowed_users(perm='change_notification')
# def answer_to_author(request, pk):
#     notif = get_object_or_404(Notification, pk=pk)
#     user = User.objects.get(pk=notif.article.author.id)  # user ga email
#     article = get_object_or_404(Article, pk=notif.article.id)  # article
#     if notif and request.method == 'GET':
#         re_send = State.objects.get(pk=5)  # resend переотправить
#         reject = State.objects.get(pk=2)  # rejected отказ
#         confirm = State.objects.get(pk=3)  # reading прочитенно
#
#         msg = request.GET.get('message_author')  # message from editor
#         result = request.GET.get('stateArticle')  # result state
#         my_resends = MyResendArticle.objects.filter(article=article)  # junatgandi hammasini oladi
#         my_resend_last = my_resends.last()  # bu junatilgan dan oxirini oladi
#
#         if result == '1':  # result this is button 'Rad etish'
#             article.state = reject  # article ni statusini rad etishga tenglayapmiz
#             article.save()  # bo'lgan otkazni saqlayapmiz
#
#             my_resend_last.state = reject  # oxirgi junatilgan article ni state ni rejected qiladi
#             my_resend_last.message = msg  # va uning sms ni uzing message ga tenglab quyapdi
#             my_resend_last.save()  # rejected ni save qilamiz
#
#             notif.status = 'Tekshirildi'  # editor dagi xolatni change qilyapmiz
#             notif.save()  # va edit dagi artivle ni save qilyapmiz
#
#             # sent_email_message(user.email, result)
#
#         elif result == '2':
#             article.state = re_send
#             article.save()
#
#             my_resend_last.state = re_send
#             my_resend_last.message = msg
#             my_resend_last.save()
#
#             notif.status = 'Tekshirildi'
#             notif.save()
#             # sent_email_message(user.email, result)
#
#         elif result == '3':
#             article.state = confirm
#             article.save()
#
#             my_resend_last.state = confirm
#             my_resend_last.message = msg
#             my_resend_last.save()
#
#             notif.status = 'Tekshirildi'
#             notif.save()
#             # sent_email_message(user.email, result)
#
#     return redirect('notifications')
#
#
# # END Glavniy redaktor
#
# @login_required(login_url='login')
# @allowed_users(menu_url='menus')
# def get_menus(request):
#     menus = Menu.objects.filter(status=True)
#     context = {
#         'menus': menus
#     }
#     return render(request, "user_app/settings/menus_page.html", context=context)
#
#
# @login_required(login_url='login')
# @allowed_users(perm='change_menu')
# def edit_menu(request, pk):
#     menu = get_object_or_404(Menu, pk=pk)
#     if request.method == 'POST':
#         form = CreateMenuForm(request.POST, instance=menu)
#         form.save()
#         return redirect('menus')
#
#     else:
#         form = CreateMenuForm(instance=menu)
#         return render(request, 'user_app/crud/edit_menu.html', {"menu": menu, 'form': form})
#
#
# @login_required(login_url='login')
# @allowed_users(perm='delete_menu')
# def delete_menu(request, pk):
#     menu = get_object_or_404(Menu, pk=pk)
#     if request.method == "POST":
#         menu.delete()
#         return redirect('menus')
#     else:
#         return render(request, 'user_app/crud/delete_menu.html', {'menu': menu})
#
#
# @login_required(login_url='login')
# # @allowed_users(perm='delete_menu')
# def send_to_review(request, article_id):
#     print(f"article_id={article_id}")
#     ob = MyResendArticle.objects.filter(article__id=article_id).last()
#     print(ob.id)
#     article = Article.objects.get(pk=article_id)
#     specialities = set(ob.article.get_categories())
#     users = User.objects.filter(role__id=4)
#
#     reviews = []
#
#     for user in users:
#         if specialities.intersection(set(user.get_speciality())):
#             reviews.append(user)
#
#     if len(reviews) > 0:
#         for review in reviews:
#             Notification.objects.create(
#                 title=ob.article.title,
#                 article=article,
#                 user=review,
#                 my_resend=ob,
#                 description="Yangi maqola yuborildi",
#             )
#         ob.state = get_object_or_404(State, pk=6)
#         print(ob.state.id)
#         ob.save()
#         return redirect('notifications')
#     else:
#         return HttpResponse("Kechirasiz taqrizchilar topilmadi!")
#
#
# def review_notifications(request):
#     return render(request, "user_app/reviews/notif_review.html")
#
#
# def get_review_view_notification(request):
#     notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
#     return JsonResponse({"notifications": list(notifications.values(
#         'id', 'title', 'status', 'created_at', 'result_review', 'my_resend__article', 'description'
#     ))})
#
#
# def review_view_notification(request, pk):
#     notif = get_object_or_404(Notification, pk=pk)
#
#     if notif.status == 'Tekshirilmadi':
#         notif.status = 'Tekshirilmoqda'
#         notif.save()
#
#     context = {
#         'notif': notif,
#     }
#
#     return render(request, "user_app/reviews/notification_view.html", context=context)
