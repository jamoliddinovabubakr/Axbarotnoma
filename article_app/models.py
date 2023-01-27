import os

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Section(models.Model):
    name = models.CharField(_('Name'), max_length=150, blank=True, default=None)

    def __str__(self):
        return self.name


class ArticleType(models.Model):
    name = models.CharField(_('Name'), max_length=150, blank=True, default=None)

    def __str__(self):
        return self.name


class ArticleLanguage(models.Model):
    name = models.CharField(_('Name'), max_length=150, blank=True, default=None)

    def __str__(self):
        return self.name


class Stage(models.Model):
    name = models.CharField(_('Name'), max_length=100, default=None)

    def __str__(self):
        return self.name


class ArticleStatus(models.Model):
    name = models.CharField(max_length=100, default=None)
    stage = models.ForeignKey('article_app.Stage', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


def user_directory_path(instance, filename):
    return 'files/articles/{0}'.format(filename)


class Article(models.Model):
    article_type = models.ForeignKey('article_app.ArticleType', on_delete=models.CASCADE, blank=True)
    country = models.ForeignKey('user_app.Country', on_delete=models.CASCADE, blank=True)
    article_lang = models.ForeignKey('article_app.ArticleLanguage', on_delete=models.CASCADE, blank=True)
    section = models.ForeignKey('article_app.Section', verbose_name="Section", related_name="article_section",
                                on_delete=models.CASCADE, blank=True)
    author = models.ForeignKey('user_app.User', on_delete=models.CASCADE, related_name="article_author", blank=True)
    file = models.ForeignKey('article_app.ArticleFile', related_name="article_file", blank=True,
                             on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, blank=True)
    title_en = models.CharField(max_length=255, blank=True)
    abstract = RichTextUploadingField(blank=True)
    abstract_en = RichTextUploadingField(blank=True)
    keywords = RichTextField(blank=True)
    keywords_en = RichTextField(blank=True)
    references = RichTextField(blank=True, null=True)
    article_status = models.ForeignKey('article_app.ArticleStatus', on_delete=models.CASCADE, blank=True, null=True)
    is_publish = models.BooleanField(default=False)
    is_resubmit = models.BooleanField(default=False)
    is_publish_journal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    filePDF = models.FileField(_("Pdf Fayl"), upload_to="files/articles/%Y/%m/%d", blank=True, null=True,
                                validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']


class ArticleFile(models.Model):
    article = models.ForeignKey('article_app.Article', on_delete=models.CASCADE, blank=True)
    file = models.FileField(_("Word Fayl"), upload_to="files/articles/%Y/%m/%d", max_length=255, blank=True,
                            validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx'])],
                            help_text='Please upload only .doc or .docx files!')
    file_status = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def file_name(self):
        return str(self.file.name.split("/")[-1].replace('_', ' ').replace('-', ' '))

    def file_size(self):
        return self.file.size

    def file_type(self):
        name, type_f = os.path.splitext(self.file.name)
        return type_f

    # def get_absolute_url(self):
    #     return reverse('article_app:document-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.article)


class ExtraAuthor(models.Model):
    article = models.ForeignKey('article_app.Article', on_delete=models.CASCADE, blank=True)
    lname = models.CharField(max_length=50, blank=True)
    fname = models.CharField(max_length=50, blank=True)
    mname = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True)
    work = models.CharField(max_length=255, blank=True, null=True)
    scientific_degree = models.ForeignKey('user_app.ScientificDegree', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.fname


class NotificationStatus(models.Model):
    name = models.CharField(_('Name'), max_length=50, blank=True)

    def __str__(self):
        return self.name


class Notification(models.Model):
    article = models.ForeignKey('article_app.Article', on_delete=models.CASCADE, blank=True)
    from_user = models.ForeignKey('user_app.User', on_delete=models.CASCADE, related_name="sender_user", blank=True,
                                  null=True)
    to_user = models.ForeignKey('user_app.User', on_delete=models.CASCADE, related_name="recieve_user", blank=True,
                                null=True)
    message = models.TextField(_("Message"), blank=True)
    notification_status = models.ForeignKey('article_app.NotificationStatus', on_delete=models.CASCADE, blank=True,
                                            null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_update_article = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
