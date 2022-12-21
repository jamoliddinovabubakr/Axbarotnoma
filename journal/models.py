from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Journal(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    file_pdf = models.FileField(_("Fayl"), upload_to="files/journals", max_length=255, null=True,
                                validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
                                help_text='Please upload only .pdf!')
    number = models.PositiveBigIntegerField(unique=True)
    year = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_publish = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    is_split = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Journal")


class JournalArticle(models.Model):
    journal = models.ForeignKey('journal.Journal', on_delete=models.CASCADE, related_name="journal_article")
    article = models.ForeignKey('article_app.Article', on_delete=models.CASCADE, related_name="article")
    start_page = models.PositiveBigIntegerField(default=0)
    end_page = models.PositiveBigIntegerField(default=0)
    article_pdf = models.FileField(_("Fayl"), upload_to="files/split_article", max_length=255, null=True,
                                validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
                                help_text='Please upload only .pdf!')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
