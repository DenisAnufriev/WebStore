from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView

from catalog.models import Product, ContactsInfo


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
