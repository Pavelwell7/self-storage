import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .manager import CustomUserManager


class User(AbstractUser):
    username = None

    first_name = models.CharField(
        "имя",
        max_length=255,
        blank=True,
        default="",
    )
    last_name = models.CharField(
        "фамилия",
        max_length=255,
        blank=True,
        default="",
    )
    email = models.EmailField(
        "емайл",
        unique=True,
    )
    phone = PhoneNumberField(
        "Номер телефона",
        db_index=True,
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        "аватар",
        upload_to="avatars/",
        blank=True,
        null=True,
    )

    access_token = models.UUIDField(
        "Токен доступа",
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
    )

    objects = CustomUserManager()  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Feedback(models.Model):
    email = models.EmailField("Email", blank=True, null=True)
    created_at = models.DateTimeField("Дата заявки", auto_now_add=True)
    phone = PhoneNumberField("Номер телефона", blank=True, null=True)

    class Meta:
        verbose_name = "Заявка на обратную связь"
        verbose_name_plural = "Заявки на обратную связь"

    def __str__(self):
        if self.phone:
            return f"{self.phone} {self.created_at}"
        return f"{self.email}  {self.created_at}"
