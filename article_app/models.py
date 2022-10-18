from email.policy import default
from operator import mod
from pyexpat import model
from tkinter.tix import Tree
from turtle import title
from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(_('Nomi'), max_length=150)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Kategoriya")
        verbose_name_plural = _("Kategoriyalar")


def user_directory_path(instance, filename):
    return 'files/user_{0}/{1}'.format(instance.author.id, filename)


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoriya", blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    abstract = RichTextField(blank=True, null=True)
    keywords = RichTextField(blank=True, null=True)
    references = RichTextField(blank=True, null=True)
    author = models.ForeignKey('user_app.User', verbose_name='Author', on_delete=models.CASCADE,
                               related_name="article_author")
    file = models.FileField(_("Word Fayl"), upload_to=user_directory_path, max_length=255, blank=True, )
    file_pdf = models.FileField(_("PDF Fayl"), upload_to=user_directory_path, max_length=255, blank=True, null=True)
    state = models.ForeignKey('user_app.State', on_delete=models.CASCADE, related_name="article_state",
                              blank=True,
                              null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_publish = models.BooleanField(default=True)
    # url = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("article_detail", kwargs={"slug": self.url})

    class Meta:
        ordering = ['id']
        verbose_name = _("Maqola")
        verbose_name_plural = _("Maqolalar")


class Authors(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(_("Ism"), max_length=255)
    last_name = models.CharField(_("Familiya"), max_length=255)
    middle_name = models.CharField(_("Sharif"), max_length=255, blank=True, null=True)
    email = models.EmailField(_('Email'), max_length=255)
    work_place = models.CharField(_('Ish joy'), max_length=255)
    author_order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = _("Aftor")
        verbose_name_plural = _("Aftorlar")


class MyResendArticle(models.Model):
    author = models.ForeignKey('user_app.User', verbose_name='Author', on_delete=models.CASCADE, blank=True, null=True,
                               related_name="article_resend_author")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True)
    file_word = models.FileField(_("Word Fayl"), upload_to='files/', max_length=255, blank=True, )
    message = models.CharField(_("Xabar"), max_length=255, blank=True, null=True)
    state = models.ForeignKey('user_app.State', on_delete=models.CASCADE,
                              blank=True,
                              null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.article)


class Journal(models.Model):
    file_pdf = models.FileField(_("Fayl"), upload_to="files/jurnals/", max_length=255, blank=True, null=True)
    number_magazine = models.PositiveBigIntegerField(default=0, unique=True)
    year_magazine = models.CharField(max_length=4, blank=True)
    img = models.ImageField(upload_to='jurnal/', default='jurnal_ob.png')
    article = models.ManyToManyField('Article', related_name='articles', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def get_articles(self):
        return [p.title for p in self.article.all()]

    def __str__(self):
        return str(self.number_magazine)

    class Meta:
        verbose_name = _("Magazine")
        verbose_name_plural = _("Magazines")


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    tag = RichTextField(blank=True, null=True)
    img = models.ImageField(upload_to='blog/')
    desc = RichTextField(blank=True, null=True)
    is_publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.SlugField(max_length=200, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.url})

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = slugify(self.title, allow_unicode=True)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Elon")
        verbose_name_plural = _("Elonlar")


class BlankPage(models.Model):
    title = models.CharField(max_length=255, unique=True)
    body = RichTextField(blank=True, null=True)
    is_publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("BlankPage")
        verbose_name_plural = _("BlankPages")
