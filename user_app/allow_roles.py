from .models import Menu


def allow(f):
    allow_roles = None
    menus = Menu.objects.all()

    for item in menus:
        if item.url == f:
            allow_roles = item.get_roles()
            break
    return allow_roles
