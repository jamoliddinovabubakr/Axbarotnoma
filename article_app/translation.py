from modeltranslation.translator import register, TranslationOptions
from article_app.models import Category, MyResendArticle, Post, BlankPage


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(MyResendArticle)
class MyResendArticleTranslationOptions(TranslationOptions):
    fields = ('message',)


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'tag', 'desc',)


@register(BlankPage)
class BlankPageTranslationOptions(TranslationOptions):
    fields = ('title', 'body',)
