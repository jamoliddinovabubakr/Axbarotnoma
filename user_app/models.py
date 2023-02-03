import os

from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from user_app.validator import validate_file_size


class Country(models.Model):
    name = models.CharField(_('Name'), max_length=50)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(_('Name'), max_length=50)

    def __str__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField(_('Name'), max_length=10)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)
    code_name = models.CharField(max_length=10, blank=True, null=True)
    level = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(_("Username"), max_length=100, blank=True, unique=True)
    last_name = models.CharField(_('Surname'), max_length=100, blank=True)
    first_name = models.CharField(_('Name'), max_length=100, blank=True)
    middle_name = models.CharField(_('Middle Name'), max_length=30, null=True, blank=True)
    birthday = models.DateField(_('Birthday'), null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True)
    avatar = models.ImageField(_("Avatar"), upload_to='avatars/%Y/%m/%d', default='user.png',
                               validators=[validate_file_size, FileExtensionValidator(['png', 'jpg'])], blank=True,
                               null=True)
    email = models.EmailField(_('Email address'), max_length=255, blank=True, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Phone number', unique=True)
    pser = models.CharField(_('Passport '), max_length=2, blank=True, null=True)
    pnum = models.CharField(_('Passport '), max_length=7, blank=True, null=True)
    work = models.CharField(max_length=255, null=True, blank=True)
    region = models.ForeignKey('user_app.Region', on_delete=models.CASCADE, verbose_name="Region", null=True,
                               blank=True)
    roles = models.ManyToManyField('user_app.Role', related_name="user_roles", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        if self.first_name is not None and self.last_name is not None:
            full_name_user = f"{self.last_name} {self.first_name}"
        else:
            full_name_user = f"{self.username}"
        return full_name_user

    @property
    def get_roles(self):
        roles = []
        levels = []
        for role in self.roles.all():
            roles.append(role.id)
            levels.append(role.level)
        return roles, levels

    def __str__(self):
        return self.username


class Editor(models.Model):
    user = models.ForeignKey('user_app.User', on_delete=models.CASCADE, blank=True)
    is_editor = models.BooleanField(default=False)


class ScientificDegree(models.Model):
    name = models.CharField(max_length=255, blank=True, unique=True)
    level = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name


class Reviewer(models.Model):
    section = models.ManyToManyField('article_app.Section', related_name="reviewer_sections", blank=True)
    scientific_degree = models.ForeignKey('user_app.ScientificDegree', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('user_app.User', on_delete=models.CASCADE, blank=True, null=True)
    is_reviewer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ReviewerFile(models.Model):
    reviewer = models.ForeignKey('user_app.Reviewer', on_delete=models.CASCADE, blank=True)
    file = models.FileField(_("Fayl"), upload_to="files/reviewer/%Y/%m/%d", max_length=255, blank=True, null=True,
                            validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', 'pdf'])],
                            help_text='Please upload only .doc, .docx or .pdf files!')

    def file_name(self):
        return str(self.file.name.split("/")[-1].replace('_', ' ').replace('-', ' '))

    def file_size(self):
        return self.file.size

    def file_type(self):
        name, type_f = os.path.splitext(self.file.name)
        return type_f


class ReviewerEditorStatus(models.Model):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class ReviewerEditor(models.Model):
    reviewer = models.ForeignKey('user_app.Reviewer', blank=True, on_delete=models.CASCADE)
    editor = models.ForeignKey('user_app.Editor', on_delete=models.CASCADE, blank=True)
    status = models.ForeignKey('user_app.ReviewerEditorStatus', on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class StatusReview(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)

    def __str__(self):
        return self.name


class ReviewerArticle(models.Model):
    article = models.ForeignKey('article_app.Article', on_delete=models.CASCADE, related_name="review_article",
                                blank=True)
    editor = models.ForeignKey('user_app.Editor', on_delete=models.CASCADE, related_name="review_editor", blank=True)
    reviewer = models.ForeignKey('user_app.Reviewer', on_delete=models.CASCADE, related_name="review_reviewer",
                                 blank=True)
    status = models.ForeignKey('user_app.StatusReview', on_delete=models.CASCADE, related_name="review_status",
                               blank=True)
    comment = models.TextField()
    result = models.PositiveSmallIntegerField(default=0)
    is_extra = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Menu(models.Model):
    name = models.CharField(max_length=100)
    icon_name = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    url_name = models.CharField(max_length=255, null=True, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    status = models.BooleanField(default=True)
    allowed_roles = models.ManyToManyField('user_app.Role', related_name='allowed_role_menus', blank=True)
    type = models.PositiveSmallIntegerField(default=0)

    def get_roles(self):
        return [p.name for p in self.allowed_roles.all()]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(f'{self.url_name}')
