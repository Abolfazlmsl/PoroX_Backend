import csv

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.http import HttpResponse
from django.utils.translation import gettext as _

from core import models
from .models import License


class UserAdmin(UserAdminBase):
    ordering = ['id']
    list_display = ['phone_number', 'name']
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (
            _('Personal Info'),
            {
                'fields': (
                    'generated_token',
                    'is_verified',
                )
            }
        ),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }
        ),
        (
            _('Important dates'),
            {
                'fields': ('last_login',)
            }
        )
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2')
        }),
    )


class LicenseAdmin(admin.ModelAdmin):
    search_fields = ['email', 'serialNumber', ]
    list_display = ('key', 'email', 'licenseType', 'serialNumber')
    list_filter = ('email', 'licenseType', )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Device)
# admin.site.register(models.License)
admin.site.register(License, LicenseAdmin)
