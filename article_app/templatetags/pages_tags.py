from django import template
from article_app.models import  Journal, Post

register = template.Library()


@register.simple_tag()
def get_pages():
    pages = Page.objects.all()
    return pages


# @register.simple_tag()
# def get_jurnals():
#     jurnals = Magazine.objects.all().order_by('-id')[:10]
#     return jurnals
#

@register.simple_tag()
def get_last_posts():
    posts = Post.objects.all().order_by('-id')[:5]
    return posts
