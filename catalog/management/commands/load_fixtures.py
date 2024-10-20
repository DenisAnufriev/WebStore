import json

from django.core.management.base import BaseCommand

from blog.models import Article
from catalog.models import Product, Category, ContactsInfo


class Command(BaseCommand):
    """
    Пользовательская команда управления для заполнения базы данных данными из файла фикстуры JSON.
    Команда сначала очищает существующие данные в таблицах Product, Category и ContactsInfo,
    а затем заполняет их данными из файла фикстуры `catalog_data.json`.
    """

    @staticmethod
    def json_read_categories():
        """
        Читает и фильтрует данные категорий из файла фикстуры.

        Returns:
            list: Список словарей, содержащих данные для экземпляров модели Category.
        """
        with open("fixtures/catalog_data.json", encoding="utf-8") as file:
            data = json.load(file)
            return [item for item in data if item["model"] == "catalog.category"]

    @staticmethod
    def json_read_products():
        """
        Читает и фильтрует данные продуктов из файла фикстуры.

        Returns:
            list: Список словарей, содержащих данные для экземпляров модели Product.
        """
        with open("fixtures/catalog_data.json", encoding="utf-8") as file:
            data = json.load(file)
            return [item for item in data if item["model"] == "catalog.product"]

    @staticmethod
    def json_read_contacts_info():
        """
        Читает и фильтрует данные контактной информации из файла фикстуры.

        Returns:
            list: Список словарей, содержащих данные для экземпляров модели ContactsInfo.
        """
        with open("fixtures/catalog_data.json", encoding="utf-8") as file:
            data = json.load(file)
            return [item for item in data if item["model"] == "catalog.contactsinfo"]

    @staticmethod
    def json_read_articles():
        """
        Читает и фильтрует данные статей из файла фикстуры.

        Returns:
            list: Список словарей, содержащих данные для экземпляров модели Article.
        """
        with open("fixtures/blog_data.json", encoding="utf-8") as file:
            data = json.load(file)
            return [item for item in data if item["model"] == "blog.article"]

    def handle(self, *args, **options):
        """
        Основной метод, который обрабатывает выполнение команды.

        - Удаляет все существующие данные из таблиц Product и Category.
        - Читает данные о категориях и продуктах из файла фикстуры.
        - Создает новые экземпляры Category и Product на основе данных из фикстуры.
        - Сохраняет новые экземпляры в базе данных в пакетном режиме.
        """
        Product.objects.all().delete()
        Category.objects.all().delete()
        ContactsInfo.objects.all().delete()
        Article.objects.all().delete()

        categories_for_create = []
        for item in Command.json_read_categories():
            category_data = item["fields"]
            categories_for_create.append(Category(id=item["pk"], **category_data))
        Category.objects.bulk_create(categories_for_create)

        products_for_create = []
        for item in Command.json_read_products():
            product_data = item["fields"]
            category = Category.objects.get(pk=product_data.pop("category"))
            products_for_create.append(
                Product(id=item["pk"], category=category, **product_data)
            )
        Product.objects.bulk_create(products_for_create)

        contacts_info_for_create = []
        for item in Command.json_read_contacts_info():
            contacts_data = item["fields"]
            contacts_info_for_create.append(
                ContactsInfo(id=item["pk"], **contacts_data)
            )
        ContactsInfo.objects.bulk_create(contacts_info_for_create)

        articles_for_create = []
        for item in Command.json_read_articles():
            article_data = item["fields"]
            articles_for_create.append(Article(id=item["pk"], **article_data))
        Article.objects.bulk_create(articles_for_create)
