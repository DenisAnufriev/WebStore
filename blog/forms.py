from django import forms

from blog.models import Article


class ArticleUpdateForm(forms.ModelForm):
    """
        Форма для обновления статьи.

        Эта форма позволяет редактировать поля статьи, такие как заголовок, содержимое,
        фотография и статус публикации.
        """
    class Meta:
        model = Article
        fields = ["title", "content", "photo", "is_published"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите заголовок статьи",
                    "required": "required",
                    "id": "title",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 10,
                    "placeholder": "Введите содержимое статьи",
                    "required": "required",
                    "id": "content",
                }
            ),
            "photo": forms.ClearableFileInput(
                attrs={"class": "form-control", "id": "preview"}
            ),
            "is_published": forms.CheckboxInput(
                attrs={"class": "form-check-input", "id": "is_published"}
            ),
        }
