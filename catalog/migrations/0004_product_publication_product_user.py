# Generated by Django 4.2.2 on 2024-10-13 19:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalog", "0003_version"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="publication",
            field=models.BooleanField(
                default=False,
                help_text="продукт опубликован",
                verbose_name="признак публикации продукта",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="user",
            field=models.ForeignKey(
                blank=True,
                help_text="Укажите пользователя",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
    ]
