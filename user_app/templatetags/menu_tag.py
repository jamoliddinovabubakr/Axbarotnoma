from django import template
from user_app.models import Menu

register = template.Library()


# @register.simple_tag()
# def menus():
#     return Menu.objects.filter(status=True).filter(type=0).order_by('order')
