import os

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from user_app.decorators import unauthenticated_user, allowed_users, admin_only

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

from user_app.forms import CreateUserForm, UpdateUserForm


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admins', 'Masters'])
def admins(request):
    admins = User.objects.filter(Q(role__name="MASTER") | Q(role__name="ADMIN"))
    context = {
        'admins': admins
    }
    return render(request, "user_app/admins_page.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admins', 'Masters'])
def users(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, "user_app/users_page.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admins', 'Masters'])
def view_user(request, pk):
    # user = request.user
    # if is_user(user):
    #     error = "Error"
    #     return render(request, 'report/not_access.html', {'error': error})
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admins', 'Masters'])
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        person = form.save(commit=False)
        person.save()

        if user.role.name == 'MASTER':
            if not user.groups.exists():
                new_group, created = Group.objects.get_or_create(name='Masters')
                new_group.user_set.add(user)

        if user.role.name == 'ADMIN':
            change_group(user, 'Admins')

        if user.role.name == 'USER':
            change_group(user, 'Users')

        if request.FILES.get('avatar', None) is not None:
            try:
                os.remove(user.avatar.url)
            except Exception as e:
                print('Exception in removing old profile image: ', e)
            user.avatar = request.FILES['avatar']
            user.save()
        return redirect('users')

    else:
        form = UpdateUserForm(instance=user)
        return render(request, 'user_app/crud/edit_user.html', {"user": user, 'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admins', 'Masters'])
def delete_user(request, pk):
    user = request.user
    # if is_user(user):
    #     error = "Error"
    #     return render(request, 'report/not_access.html', {'error': error})
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        return redirect('users')
    else:
        return render(request, 'user_app/crud/delete_user.html', {'user': user})
