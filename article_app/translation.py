from modeltranslation.translator import register, TranslationOptions
from article_app.models import Category, Post, BlankPage


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'tag', 'desc',)


@register(BlankPage)
class BlankPageTranslationOptions(TranslationOptions):
    fields = ('title', 'body',)
