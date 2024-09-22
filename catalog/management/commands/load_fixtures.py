import json

from django.core.management.base import BaseCommand

from blog.models import Article
from catalog.models import Product, Category, ContactsInfo


class Command(BaseCommand):
    """
    Custom management command to populate the database with data from a JSON fixtures file.
    The command will first clear existing data from the Product, Category, and ContactInfo tables,
    and then repopulate them with the data from the fixtures file `catalog_data.json`.
    """

    @staticmethod
    def json_read_categories():
        """
        Reads and filters category data from the fixtures file.

        Returns:
            list: A list of dictionaries containing data for Category model instances.
        """
        with open("fixtures/catalog_data.json", encoding="utf-8") as file:
            data = json.load(file)
            return [item for item in data if item["model"] == "catalog.category"]

    @staticmethod
    def json_read_products():
        """
        Reads and filters product data from the fixtures file.

        Returns:
            list: A list of dictionaries containing data for Product model instances.
        """
        with open("fixtures/catalog_data.json", encoding="utf-8") as file:
            data = json.load(file)
            return [item for item in data if item["model"] == "catalog.product"]

    @staticmethod
    def json_read_contacts_info():
        with open("fixtures/catalog_data.json", encoding="utf-8") as file:
            data = json.load(file)
            return [item for item in data if item["model"] == "catalog.contactsinfo"]

    @staticmethod
    def json_read_articles():
        with open("fixtures/blog_data.json", encoding="utf-8") as file:
            data = json.load(file)
            return [item for item in data if item["model"] == "blog.article"]

    def handle(self, *args, **options):
        """
        Main method that handles the execution of the command.

        - Deletes all existing data from the Product, Category tables.
        - Reads category, product information data from the fixtures file.
        - Creates new instances of Category, Product based on the fixtures data.
        - Saves the new instances in bulk to the database.
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
            contacts_info_for_create.append(ContactsInfo(id=item["pk"], **contacts_data))
        ContactsInfo.objects.bulk_create(contacts_info_for_create)

        articles_for_create = []
        for item in Command.json_read_articles():
            article_data = item["fields"]
            articles_for_create.append(Article(id=item["pk"], **article_data))
        Article.objects.bulk_create(articles_for_create)
