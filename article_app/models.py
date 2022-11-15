import os

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.template.defaultfilters import slugify


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
    stage = models.ForeignKey('article_app.Stage', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


def user_directory_path(instance, filename):
    return 'files/articles/{0}'.format(filename)


class Article(models.Model):
    section = models.ForeignKey('article_app.Section', verbose_name="Section", related_name="article_section",
                                on_delete=models.CASCADE, blank=True)
    author = models.ForeignKey('user_app.User', on_delete=models.CASCADE, related_name="article_authors", blank=True)
    file = models.ForeignKey('article_app.ArticleFile', related_name="article_file", blank=True,
                             on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, blank=True)
    abstract = RichTextField(blank=True)
    keywords = RichTextField(blank=True)
    references = RichTextField(blank=True, null=True)
    article_status = models.ForeignKey('article_app.ArticleStatus', on_delete=models.CASCADE, blank=True, null=True)
    is_publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    @property
    def file_name(self):
        return self.file.name.split("/")[1].replace('_', ' ').replace('-', ' ')

    @property
    def file_size(self):
        return self.file.size

    @property
    def file_type(self):
        name, type = os.path.splitext(self.file.name)
        return type

    # def get_absolute_url(self):
    #     return reverse('article_app:document-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.article)


class ExtraAuthor(models.Model):
    article = models.ForeignKey('article_app.Article', on_delete=models.CASCADE, blank=True)
    lname = models.CharField(max_length=50, blank=True)
    fname = models.CharField(max_length=50, blank=True)
    mname = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    work = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.fname


class Submission(models.Model):
    article = models.ForeignKey('article_app.Article', on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey('user_app.User', on_delete=models.CASCADE, blank=True, null=True)
    file = models.ForeignKey('article_app.ArticleFile', related_name="submission_file", blank=True,
                             on_delete=models.CASCADE, null=True)
    article_status = models.ForeignKey('article_app.ArticleStatus', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class StatusReviewer(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class ReviewerArticle(models.Model):
    article = models.ForeignKey('article_app.Article', on_delete=models.CASCADE, blank=True, null=True)
    reviewer = models.ForeignKey('user_app.Reviewer', on_delete=models.CASCADE, blank=True, null=True)
    editor = models.ForeignKey('user_app.Editor', on_delete=models.CASCADE, blank=True, null=True)
    comment = models.TextField(help_text="Message")
    status = models.ForeignKey('article_app.StatusReviewer', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


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
    message = models.TextField(_("Message"), max_length=255, null=True, blank=True)
    notification_status = models.ForeignKey('article_app.NotificationStatus', on_delete=models.CASCADE, blank=True,
                                            null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-id']


class Journal(models.Model):
    file_pdf = models.FileField(_("Fayl"), upload_to="files/jurnals/", max_length=255, blank=True, null=True)
    journal_number = models.PositiveBigIntegerField(default=0, unique=True)
    journal_year = models.CharField(max_length=4, blank=True)
    img = models.ImageField(upload_to='jurnal/', default='jurnal_ob.png')
    article = models.ManyToManyField('Article', related_name='articles', blank=True)
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
