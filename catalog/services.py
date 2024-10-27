from django.core.cache import cache

from catalog.models import Product, Category
from config.settings import CACHE_ENABLED

def get_product_from_cache():
    """
    Получает данные по продуктам из кэша, если кэш пуст, получает данные из БД.
    :return:
    """
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = "product_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products

def get_categories_from_cache():
    if not CACHE_ENABLED:
        return Category.objects.all()
    key = 'category_list'
    categories = cache.get(key)
    if categories is not None:
        return categories
    categories = Category.objects.all()
    cache.set(key, categories)
    return categories
