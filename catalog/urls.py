from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import (ProductListView, ProductDetailView, ContactsTemplateView, ProductCreateView, \
                           ProductDeleteView, ProductUpdateView, CategoryListView)

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path("contact/", cache_page(60)(ContactsTemplateView.as_view()), name="contacts"),
    path("products/<int:pk>/", cache_page(60)(ProductDetailView.as_view()), name="product_detail"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/edit/<int:pk>/", ProductUpdateView.as_view(), name="product_edit"),
    path("products/delete/<int:pk>", ProductDeleteView.as_view(), name="product_delete"),
    path('catalog/category/', CategoryListView.as_view(), name='categories_list'),
]
