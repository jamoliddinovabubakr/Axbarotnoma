from django import template
from article_app.models import Page

register = template.Library()


@register.simple_tag()
def get_pages():
    pages = Page.objects.all()
    return pages
