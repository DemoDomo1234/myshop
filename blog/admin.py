from django.contrib import admin
from .models import *


class BlogAdmin(admin.ModelAdmin):
    list_display = ("titel", "seller")
    list_filter = ("time" , "seller" , "price" )
    search_fields = ("titel" , "seller" , "body")

admin.site.register(Blog , BlogAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ("date", "user")
    list_filter = ("date" , "user")
    search_fields = ("user" ,)

admin.site.register(Order , OrderAdmin)

class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "name")
    list_filter = ("user" , "name" , "number" )
    search_fields = ("user" , "name")

admin.site.register(Address , AddressAdmin)

admin.site.register(Images)
admin.site.register(Colors)
admin.site.register(Sizes)
admin.site.register(Notifications)
admin.site.register(List)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Nums)
admin.site.register(Brand)
admin.site.register(ColorNum)
admin.site.register(Advertising)
