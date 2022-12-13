from django.contrib.auth import logout
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404

from user_app.models import Menu


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


def allowed_users(perm=None, menu_url=None):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if perm and menu_url is None:
                user = request.user
                permissions = [p.codename for p in Permission.objects.filter(Q(user=user) | Q(group__user=user)).all()]
                if perm in permissions:
                    return view_func(request, *args, **kwargs)
                else:
                    return render(request, 'user_app/not_access.html')
            elif menu_url and perm is None:
                menu = get_object_or_404(Menu, url=menu_url)
                roles = menu.get_roles()
                user_role = request.user.role.name
                if user_role in roles:
                    return view_func(request, *args, **kwargs)
                else:
                    return render(request, 'user_app/not_access.html')

        return wrapper_func

    return decorator


# def admin_only(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         group = None
#         if request.user.groups.exists():
#             group = request.user.groups.all()[0].name
#
#         if group == 'USER':
#             return redirect('main_page')
#
#         if group == 'ADMIN':
#             return view_func(request, *args, **kwargs)
#
#     return wrapper_func
