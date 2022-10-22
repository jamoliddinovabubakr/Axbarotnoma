from email.policy import default
from operator import mod
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, GroupManager, Permission
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from article_app.models import Article, MyResendArticle, Category


class Region(models.Model):
    name = models.CharField(_('Nomi'), max_length=150)
    key = models.PositiveSmallIntegerField(_("Key"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Viloyat")
        verbose_name_plural = _("Viloyatlar")


class Gender(models.Model):
    name = models.CharField(_('Jins'), max_length=50)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(_('Roli'), max_length=255, unique=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(_("Username"), max_length=100, blank=True, unique=True)
    first_name = models.CharField(_('Ism'), max_length=100, blank=True, null=True)
    last_name = models.CharField(_('Familiya'), max_length=100, blank=True, null=True)
    middle_name = models.CharField(_('Otasini ismi'), max_length=30, null=True, blank=True)
    birthday = models.DateField(_('Tugilgan kun'), null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True, )
    avatar = models.ImageField(_("Avatar"), upload_to='avatars/', default='user.png')
    email = models.CharField(_('Email address'), max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Telefon raqam', unique=True)
    passport = models.CharField(_('Pasport'), max_length=15, blank=True, null=True)
    role = models.ForeignKey('Role', related_name="user_role", on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey('Region', on_delete=models.CASCADE, verbose_name="Viloyat", null=True, blank=True)
    speciality = models.ManyToManyField(Category, related_name="user_speciality")

    def save(self, *args, **kwargs):
        rollar = Role.objects.all()
        if rollar and self.role is None:
            rol = None
            if self.is_superuser:
                rol = rollar.get(name='MASTER')
            if self.is_staff and not self.is_superuser:
                rol = rollar.get(name='ADMIN')
            if not self.is_staff:
                rol = rollar.get(name='USER')
            self.role_id = rol.id
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    # def get_user_permissions(self):
    #     if self.is_superuser:
    #         return Permission.objects.all()
    #     return Permission.objects.filter(group__user=self)

    def __str__(self):
        return self.email

    # def is_master(self) -> bool:
    #     return self.groups.filter(name='Master').exists()
    #
    # def is_admin(self) -> bool:
    #     return self.groups.filter(name='ADMIN').exists()
    #
    # def is_user(self):
    #     return self.groups.filter(name='USER').exists()
    #
    # def is_redactor(self):
    #     return self.groups.filter(name='MUHARRIR').exists()
    #
    # def is_editor(self):
    #     return self.groups.filter(name='TAHRIRCHI').exists()

    class Meta:
        verbose_name = _('Foydalanuvchi')
        verbose_name_plural = _('Foydalanuvchilar')


class State(models.Model):
    name = models.CharField(max_length=100, default=None)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=100)
    parent_id = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)
    icon = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    type_menu = models.PositiveSmallIntegerField(default=0)
    menu_tr = models.PositiveSmallIntegerField(default=0)
    allowed_roles = models.ManyToManyField('Role', related_name='allowed_role_menus', blank=True)

    def get_roles(self):
        return [p.name for p in self.allowed_roles.all()]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(f"{self.url}")


class Notification(models.Model):
    CHECKED = 'Tekshirildi'
    UNCHECK = 'Tekshirilmadi'
    CHECKING = 'Tekshirilmoqda'

    STATUS = (
        (CHECKED, 'tekshirildi'),
        (UNCHECK, 'tekshirilmadi'),
        (CHECKING, 'tekshirilmoqda'),
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS, default=UNCHECK)
    created_at = models.DateTimeField(auto_now_add=True)
    my_resend = models.ForeignKey(MyResendArticle, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
