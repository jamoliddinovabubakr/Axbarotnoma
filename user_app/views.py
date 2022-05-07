import os

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from .decorators import unauthenticated_user, allowed_users, admin_only

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from user_app.models import User, Menu, Role, District, Region, Gender
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from .forms import CreateUserForm, UpdateUserForm


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admins', 'Users'])
# @admin_only
def profile_page(request):
    context = {

    }
    return render(request, "user_app/cabinet_page.html", context=context)


@login_required(login_url='login')
def profile(request):
    context = {

    }
    return render(request, "user_app/profile_page.html", context=context)


@login_required(login_url='login')
def admins(request):
    admins = User.objects.filter(Q(role__name="MASTER") | Q(role__name="ADMIN"))
    context = {
        'admins': admins
    }
    return render(request, "user_app/admins_page.html", context=context)


@login_required(login_url='login')
def users(request):
    users = User.objects.filter(role__name='USER')
    context = {
        'users': users
    }
    return render(request, "user_app/users_page.html", context=context)



@login_required(login_url='login')
def menus(request):
    menus = Menu.objects.filter(status=True)
    context = {
        'menus': menus
    }
    return render(request, "user_app/settings/menus_page.html", context=context)


@login_required(login_url='login')
def roles(request):
    roles = Role.objects.filter(status=True)
    context = {
        'roles': roles
    }
    return render(request, "user_app/settings/roles_page.html", context=context)


@login_required(login_url='login')
def menus(request):
    menus = Menu.objects.filter(status=True)
    context = {
        'menus': menus
    }
    return render(request, "user_app/settings/menus_page.html", context=context)


@login_required(login_url='login')
def genders(request):
    genders = Gender.objects.filter(status=True)
    context = {
        'genders': genders
    }
    return render(request, "user_app/settings/gender_page.html", context=context)


@login_required(login_url='login')
def districts(request):
    districts = District.objects.all()
    context = {
        'districts': districts
    }
    return render(request, "user_app/settings/district_page.html", context=context)


@login_required(login_url='login')
def regions(request):
    regions = Region.objects.all()
    context = {
        'regions': regions
    }
    return render(request, "user_app/settings/region_page.html", context=context)


@unauthenticated_user
def login_page(request):
    errors = ''
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
    # if is_user(user):
    #     error = "Error"
    #     return render(request, 'report/not_access.html', {'error': error})
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            user_group, created = Group.objects.get_or_create(name='Users')
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
def handler404(request, exception):
    return render(request, 'user_app/error_404.html')


def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        form.save()
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
        r = 0
        form = UpdateUserForm(instance=user)
        return render(request, 'user_app/register/edit_profile.html', {"user": user, 'form': form, 'result': r})
