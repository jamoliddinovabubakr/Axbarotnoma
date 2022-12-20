from django.contrib.auth import logout
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404

from user_app.models import Menu, User, Role


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


def allowed_users(role=None):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if role is not None:
                user = get_object_or_404(User, pk=request.user.id)
                if len(role) == 1:
                    current_user_roles = user.roles.all()
                    rol = Role.objects.get(code_name=role[0])
                    if rol in current_user_roles:
                        return view_func(request, *args, **kwargs)
                    else:
                        return render(request, 'user_app/not_access.html')
                if len(role) > 1:
                    r, lv = user.get_roles
                    current_role_level = min(lv)
                    levels = []
                    for code_name in role:
                        t = get_object_or_404(Role, code_name=code_name)
                        levels.append(t.level)
                    if current_role_level in levels:
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
