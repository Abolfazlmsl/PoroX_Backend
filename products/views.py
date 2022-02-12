from django.shortcuts import render

from .models import Product


def main_products(request):
    products = Product.objects.all().order_by('time').order_by('deviceUsers')
    context = {
        'products': products,
    }
    return render(request, 'products/index.html', context=context)


def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    context = {
        'product': product
    }
    return render(request, 'products/purchase.html', context)
