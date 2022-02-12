from django.shortcuts import render

from products.models import Product


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
    if request.method == 'POST':
        try:
            name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']
            price = product.price
            userNumbers = product.deviceUsers
            time = product.time
            print(name)
            print(phone)
            print(email)
            print(price)
            print(userNumbers)
            print(time)
        except Exception as e:
            context['error'] = str(e)
        else:
            pass
    return render(request, 'products/purchase.html', context)


def success_purchase(request):
    return render(request, 'products/lastPage.html')
