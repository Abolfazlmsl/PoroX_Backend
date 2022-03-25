from django.shortcuts import render, get_object_or_404, redirect
from payment.models import Payment
from core.models import License
from django.views.decorators.csrf import csrf_exempt
from decouple import config
from idpay.api import IDPayAPI

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl

import uuid
import datetime


def getExpiredDate(time):
    date = datetime.datetime.now() + datetime.timedelta(int(time))
    return date.strftime('%Y-%m-%d')

def payment_init():
    base_url = config('BASE_URL', default='http://127.0.0.1:8000/', cast=str)
    api_key = config('IDPAY_API_KEY', default='73292c3b-231c-471e-a8cd-cd5d7d13effe', cast=str)
    sandbox = config('IDPAY_SANDBOX', default=True, cast=bool)

    return IDPayAPI(api_key, base_url, sandbox)


def payment_start(request):
    if request.method == 'POST':
        order_id = uuid.uuid1()
        amount = request.POST.get('amount')

        payer = {
            'name': request.POST.get('name'),
            'phone': request.POST.get('phone'),
            'mail': request.POST.get('email'),
            # 'desc': request.POST.get('desc'),
        }

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        deviceNumber = request.POST.get('deviceUsers')
        time = request.POST.get('time')
        time = getExpiredDate(time)

        record = Payment(order_id=order_id, amount=int(amount), name=name, phone=phone,
                         email=email, deviceNumber=deviceNumber, time=time)
        record.save()

        idpay_payment = payment_init()
        # result = idpay_payment.payment(str(order_id), amount, 'products/success/', payer)
        result = idpay_payment.payment(str(order_id), amount, 'idpay/payment/return', payer)

        if 'id' in result:
            record.status = 1
            record.payment_id = result['id']
            record.save()

            return redirect(result['link'])

        else:
            txt = result['message']
    else:
        txt = "Bad Request"

    return render(request, 'products/lastPage.html')


@csrf_exempt
def payment_return(request):
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

        if Payment.objects.filter(order_id=order_id, payment_id=pid, amount=amount, status=1).count() == 1:

            idpay_payment = payment_init()

            payment = Payment.objects.get(payment_id=pid, amount=amount)
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

                    # Generate license
                    newLicense = License(expired_on=payment.time, deviceNumber=payment.deviceNumber,
                                         licenseType="time limit", email=payment.email, serialNumber=payment.order_id)
                    newLicense.save()

                    # Send email to user
                    serial = payment.order_id
                    key = newLicense.key
                    message = "Thank you for purchasing the PoroX software license"
                    msg = MIMEMultipart()

                    password = "Porox@Sharif1" #"3@#abmsl@"
                    msg['From'] = "reza.shams@digitalrockphysics.ir" #"poroxsoftware@gmail.com"
                    msg['To'] = email
                    msg['Subject'] = "PoroX license"

                    message = message + "\nYour license key: " + key + "\nYour serial number: " + serial
                    msg.attach( MIMEText(message, 'plain') )

                    context = ssl.create_default_context()
                    server = smtplib.SMTP_SSL(host='mail.digitalrockphysics.ir', port=465, context=context)

                    server.login(msg['From'], password)

                    server.sendmail(msg['From'], msg['To'], msg.as_string())

                    server.quit()

                    # return render(request, 'error.html', {'txt': result['message']})
                    return render(request, 'products/lastPage.html', context=context)

                else:
                    txt = result['message']

            else:
                txt = "Error Code : " + str(status) + "   |   " + "Description : " + idpay_payment.get_status(status)

        else:
            txt = "Order Not Found"

    else:
        txt = "Bad Request"

    return render(request, 'products/lastPage.html', context=context)


def payment_check(request, pk):

    payment = Payment.objects.get(pk=pk)

    idpay_payment = payment_init()
    result = idpay_payment.inquiry(payment.payment_id, payment.order_id)

    if 'status' in result:

        payment.status = result['status']
        payment.idpay_track_id = result['track_id']
        payment.bank_track_id = result['payment']['track_id']
        payment.card_number = result['payment']['card_no']
        payment.date = str(result['date'])
        payment.save()

    return render(request, 'error.html', {'txt': result['message']})


def requirement(request):
    txt = "pip install idpay"

    return render(request, 'error.html', {'txt': txt})


def about_me(request):
    txt = 'IDPay'

    return render(request, 'error.html', {'txt': txt})
