from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from django.utils.translation import gettext_lazy as _


class Journal(models.Model):
    file_pdf = models.FileField(_("Fayl"), upload_to="files/jurnals/", max_length=255, null=True)
    journal_number = models.PositiveBigIntegerField(unique=True)
    journal_year = models.CharField(max_length=4)
    article = models.ManyToManyField('article_app.Article', related_name='articles', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def get_articles(self):
        return [p.title for p in self.article.all()]

    def __str__(self):
        return str(self.journal_number)

    class Meta:
        verbose_name = _("Journal")
        verbose_name_plural = _("Journals")


class SplitPdf(models.Model):
    start_page = models.PositiveIntegerField(default=0, null=True)
    finish_page = models.PositiveIntegerField(default=0, null=True)
    article = models.ForeignKey('article_app.Article', on_delete=models.CASCADE)
    file = models.FileField(upload_to="files/articles/%Y/%m/%d", blank=True, null=True)

    def __str__(self):
        return f'{self.id}, {self.article}, {self.start_page}, {self.finish_page}, {self.file}'


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


class Post(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    tag = RichTextField(blank=True, null=True)
    img = models.ImageField(upload_to='blog/')
    desc = RichTextField(blank=True, null=True)
    is_publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.SlugField(max_length=200, unique=True)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.url})

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = slugify(self.title, allow_unicode=True)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
