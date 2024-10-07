from django.forms import ValidationError, BooleanField, ModelForm

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field, in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, ModelForm):
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
        name = self.cleaned_data.get("name")
        if any(word in name.lower() for word in self.forbidden_words):
            raise ValidationError(
                "Название товара не должно содержать запрещенные слова"
            )
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if any(word in description.lower() for word in self.forbidden_words):
            raise ValidationError("Описание не должно содержать запрещенные слова")
        return description


class VersionForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Version
        fields = "__all__"
