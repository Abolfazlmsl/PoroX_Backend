from django.shortcuts import render

from products.models import Product
from core.models import License


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
    # if request.method == 'Get':
    #     if request.response == "200":
    #         name = request.GET['name']
    #         phone = request.GET['phone']
    #         email = request.GET['email']
    #         # price = product.price --> request.GET['price']
    #         # userNumbers = product.deviceUsers
    #         # time = product.time
    #         license = License.objects.create(expired_on=55, email="", deviceNumber=1, licenseType="time limit",
    #                                          serialNumber=466)
    #     except Exception as e:
    #         context['error'] = str(e)
    #     else:
    #         return HttpResponseRedirect(reverse('products:ticket_details', kwargs={'ticket_id': ticket.id}))
    return render(request, 'products/lastPage.html')
