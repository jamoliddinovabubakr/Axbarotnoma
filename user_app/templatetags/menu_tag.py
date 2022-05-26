from django import template

from user_app.models import Menu

register = template.Library()


@register.simple_tag()
def get_sub_menus():
    menus = Menu.objects.filter(type_menu=2).filter(status=True).order_by('menu_tr')
    return menus


@register.inclusion_tag("user_app/includes/menus.html")
def get_allow_menus(user_id: int = None):
    menus_id = []
    menyular = Menu.objects.filter(status=True).order_by('menu_tr')

    for menu in menyular:
        t = []
        allows = menu.allowed_roles.all()
        pk_list = [obj.pk for obj in allows]

        for id in pk_list:
            t.append(id)
        if user_id in t:
            menus_id.append(menu.pk)

    return {'allow_menus': Menu.objects.filter(pk__in=menus_id)}
