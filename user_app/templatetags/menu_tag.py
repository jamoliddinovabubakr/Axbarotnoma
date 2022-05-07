from django import template
from user_app.models import Menu

register = template.Library()


@register.simple_tag()
def get_menus():
    menus = Menu.objects.filter(status=True).order_by('menu_tr')
    return menus


# @register.inclusion_tag("articles/index.html")
# def get_last_articles(count=5):
#     movies = Article.objects.order_by("id")[:count]
#     return {"last_articles": movies}