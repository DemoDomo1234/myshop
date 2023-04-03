from django.contrib import admin
from .models import Prodact, Nums


class ProdactAdmin(admin.ModelAdmin):
    list_display = ("titel", "seller")
    list_filter = ("time", "seller")
    search_fields = ("titel", "seller", "body")


admin.site.register(Prodact, ProdactAdmin)

admin.site.register(Nums)



