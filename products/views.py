from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from decouple import config
from idpay.api import IDPayAPI
from products.models import Product
from payment.models import Main
from core.models import License

import uuid


def main_products(request):
    products = Product.objects.all().order_by('time').order_by('deviceUsers')
    context = {
        'products': products,
    }
    return render(request, 'products/index.html', context=context)


def payment_init():
    base_url = config('BASE_URL', default='http://127.0.0.1:8000/', cast=str)
    api_key = config('IDPAY_API_KEY', default='97ded38e-9a89-488b-b4e9-6d1b5570f93e', cast=str)
    sandbox = config('IDPAY_SANDBOX', default=True, cast=bool)

    return IDPayAPI(api_key, base_url, sandbox)


def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    context = {
        'product': product
    }
    return render(request, 'products/purchase.html', context)


def product_payment(request):
    if request.method == 'POST':
        # try:
        #     name = request.POST['name']
        #     phone = request.POST['phone']
        #     email = request.POST['email']
        #     amount = product.price
        #     userNumbers = product.deviceUsers
        #     time = product.time
        #     print(name)
        #     print(phone)
        #     print(email)
        #     print(amount)
        #     print(userNumbers)
        #     print(time)
        #     return redirect(reverse('payment:payment_start'))
        order_id = uuid.uuid1()
        amount = request.POST.get('amount')

        payer = {
            'name': request.POST.get('name'),
            'phone': request.POST.get('phone'),
            'mail': request.POST.get('email')
            # 'desc': request.POST.get('desc'),
        }

        record = Main(order_id=order_id, amount=int(amount))
        record.save()

        idpay_payment = payment_init()
        result = idpay_payment.payment(str(order_id), amount, 'products/success', payer)
        # result = idpay_payment.payment(str(order_id), amount, 'payment/return', payer)

        if 'id' in result:
            record.status = 1
            record.payment_id = result['id']
            record.save()

            return redirect(result['link'])

        else:
            txt = result['message']
        #     except Exception as e:
        #         context['error'] = str(e)
        #     else:
        #         pass
    return render(request, 'products/lastPage.html')


@csrf_exempt
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
    if request.method == 'POST':

        pid = request.POST.get('id')
        status = request.POST.get('status')
        pidtrack = request.POST.get('track_id')
        order_id = request.POST.get('order_id')
        amount = request.POST.get('amount')
        card = request.POST.get('card_no')
        date = request.POST.get('date')

        context = {
            'order_id': order_id,
            'status': (status == "10")
        }

        if Main.objects.filter(order_id=order_id, payment_id=pid, amount=amount, status=1).count() == 1:

            idpay_payment = payment_init()

            payment = Main.objects.get(payment_id=pid, amount=amount)
            payment.status = status
            payment.date = str(date)
            payment.card_number = card
            payment.idpay_track_id = pidtrack
            payment.save()

            if str(status) == '10':
                result = idpay_payment.verify(pid, payment.order_id)

                if 'status' in result:

                    payment.status = result['status']
                    payment.bank_track_id = result['payment']['track_id']
                    payment.save()

                    # return render(request, 'error.html', {'txt': result['message']})
                    return render(request, 'products/lastPage.html', context=context)

                else:
                    txt = result['message']

            else:
                txt = "Error Code : " + str(status) + "   |   " + "Description : " + idpay_payment.get_status(
                    status)

        else:
            txt = "Order Not Found"

    else:
        txt = "Bad Request"
    return render(request, 'products/lastPage.html', context=context)
