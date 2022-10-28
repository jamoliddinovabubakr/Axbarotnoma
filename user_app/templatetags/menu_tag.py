from ast import Not
from django import template

from user_app.models import Menu, Notification

register = template.Library()
get_sub_menus_id = None


@register.inclusion_tag("user_app/includes/menus.html")
def get_allow_menus(role_id: int = None):
    menus_id = []
    menyular = Menu.objects.filter(status=True)

    for menu in menyular:
        allows = menu.allowed_roles.all()
        pk_list = [obj.pk for obj in allows]

        if role_id in pk_list:
            menus_id.append(menu.pk)

    global get_sub_menus_id
    get_sub_menus_id = menus_id

    allow_menus = Menu.objects.filter(pk__in=menus_id).order_by('menu_tr')
    return {'allow_menus': allow_menus}


# @register.simple_tag()
# def get_editor_notifications():
#     notifications = Notification.objects.order_by("-created_at").filter(status='Tekshirilmadi')
#     return notifications


@register.simple_tag()
def get_sub_menus():
    menus = Menu.objects.filter(type_menu=2).filter(
        pk__in=get_sub_menus_id).filter(status=True).order_by('menu_tr')
    return menus