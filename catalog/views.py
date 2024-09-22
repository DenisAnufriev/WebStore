from django.shortcuts import render, get_object_or_404

from catalog.models import Product


def home(request):
    products = Product.objects.all().order_by("-created_at")
    context = {"products": products}
    return render(request, 'product_list.html', context)

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print(f'You have new message from {name}({phone}): {message}')
    return render(request, 'contacts.html')

# def product_list(request):
#     products = Product.object.all()
#     context = {"products": products}
#     return render(request, 'product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, 'product_detail.html', context)

