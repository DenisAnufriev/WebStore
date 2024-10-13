import secrets
import string
import random

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http:/{host}/users/email-confirm/{token}'
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке, для подтверждения почты{url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_object_or_404(User, email=email)
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(10))
        user.set_password(password)
        user.save()
        send_mail(
            subject='Сброс пароля',
            message=f' Ваш новый пароль {password}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return redirect(reverse('users:login'))
    return render(request, 'users/reset_password.html')

class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user