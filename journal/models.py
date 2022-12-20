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
    articles = models.ManyToManyField('article_app.Article', related_name='articles', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_publish = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    def get_articles(self):
        return [p.title for p in self.articles.all()]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Journal")


# class SplitPdf(models.Model):
#     start_page = models.PositiveIntegerField(default=0, null=True)
#     finish_page = models.PositiveIntegerField(default=0, null=True)
#     article = models.ForeignKey('article_app.Article', on_delete=models.CASCADE)
#     file = models.FileField(upload_to="files/articles/%Y/%m/%d", blank=True, null=True)
#
#     def __str__(self):
#         return f'{self.id}, {self.article}, {self.start_page}, {self.finish_page}, {self.file}'
