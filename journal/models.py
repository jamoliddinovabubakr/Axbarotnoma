from django.db import models
from django.utils.translation import gettext_lazy as _


def _validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class Journal(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    file_pdf = models.FileField(_("Fayl"), upload_to="files/jurnals/", validators=[_validate_file_extension],
                                max_length=255, null=True)
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
