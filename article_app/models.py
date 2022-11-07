from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.template.defaultfilters import slugify

from user_app.models import Author


class Section(models.Model):
    name = models.CharField(_('Name'), max_length=150, blank=True, default=None)

    def __str__(self):
        return self.name


class Stage(models.Model):
    name = models.CharField(_('Name'), max_length=100, default=None)

    def __str__(self):
        return self.name


class ArticleStatus(models.Model):
    name = models.CharField(max_length=100, default=None)
    stage_id = models.ForeignKey('article_app.Stage', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name


def user_directory_path(instance, filename):
    return 'files/user_{0}/{1}'.format(instance.author.id, filename)


class Article(models.Model):
    section_id = models.ForeignKey('article_app.Section', verbose_name="Section", related_name="article_section",
                                on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=255, blank=True)
    abstract = RichTextField(blank=True)
    keywords = RichTextField(blank=True)
    references = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_publish = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']


class ArticleFile(models.Model):
    article_id = models.ForeignKey('article_app.Article', on_delete=models.CASCADE, blank=True)
    file = models.FileField(_("Word Fayl"), upload_to=user_directory_path, max_length=255, blank=True,
                            validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx'])],
                            help_text='Please upload only .doc or .docx files!')
    file_name = models.CharField(max_length=255, default=None)
    file_size = models.CharField(max_length=255, default=None)
    file_type = models.CharField(max_length=255, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name


class Submission(models.Model):
    article_id = models.ForeignKey('article_app.Article', on_delete=models.CASCADE, blank=True, null=True)
    author_id = models.ForeignKey('user_app.Author', on_delete=models.CASCADE, blank=True, null=True)
    editor_id = models.ForeignKey('user_app.Editor', on_delete=models.CASCADE, blank=True, null=True)
    file_id = models.ForeignKey('article_app.ArticleFile', on_delete=models.CASCADE, blank=True, null=True)
    article_status_id = models.ForeignKey('article_app.ArticleStatus', on_delete=models.CASCADE,
                              blank=True,
                              null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class NotificationStatus(models.Model):
    name = models.CharField(_('Name'), max_length=50, blank=True)

    def __str__(self):
        return self.name


class Notification(models.Model):
    submission_id = models.ForeignKey('article_app.Submission', on_delete=models.CASCADE, blank=True)
    from_user_id = models.ForeignKey('user_app.User', on_delete=models.CASCADE, related_name="sender_user",  blank=True, null=True)
    to_user_id = models.ForeignKey('user_app.User', on_delete=models.CASCADE, related_name="recieve_user", blank=True, null=True)
    message = models.CharField(_("Message"), max_length=255, null=True, blank=True)
    notification_status_id = models.ForeignKey('article_app.NotificationStatus', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-id']


class Journal(models.Model):
    file_pdf = models.FileField(_("Fayl"), upload_to="files/jurnals/", max_length=255, blank=True, null=True)
    number_magazine = models.PositiveBigIntegerField(default=0, unique=True)
    year_magazine = models.CharField(max_length=4, blank=True)
    img = models.ImageField(upload_to='jurnal/', default='jurnal_ob.png')
    article = models.ManyToManyField('Article', related_name='articles', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def get_articles(self):
        return [p.title for p in self.article.all()]

    def __str__(self):
        return str(self.number_magazine)

    class Meta:
        verbose_name = _("Journal")
        verbose_name_plural = _("Journals")


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
