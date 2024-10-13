from django.forms import ValidationError, BooleanField, ModelForm

from catalog.models import Product, Version


class StyleFormMixin:
    """
    Миксин для установки стилей для полей форм.

    При инициализации добавляет классы CSS к полям формы:
    - 'form-check-input' для полей типа BooleanField
    - 'form-control' для остальных полей
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for (
            field_name,
            field,
        ) in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ProductForm(StyleFormMixin, ModelForm):
    """
    Форма для создания и редактирования продукта.

    Проверяет наличие запрещенных слов в названии и описании продукта.
    """

    forbidden_words = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    class Meta:
        model = Product
        fields = "__all__"

    def clean_name(self):
        """
        Проверяет, что название продукта не содержит запрещенные слова.

        :return: Чистое название продукта.
        :raises ValidationError: Если в названии содержатся запрещенные слова.
        """
        name = self.cleaned_data.get("name")
        if any(word in name.lower() for word in self.forbidden_words):
            raise ValidationError(
                "Название товара не должно содержать запрещенные слова"
            )
        return name

    def clean_description(self):
        """
        Проверяет, что описание продукта не содержит запрещенные слова.

        :return: Чистое описание продукта.
        :raises ValidationError: Если в описании содержатся запрещенные слова.
        """
        description = self.cleaned_data.get("description")
        if any(word in description.lower() for word in self.forbidden_words):
            raise ValidationError("Описание не должно содержать запрещенные слова")
        return description


class VersionForm(StyleFormMixin, ModelForm):
    """
    Форма для создания и редактирования версии продукта.
    """

    class Meta:
        model = Version
        fields = "__all__"
