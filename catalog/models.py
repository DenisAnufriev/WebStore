from decimal import Decimal

from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Category(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Наименование категории",
        help_text="Введите наименование категории",
    )
    description = models.TextField(
        verbose_name="Описание категории", help_text="Введите описание категории"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


class Product(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Наименование товара",
        help_text="Введите наименование товара",
    )
    description = models.TextField(
        verbose_name="Описание товара", help_text="Введите описание товара"
    )
    photo = models.ImageField(
        upload_to="catalog/photo",
        **NULLABLE,
        verbose_name="Фото",
        help_text="Загрузите фото товара",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Введите категорию товара",
        **NULLABLE,
        related_name="Товары",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Укажите цену за покупку",
        verbose_name="Цена за покупку",
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Укажите дату создания",
    )
    updated_at = models.DateField(
        auto_now=True,
        verbose_name="Дата последнего изменения",
        help_text="Укажите дату изменения",
    )
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
        **NULLABLE,
        on_delete=models.SET_NULL,
    )
    publication = models.BooleanField(
        default=False,
        verbose_name="признак публикации продукта",
        help_text="продукт опубликован",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name", "-price", "created_at", "-updated_at"]
        permissions = [
            ('set_published', 'Can publish products'),
            ("can_edit_category", "Can edit category"),
            ("can_edit_description", "Can edit description")
        ]


class ContactsInfo(models.Model):
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    email = models.EmailField(verbose_name="Почта")
    address = models.TextField(verbose_name="Адрес")

    def __str__(self):
        return f"{self.phone}" f"{self.email}" f"{self.address}"

    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактные информации"


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    version_number = models.CharField(max_length=50, verbose_name="Номер версии")
    version_name = models.CharField(max_length=100, verbose_name="Название версии")
    is_active = models.BooleanField(default=False, verbose_name="Активность версии")

    def __str__(self):
        return f"{self.version_name} - ({self.version_number})"

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
