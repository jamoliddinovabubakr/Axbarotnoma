from django import template
from article_app.models import Page, Article

register = template.Library()


@register.simple_tag()
def get_pages():
    pages = Page.objects.all()
    return pages


@register.simple_tag()
def get_last_articles():
    articles = Article.objects.all()[:5]
    return articles

