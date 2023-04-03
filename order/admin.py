from django.contrib import admin
from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ("date", "user")
    list_filter = ("date", "user")
    search_fields = ("user",)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)

