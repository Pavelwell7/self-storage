from django.contrib.auth.models import AbstractUser
from django.db import models


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
    phone = models.CharField(
        "телефон",
        max_length=20,
        blank=True,
        default="",
    )
    avatar = models.ImageField(
        "аватар",
        upload_to="avatars/",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        
    def __str__(self):
        return self.email
