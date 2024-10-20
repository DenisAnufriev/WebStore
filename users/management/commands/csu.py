from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User.objects.create(email="admin@examlpe.com")
        user.set_password("123qwe")
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()


# class Command(BaseCommand):
#     def handle(self, *args, **kwargs):
#         user = User.objects.create(email="moderator@examlpe.com")
#         user.set_password("123qwe")
#         user.is_active = True
#         user.is_staff = False
#         user.is_superuser = False
#         user.save()