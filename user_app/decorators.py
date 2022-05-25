from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import redirect, render


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main_page')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def password_reset_authentification(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return redirect('password_reset')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'user_app/not_access.html')

        return wrapper_func

    return decorator


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'USER':
            return redirect('main_page')

        if group == 'ADMIN':
            return view_func(request, *args, **kwargs)

    return wrapper_func
