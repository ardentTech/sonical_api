from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from utils.models import Creatable, Modifiable


class SonicalUserManager(UserManager):

    def create_user(self, email, password=None, **kwargs):
        return self._create_user(email, password, False, False, **kwargs)

    def create_superuser(self, email, password=None, **kwargs):
        return self._create_user(email, password, True, True, **kwargs)

    def _create_user(self, email, password, is_staff, is_superuser, **kwargs):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email, is_staff=is_staff, is_active=True,
            is_superuser=is_superuser, date_joined=timezone.now(), **kwargs)
        user.set_password(password)
        user.save(user=self._db)
        return user


class User(Creatable, Modifiable, PermissionsMixin, AbstractBaseUser):

    email = models.EmailField(
        _("email address"),
        unique=True)
    is_active = models.BooleanField(
        _("is active"),
        default=True,
        help_text=("Designates whether this user should be treated as active.")
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site.")
    )
    objects = SonicalUserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email
