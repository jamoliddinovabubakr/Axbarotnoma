from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from user_app.validator import validate_file_size


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

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(_("Username"), max_length=100, blank=True, unique=True)
    last_name = models.CharField(_('Surname'), max_length=100, blank=True)
    first_name = models.CharField(_('Name'), max_length=100, blank=True)
    middle_name = models.CharField(_('Middle Name'), max_length=30, null=True, blank=True)
    birthday = models.DateField(_('Birthday'), null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True)
    avatar = models.ImageField(_("Avatar"), upload_to='avatars/', default='user.png',
                               validators=[validate_file_size, FileExtensionValidator(['png', 'jpg'])], blank=True,
                               null=True)
    email = models.EmailField(_('Email address'), max_length=255, blank=True, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Phone number', unique=True)
    pser = models.CharField(_('Passport '), max_length=2, blank=True, null=True)
    pnum = models.CharField(_('Passport '), max_length=7, blank=True, null=True)
    work = models.CharField(max_length=255, null=True, blank=True)
    region = models.ForeignKey('user_app.Region', on_delete=models.CASCADE, verbose_name="Region", null=True,
                                  blank=True)
    role = models.ManyToManyField('user_app.Role', related_name="user_roles", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     if self.role is None:
    #         admin = Role.objects.get(pk=1)
    #         author = Role.objects.get(pk=4)
    #         if self.is_superuser:
    #             self.role.add(admin)
    #     super().save(*args, **kwargs)

    @property
    def full_name(self):
        if self.first_name is not None and self.last_name is not None:
            full_name_user = '%s %s' % (self.last_name, self.first_name)
        else:
            full_name_user = '%s' % self.username
        return full_name_user

    @property
    def get_roles(self):
        roles = []
        for role in self.role.all():
            roles.append(role.id)
        return roles

    def __str__(self):
        return self.username


class Author(models.Model):
    user = models.ForeignKey('user_app.User', on_delete=models.CASCADE, blank=True)


class Editor(models.Model):
    user = models.ForeignKey('user_app.User', on_delete=models.CASCADE, blank=True)


class Reviewer(models.Model):
    section = models.ManyToManyField('article_app.Section', related_name="reviewer_sections", blank=True)
    user = models.ForeignKey('user_app.User', on_delete=models.CASCADE, blank=True)
    mfile = models.FileField(_("Multiple File"), upload_to='files/reviewer/',
                             validators=[FileExtensionValidator(['doc', 'docx', 'pdf'])], blank=True)
    is_reviewer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Menu(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    menu_tr = models.PositiveSmallIntegerField(default=0)
    status = models.BooleanField(default=True)
    allowed_roles = models.ManyToManyField('user_app.Role', related_name='allowed_role_menus', blank=True)

    # parent_id = models.PositiveIntegerField(default=0)
    # type_menu = models.PositiveSmallIntegerField(default=0)

    def get_roles(self):
        return [p.name for p in self.allowed_roles.all()]

    def save(self, *args, **kwargs):
        menus = self.objects.all()
        if menus.count() > 0:
            self.menu_tr = menus.last().menu_tr + 1
        else:
            self.menu_tr = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(f"{self.url}")
