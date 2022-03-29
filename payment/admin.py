from django.contrib import admin
from payment.models import Payment

class PaymentAdmin(admin.ModelAdmin):
    search_fields = ['email', 'order_id', ]
    list_display = ('name', 'email', 'phone', 'status')
    list_filter = ('name', 'email', 'phone', )
    
admin.site.register(Payment, PaymentAdmin)
