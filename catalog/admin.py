from django.contrib import admin

from blog.models import Article
from catalog.models import Product, Category, ContactsInfo


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # list_display = ('id', 'name', 'price', 'description', 'category', 'photo', 'created_at', 'updated_at')
    list_display = ('id', 'name', 'price', 'description', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(ContactsInfo)
class ContactsInfoAdmin(admin.ModelAdmin):
    list_display = ("phone", "email", "address")

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "content", "created_at", "is_published", "slug")
    list_filter = ("created_at", "is_published")
    search_fields = ("title", "content")
