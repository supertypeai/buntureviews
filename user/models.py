from django.db import models
from django.contrib import auth
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from user.token import get_token
from django.contrib.auth.models import (
    AbstractBaseUser,
    UserManager,
    Group,
    _user_get_permissions,
    _user_has_perm,
    _user_has_module_perms,
)
from common.mails.mail_base import EmailHandler

import logging

logger = logging.getLogger(__name__)


class BaseManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")

        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        if password is not None:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    def _user_get_permissions(user, obj, from_name):
        permissions = set()
        name = "get_%s_permissions" % from_name
        for backend in auth.get_backends():
            if hasattr(backend, name):
                permissions.update(getattr(backend, name)(user, obj))
        return permissions


class PermissionsMixin(models.Model):
    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_(
            "Designates that this user has all permissions without "
            "explicitly assigning them."
        ),
    )
    role = models.ForeignKey(
        Group, related_name="g_users", blank=True, null=True, on_delete=models.PROTECT
    )

    class Meta:
        abstract = True

    def get_user_permissions(self, obj=None):
        return _user_get_permissions(self, obj, "user")

    def get_group_permissions(self, obj=None):
        return _user_get_permissions(self, obj, "role")

    def get_all_permissions(self, obj=None):
        return _user_get_permissions(self, obj, "all")

    def has_perm(self, perm, obj=None):
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)


class UserAbstract(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={"unique": _("A user with that username already exists."),},
    )
    email = models.EmailField(_("email address"), unique=True, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = BaseManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name


class User(UserAbstract):
    @classmethod
    def send_password_reset_link(cls, instance):
        if not isinstance(instance, cls):
            return False, "Wrong Data Format"

        uid = urlsafe_base64_encode(force_bytes(instance.id))
        token = get_token.make_token(instance)
        reset_pass_url = (
            "localhost:8000" + "/password/change/" + uid + "/" + token + "/"
        )
        mail_body = {
            "USERNAME": instance.username,
            "USER_EMAIL": instance.email,
            "PASSWORD_CHANGE_URL": reset_pass_url,
        }
        try:
            mail_handler = EmailHandler("Password Reset", mail_body, [instance.email,])
            response = mail_handler.user_password_reset_email()
            if response is False:
                return False, "Sending password request is failed"
            else:
                return True, "Password reset link has been sent to email"
        except:
            return False, "Internal Error"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

