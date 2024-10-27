from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        **NULLABLE,
        help_text="Введите номер телефона",
    )
    country = models.CharField(
        max_length=100,
        verbose_name="Страна",
        **NULLABLE,
        help_text="Введите название страны",
    )
    avatar = models.ImageField(
        upload_to="users/photo",
        **NULLABLE,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )
    token = models.CharField(max_length=100, verbose_name="Token", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if 'pbkdf2_sha256' not in self.password:
            password = make_password(self.password)
            self.password = password
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
