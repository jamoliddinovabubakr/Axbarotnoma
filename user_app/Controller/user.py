import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from user_app.decorators import allowed_users
from user_app.models import User
from django.db.models.query_utils import Q
from user_app.forms import UpdateUserForm


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admins', 'Masters'])
def admins(request):
    adminlar = User.objects.filter(Q(role__name="MASTER") | Q(role__name="ADMIN"))
    context = {
        'admins': adminlar
    }
    return render(request, "user_app/admins_page.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admins', 'Masters'])
def users(request):
    userlar = User.objects.all()
    context = {
        'users': userlar
    }
    return render(request, "user_app/users_page.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admins', 'Masters'])
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
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        return redirect('users')
    else:
        return render(request, 'user_app/crud/delete_user.html', {'user': user})
