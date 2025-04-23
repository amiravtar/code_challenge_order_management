
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.db import models

from utils.validators import NAME_VALIDATOR, USERNAME_VALIDATOR


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("نام کاربری نباید خالی باشد")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("سوپر یوزر باید دسترسی استاف داشته باشد")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("سوپر یوزر باید دسترسی کامل داشته باشد")

        return self.create_user(username, password, **extra_fields)


class User(AbstractUser):
    # Define a regex validator that only allows letters (both cases), numbers, and underscores.

    username = models.CharField(
        verbose_name="نام کاربری",
        max_length=150,
        unique=True,
        error_messages={
            "unique": "این نام کاربری قبلا استفاده شده است",
            "blank": "نام کاربری نباید خالی باشد",
        },
        validators=[USERNAME_VALIDATOR],
    )
    password = models.CharField(
        verbose_name="رمز عبور",
        max_length=128,
        error_messages={
            "blank": "رمز عبور نباید خالی باشد",
        },
    )
    first_name = models.CharField(
        verbose_name="نام",
        max_length=150,
        blank=True,
        error_messages={
            "blank": "نام نباید خالی باشد",
        },
        validators=[NAME_VALIDATOR],
    )
    last_name = models.CharField(
        verbose_name="نام خانوادگی",
        max_length=150,
        blank=True,
        error_messages={
            "blank": "نام خانوادگی نباید خالی باشد",
        },
        validators=[NAME_VALIDATOR],
    )
    email = models.EmailField(
        verbose_name="ایمیل",
        blank=True,
        error_messages={
            "invalid": "آدرس ایمیل معتبر نیست",
            "blank": "ایمیل نباید خالی باشد",
        },
    )

    objects = UserManager()  # type: ignore

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.username
