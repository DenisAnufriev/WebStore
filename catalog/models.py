from decimal import Decimal

from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование категории',
                            help_text='Введите наименование категории')
    description = models.TextField(verbose_name='Описание категории', help_text='Введите описание категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ["name"]


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование товара', help_text='Введите наименование товара')
    description = models.TextField(verbose_name='Описание товара', help_text='Введите описание товара')
    photo = models.ImageField(upload_to='catalog/photo', **NULLABLE, verbose_name='Фото',
                              help_text='Загрузите фото товара')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Категория',
                                 help_text='Введите категорию товара',
                                 **NULLABLE, related_name='Товары')
    # price = models.IntegerField(verbose_name='Цена за покупку', help_text='Укажите цену за покупку', **NULLABLE)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text='Укажите цену за покупку',
        verbose_name="Цена за покупку",
    )
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания', help_text='Укажите дату создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата последнего изменения',
                                  help_text='Укажите дату изменения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ["name", "-price", "created_at", "-updated_at"]


class ContactsInfo(models.Model):
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    email = models.EmailField(verbose_name="Почта")
    address = models.TextField(verbose_name="Адрес")

    def __str__(self):
        return f"{self.phone}" f"{self.email}" f"{self.address}"

    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактные информации"
