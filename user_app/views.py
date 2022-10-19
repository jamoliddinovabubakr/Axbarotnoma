from article_app.models import Journal
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from user_app.decorators import unauthenticated_user, password_reset_authentification, allowed_users
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from user_app.forms import CreateUserForm
from user_app.models import Notification, State, Step
from article_app.models import Article, Authors, MyResendArticle
from user_app.models import Role
from user_app.forms import CreateRoleForm
from user_app.models import State
from user_app.forms import CreateStateForm
import os
from django.contrib.auth.models import Group
from user_app.models import User
from django.db.models.query_utils import Q
from user_app.forms import UpdateUserForm
from django.http import HttpResponse
from user_app.models import Region
from user_app.forms import CreateRegionForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from user_app.decorators import allowed_users
from user_app.models import Menu
from user_app.forms import CreateMenuForm


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile_page')
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

            user_group, created = Group.objects.get_or_create(name='USER')
            user_group.user_set.add(user)

            user = authenticate(request, username=user.username, password=request.POST['password1'])

            if user is not None:
                login(request, user)
                return redirect('main_page')
            else:
                messages.info(request, 'login yoki parol xato')
                return redirect('login')
        else:
            context = {
                'message_error': 'Xatolik!'
            }
            return render(request, "user_app/register/register.html", context)

    else:
        form = CreateUserForm()
        context = {
            'form': form,
        }
        return render(request, "user_app/register/register.html", context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Parolingiz muvaffaqiyatli o\'zgartirildi!')
            r = 1
            return render(request, 'user_app/register/change_password.html', {'result': r})
        else:
            r = -1
            messages.error(request, 'Please correct the error below.')
    else:
        r = 2
        form = PasswordChangeForm(request.user)
    return render(request, 'user_app/register/change_password.html', {
        'form': form,
        'result': r,
    })


@password_reset_authentification
def password_reset(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "user_app/register/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': '127.0.0.1:8000',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin123@gmail.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="user_app/register/password_reset.html",
                  context={"password_reset_form": password_reset_form})


def logout_user(request):
    logout(request)
    return redirect('main_page')



@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN', 'USER', 'BOSH MUHARRIR', 'MASUL KOTIB', 'TAHLILCHI'])
# @admin_only
def profile_page(request):
    tasdiqlanganlar = Article.objects.filter(state=3)
    tasdiqlanmaganlar = Article.objects.filter(state=2)
    kutish_jarayonida = Article.objects.filter(state=1)
    jurnallar = Journal.objects.all()
    context = {
        'tasdiqlanganlar': tasdiqlanganlar.count,
        'tasdiqlanmaganlar': tasdiqlanmaganlar.count,
        'kutish_jarayonida': kutish_jarayonida.count,
        'jurnallar': jurnallar.count,
    }
    return render(request, "user_app/cabinet_page.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN', 'USER', 'BOSH MUHARRIR', 'MASUL KOTIB', 'TAHLILCHI'])
def profile(request):
    context = {

    }
    return render(request, "user_app/profile_page.html", context=context)


@login_required(login_url='login')
def handler404(request, exception):
    return render(request, 'user_app/error_404.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def get_roles(request):
    roles = Role.objects.filter(status=True)
    context = {
        'roles': roles
    }
    return render(request, "user_app/settings/roles_page.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def create_role(request):
    if request.method == "POST":
        form = CreateRoleForm(request.POST)
        if form.is_valid():
            role = form.save(commit=False)
            role.save()
            return redirect('roles')
    else:
        context = {
            'form': CreateRoleForm(),
        }
        return render(request, 'user_app/crud/add_role.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def edit_role(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        form = CreateRoleForm(request.POST, instance=role)
        form.save()
        return redirect('roles')

    else:
        form = CreateRoleForm(instance=role)
        return render(request, 'user_app/crud/edit_role.html', {"role": role, 'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def delete_role(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == "POST":
        role.delete()
        return redirect('roles')
    else:
        return render(request, 'user_app/crud/delete_role.html', {'role': role})


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def get_states(request):
    states = State.objects.filter(status=True)
    context = {
        'states': states
    }
    return render(request, "user_app/settings/states_page.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def create_state(request):
    if request.method == "POST":
        form = CreateStateForm(request.POST)
        if form.is_valid():
            state = form.save(commit=False)
            state.save()
            return redirect('states')
    else:
        context = {
            'form': CreateStateForm(),
        }
        return render(request, 'user_app/crud/add_state.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def edit_state(request, pk):
    state = get_object_or_404(State, pk=pk)
    if request.method == 'POST':
        form = CreateStateForm(request.POST, instance=state)
        form.save()
        return redirect('states')

    else:
        form = CreateStateForm(instance=state)
        return render(request, 'user_app/crud/edit_state.html', {"state": state, 'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def delete_state(request, pk):
    state = get_object_or_404(State, pk=pk)
    if request.method == "POST":
        state.delete()
        return redirect('states')
    else:
        return render(request, 'user_app/crud/delete_state.html', {'state': state})


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def admins(request):
    adminlar = User.objects.filter(Q(role__name="MASTER") | Q(role__name="ADMIN"))
    context = {
        'admins': adminlar
    }
    return render(request, "user_app/admins_page.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def users(request):
    userlar = User.objects.all()
    context = {
        'users': userlar
    }
    return render(request, "user_app/users_page.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def view_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'user_app/crud/view_user.html', {'user': user})


@login_required(login_url='login')
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            ob = form.save(commit=False)
            ob.save()
            if request.FILES.get('avatar', None) is not None:
                try:
                    os.remove(user.avatar.url)
                except Exception as e:
                    print('Exception in removing old profile image: ', e)
                user.avatar = request.FILES['avatar']
                user.save()
            r = 1
            return render(request, 'user_app/register/edit_profile.html', {"user": user, 'form': form, 'result': r})
        else:
            return redirect('profile')

    else:
        r = 0
        form = UpdateUserForm(instance=user)
        return render(request, 'user_app/register/edit_profile.html', {"user": user, 'form': form, 'result': r})


def change_group(user, new_gr):
    if user.groups.exists():
        user.groups.clear()
    new_group = Group.objects.get(name=new_gr)
    new_group.user_set.add(user)


MASTER = 'MASTER'
ADMIN = 'ADMIN'
USER = 'USER'
BOSH_MUHARRIR = 'BOSH MUHARRIR'
TAHRIRCHI = 'TAHRIRCHI'


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

            if user.role.name == MASTER:
                if not user.groups.exists():
                    new_group, created = Group.objects.get_or_create(name=MASTER)
                    new_group.user_set.add(user)

            if user.role.name == ADMIN:
                change_group(user, ADMIN)

            if user.role.name == USER:
                change_group(user, USER)

            if user.role.name == TAHRIRCHI:
                change_group(user, TAHRIRCHI)

            if user.role.name == BOSH_MUHARRIR:
                change_group(user, BOSH_MUHARRIR)


            if request.FILES.get('avatar', None) is not None:
                try:
                    os.remove(user.avatar.url)
                except Exception as e:
                    print('Exception in removing old profile image: ', e)
                user.avatar = request.FILES['avatar']
                user.save()
            return redirect('users')
        else:
            return HttpResponse("Forma valid emas!")

    else:
        form = UpdateUserForm(instance=user)
        return render(request, 'user_app/crud/edit_user.html', {"user": user, 'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        return redirect('users')
    else:
        return render(request, 'user_app/crud/delete_user.html', {'user': user})


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def get_regions(request):
    regions = Region.objects.all()
    context = {
        'regions': regions
    }
    return render(request, "user_app/settings/region_page.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def create_region(request):
    if request.method == "POST":
        form = CreateRegionForm(request.POST)
        if form.is_valid():
            region = form.save(commit=False)
            region.save()
            return redirect('regions')
    else:
        context = {
            'form': CreateRegionForm(),
        }
        return render(request, 'user_app/crud/add_region.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def edit_region(request, pk):
    region = get_object_or_404(Region, pk=pk)
    if request.method == 'POST':
        form = CreateRegionForm(request.POST, instance=region)
        form.save()
        return redirect('regions')

    else:
        form = CreateRegionForm(instance=region)
        return render(request, 'user_app/crud/edit_region.html', {"region": region, 'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def delete_region(request, pk):
    region = get_object_or_404(Region, pk=pk)
    if request.method == "POST":
        region.delete()
        return redirect('regions')
    else:
        return render(request, 'user_app/crud/delete_region.html', {'region': region})


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
    UQILMOQDA = State.objects.get(pk=1)

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
def answer_to_author(request, pk):
    notif = get_object_or_404(Notification, pk=pk)
    article = get_object_or_404(Article, pk=notif.article.id)

    if notif and request.method == 'GET':
        QAYTAYUBORISH = State.objects.get(pk=5)
        RAD_ETILDI = State.objects.get(pk=2)
        TASDIQLANDI = State.objects.get(pk=3)

        msg = request.GET.get('message_author')
        result = request.GET.get('stateArticle')

        my_resends = MyResendArticle.objects.filter(article=article)
        my_resend_last = my_resends.last()

        if result == '1':
            article.state = RAD_ETILDI
            article.save()

            my_resend_last.state = RAD_ETILDI
            my_resend_last.message = msg
            my_resend_last.save()

            notif.status = 'Tekshirildi'
            notif.save()

        elif result == '2':
            article.state = QAYTAYUBORISH
            article.save()

            my_resend_last.state = QAYTAYUBORISH
            my_resend_last.message = msg
            my_resend_last.save()

            notif.status = 'Tekshirildi'
            notif.save()

        elif result == '3':
            article.state = TASDIQLANDI
            article.save()

            my_resend_last.state = TASDIQLANDI
            my_resend_last.message = msg
            my_resend_last.save()

            notif.status = 'Tekshirildi'
            notif.save()

    return redirect('notifications')


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def get_menus(request):
    menus = Menu.objects.filter(status=True)
    context = {
        'menus': menus
    }
    return render(request, "user_app/settings/menus_page.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == 'POST':
        form = CreateMenuForm(request.POST, instance=menu)
        form.save()
        return redirect('menus')

    else:
        form = CreateMenuForm(instance=menu)
        return render(request, 'user_app/crud/edit_menu.html', {"menu": menu, 'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def delete_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        menu.delete()
        return redirect('menus')
    else:
        return render(request, 'user_app/crud/delete_menu.html', {'menu': menu})

