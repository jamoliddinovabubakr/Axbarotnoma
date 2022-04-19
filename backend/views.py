from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from .decorators import unauthenticated_user, allowed_users, admin_only

from .forms import CreateUserForm
from .models import Menu


def main_page(request):
    menus = Menu.objects.filter(status=True).filter(parent_id=0)
    context = {
        'menus': menus,
    }
    return render(request, "backend/content_frontend/main.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admins', 'Users'])
# @admin_only
def cabinet_page(request):
    menus = Menu.objects.filter(status=True).filter(parent_id=0)
    context = {
        'menus': menus,
    }
    return render(request, "backend/content_backend/cabinet_page.html", context=context)


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

    return render(request, "backend/register/login.html")


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
            return render(request, "backend/register/register.html", context)

    else:
        form = CreateUserForm()
        context = {
            'form': form,
        }
        return render(request, "backend/register/register.html", context)


def logout_user(request):
    logout(request)
    return redirect('main_page')


@login_required(login_url='login')
def handler404(request, exception):
    return render(request, 'backend/content_backend/error_404.html')
