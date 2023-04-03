from django.contrib import admin
from .models import Blog, Nums

class BlogAdmin(admin.ModelAdmin):
    list_display = ("titel", "author")
    list_filter = ("time" , "author")
    search_fields = ("titel" , "author", "body")

admin.site.register(Blog, BlogAdmin)
admin.site.register(Nums)