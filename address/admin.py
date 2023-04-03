from django.contrib import admin
from .models import Address


class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "name")
    list_filter = ("user", "name", "number")
    search_fields = ("user", "name")

admin.site.register(Address , AddressAdmin)

