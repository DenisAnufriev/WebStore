from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, UpdateView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, ContactsInfo, Version


class ProductListView(ListView):
    model = Product
    ordering = ['-created_at']


class ProductDetailView(DetailView):
    model = Product


class ContactsTemplateView(TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contacts_info"] = ContactsInfo.objects.first()
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")  # переделать

    def get_context_data(self, **kwargs):
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
        context = self.get_context_data()
        formset = context["formset"]
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")

    def get_context_data(self, **kwargs):
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
        context = self.get_context_data()
        formset = context["formset"]

        # Сначала проверяем валидность форм
        if not formset.is_valid():
            return self.form_invalid(form)

        active_versions = [
            version_form for version_form in formset if version_form.cleaned_data.get("is_active", False)
        ]

        # Проверка: должно быть не больше одной активной версии
        if len(active_versions) > 1:
            form.add_error(None, "У продукта не может быть более одной активной версии.")

        # Проверка: если версия активна, у неё должно быть указано название версии
        for version_form in active_versions:
            version_name = version_form.cleaned_data.get("version_name", "").strip()
            if not version_name:
                # Добавляем ошибку к полю version_name, если название не указано
                version_form.add_error('version_name', "Необходимо ввести название версии для активной версии.")

        # Проверяем наличие ошибок после всех проверок
        if form.errors or any(version_form.errors for version_form in formset.forms):
            return self.form_invalid(form)

        # Сохраняем объект и формсет
        self.object = form.save()
        formset.instance = self.object
        formset.save()

        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:home")

# to delete

# def home(request):
#     products = Product.objects.all().order_by("-created_at")
#     context = {"products": products}
#     return render(request, 'catalog/product_list.html', context)

# def contacts(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#
#         print(f'You have new message from {name}({phone}): {message}')
#     return render(request, 'catalog/contacts.html')

# def product_list(request):
#     products = Product.object.all()
#     context = {"products": products}
#     return render(request, 'product_list.html', context)


# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     context = {"product": product}
#     return render(request, 'catalog/product_detail.html', context)
