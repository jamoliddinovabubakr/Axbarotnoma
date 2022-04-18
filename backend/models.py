from django.db import models
from django.contrib.auth.models import AbstractUser, Group, GroupManager
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Region(models.Model):
    name = models.CharField(_('Nomi'), max_length=150)
    key = models.PositiveSmallIntegerField(_("Key"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Viloyat")
        verbose_name_plural = _("Viloyatlar")


class District(models.Model):
    name = models.CharField(_('Nomi'), max_length=150)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Viloyat")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Tuman")
        verbose_name_plural = _("Tumanlar")


class Gender(models.Model):
    name = models.CharField(_('Jins'), max_length=50)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(_('Roli'), max_length=255, unique=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(_("Username"), max_length=100, blank=True, unique=True)
    first_name = models.CharField(_('Familiya'), max_length=100, blank=True, null=True)
    last_name = models.CharField(_('Ism'), max_length=100, blank=True, null=True)
    middle_name = models.CharField(_('Otasini ismi'), max_length=30, null=True, blank=True)
    birthday = models.DateField(_('Tugilgan kun'), null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True, )
    avatar = models.ImageField(_("Avatar"), upload_to='avatars/', default='user.png')
    email = models.EmailField(_('Email address'), blank=True, null=True)
    phone = models.CharField(max_length=13, null=True, blank=True, verbose_name='Telefon raqam', unique=True)
    passport = models.CharField(_('Pasport'), max_length=15, blank=True, null=True)
    work_place = models.CharField(_("Ish joy"), max_length=255, blank=True, null=True)
    position = models.CharField(_("Lavozim"), max_length=255, blank=True, null=True)
    role = models.ForeignKey(Role, related_name="user_role", on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Viloyat", null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="Tuman", null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "middle_name", "password1", "password2"]

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

    def __str__(self):
        return self.username

    def is_admin(self) -> bool:
        return self.groups.filter(name='ADMIN').exists()

    def is_user(self):
        return self.groups.filter(name='USER').exists()

    def is_editor(self):
        return self.groups.filter(name='MUHARRIR').exists()

    def is_analitic(self):
        return self.groups.filter(name='TAHLILCHI').exists()

    class Meta:
        verbose_name = _('Foydalanuvchi')
        verbose_name_plural = _('Foydalanuvchilar')


class State(models.Model):
    name = models.CharField(max_length=100, default=None)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Notification(models.Model):
    STATUS = (
        (0, _("O\'qilmadi")),
        (1, _('O\'qildi')),
    )

    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(blank=True, null=True)
    from_user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                                     related_name="from_user")
    to_user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name="to_user")
    status = models.CharField(max_length=50, choices=STATUS, default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Menu(models.Model):
    name = models.CharField(max_length=100)
    parent_id = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)
    icon = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(f"{self.url}")
