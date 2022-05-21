import pytest

from payment.models import Payment


@pytest.mark.django_db
def test_payment_create():
    payment = Payment.objects.create(amount='10000')

    assert payment.amount == '10000'
    assert Payment.objects.count() == 1
