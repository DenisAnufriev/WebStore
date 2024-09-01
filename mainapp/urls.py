from django.urls import path
from mainapp.apps import MainappConfig
from mainapp.views import home, contacts

app_name = MainappConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
]
