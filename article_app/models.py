from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(_('Nomi'), max_length=150)
    key = models.PositiveSmallIntegerField(_("Key"))
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Kategoriya")
        verbose_name_plural = _("Kategoriyalar")


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'files/user_{0}/{1}'.format(instance.author.id, filename)


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoriya", blank=True, null=True)
    title = RichTextField(blank=True, null=True)
    abstract = RichTextField(blank=True, null=True)
    keywords = RichTextField(blank=True, null=True)
    references = RichTextField(blank=True, null=True)
    author = models.ForeignKey('user_app.User', verbose_name='Author', on_delete=models.CASCADE,
                               related_name="article_author")
    editor = models.ForeignKey('user_app.User', verbose_name='Taxrirchi', on_delete=models.CASCADE, blank=True,
                               null=True,
                               related_name="article_editor")
    analyst = models.ForeignKey('user_app.User', verbose_name='Tahlilchi', on_delete=models.CASCADE, blank=True,
                                null=True,
                                related_name="article_analyst")
    file = models.FileField(_("Fayl"), upload_to=user_directory_path, max_length=255)
    payed = models.BooleanField(default=True)
    state_edit = models.ForeignKey('user_app.State', on_delete=models.CASCADE, related_name="article_state_edit",
                                   blank=True,
                                   null=True)
    state_analysis = models.ForeignKey('user_app.State', on_delete=models.CASCADE, blank=True,
                                       null=True,
                                       related_name="article_state_analysis")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    # url = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("article_detail", kwargs={"slug": self.url})

    class Meta:
        ordering = ['-id']
        verbose_name = _("Maqola")
        verbose_name_plural = _("Maqolalar")


class Shartnoma(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    body = RichTextField(blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Authors(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    first_name = models.CharField(_("Ism"), max_length=255)
    last_name = models.CharField(_("Familiya"), max_length=255)
    middle_name = models.CharField(_("Sharif"), max_length=255, blank=True, null=True)
    email = models.CharField(_('Email'), max_length=255)
    work_place = models.CharField(_('Ish joy'), max_length=255)
    author_order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = _("Aftor")
        verbose_name_plural = _("Aftorlar")


class Page(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    value = models.PositiveBigIntegerField(default=5, unique=True)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")


class Magazine(models.Model):
    number_magazine = models.PositiveBigIntegerField(default=0, unique=True)
    year_magazine = models.CharField(max_length=4, blank=True)
    article = models.ManyToManyField('Article', related_name='articles', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.number_magazine)

    class Meta:
        verbose_name = _("Magazine")
        verbose_name_plural = _("Magazines")
