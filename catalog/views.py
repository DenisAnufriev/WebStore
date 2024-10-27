from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    DeleteView,
    UpdateView,
)

from catalog.forms import ProductForm, VersionForm, ProductModeratorForm, ProductContentManagerForm
from catalog.models import Product, ContactsInfo, Version, Category
from catalog.services import get_product_from_cache, get_categories_from_cache


class ProductListView(ListView):
    """
    Представление для отображения списка продуктов.
    """

    model = Product
    ordering = ["-created_at"]

    def get_queryset(self):
        return get_product_from_cache()


class ProductDetailView(DetailView):
    """
    Представление для отображения деталей продукта.
    """

    model = Product


class ContactsTemplateView(TemplateView):
    """
    Представление для отображения страницы контактов.
    """

    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        """
        Добавляет информацию о контактах в контекст.

        :param kwargs: Дополнительные параметры контекста.
        :return: Обновленный контекст с информацией о контактах.
        """
        context = super().get_context_data(**kwargs)
        context["contacts_info"] = ContactsInfo.objects.first()
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового продукта.
    """

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")  # переделать

    def get_context_data(self, **kwargs):
        """
        Добавляет заголовок и формсет версий в контекст.

        :param kwargs: Дополнительные параметры контекста.
        :return: Обновленный контекст с заголовком и формсетом.
        """
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Создание товара"
        VersionFormset = inlineformset_factory(
            Product, Version, form=VersionForm, extra=1
        )
        if self.request.method == "POST":
            context_data["formset"] = VersionFormset(self.request.POST)
        else:
            context_data["formset"] = VersionFormset()
        return context_data

    def form_valid(self, form):
        """
        Обрабатывает корректные данные формы и сохраняет продукт и связанные версии.

        :param form: Объект формы.
        :return: Ответ после успешного сохранения.
        """
        context = self.get_context_data()
        formset = context["formset"]
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования существующего продукта.
    """

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")

    def get_context_data(self, **kwargs):
        """
        Добавляет заголовок и формсет версий в контекст.

        :param kwargs: Дополнительные параметры контекста.
        :return: Обновленный контекст с заголовком и формсетом.
        """
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Редактирование товара"
        VersionFormset = inlineformset_factory(
            Product, Version, form=VersionForm, extra=1, can_delete=True
        )
        if self.request.method == "POST":
            context_data["formset"] = VersionFormset(
                self.request.POST, instance=self.object
            )
        else:
            context_data["formset"] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        """
        Обрабатывает корректные данные формы и сохраняет обновленный продукт и связанные версии.

        :param form: Объект формы.
        :return: Ответ после успешного сохранения.
        """
        context = self.get_context_data()
        formset = context["formset"]

        # Сначала проверяем валидность форм
        if not formset.is_valid():
            return self.form_invalid(form)

        active_versions = [
            version_form
            for version_form in formset
            if version_form.cleaned_data.get("is_active", False)
        ]

        # Проверка: должно быть не больше одной активной версии
        if len(active_versions) > 1:
            form.add_error(
                None, "У продукта не может быть более одной активной версии."
            )

        # Проверка: если версия активна, у неё должно быть указано название версии
        for version_form in active_versions:
            version_name = version_form.cleaned_data.get("version_name", "").strip()
            if not version_name:
                # Добавляем ошибку к полю version_name, если название не указано
                version_form.add_error(
                    "version_name",
                    "Необходимо ввести название версии для активной версии.",
                )

        # Проверяем наличие ошибок после всех проверок
        if form.errors or any(version_form.errors for version_form in formset.forms):
            return self.form_invalid(form)

        # Сохраняем объект и формсет
        self.object = form.save()
        formset.instance = self.object
        formset.save()

        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user:
            return ProductForm
        if user.has_perm("catalog.set_published") and user.has_perm("catalog.can_edit_description") and user.has_perm(
                "catalog.can_edit_category"):
            return ProductModeratorForm
        if user.has_perm("catalog.set_published"):
            return ProductContentManagerForm
        raise PermissionDenied


class ProductDeleteView(DeleteView):
    """
    Представление для удаления продукта.
    """

    model = Product
    success_url = reverse_lazy("catalog:home")


class CategoryListView(ListView):
    model = Category
    template_name = "catalog/categories_list.html"

    def get_queryset(self):
        return get_categories_from_cache()
