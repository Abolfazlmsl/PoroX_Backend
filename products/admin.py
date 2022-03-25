from django.contrib import admin
from products.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('price', 'deviceUsers', 'time', )
    list_filter = ('price', 'deviceUsers', 'time', )


admin.site.register(Product, ProductAdmin)
