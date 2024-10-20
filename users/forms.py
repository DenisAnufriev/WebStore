from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма регистрации пользователя, наследующая функционал UserCreationForm
    и применяющая стиль из StyleFormMixin.
    """

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """
    Форма для изменения профиля пользователя, наследующая функционал UserChangeForm
    и применяющая стиль из StyleFormMixin.
    """

    class Meta:
        model = User
        fields = (
            "email",
            "phone",
            "country",
            "avatar",
        )

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы, скрывающая поле для пароля.

        :param args: Позиционные аргументы.
        :param kwargs: Именованные аргументы.
        """
        super().__init__(*args, **kwargs)

        self.fields["password"].widget = forms.HiddenInput()
