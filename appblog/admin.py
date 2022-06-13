from django.contrib import admin
from .models import MyBlog , Nums

class MyBlog_Admin(admin.ModelAdmin):
    list_display = ("titel", "author")
    list_filter = ("time" , "author")
    search_fields = ("titel" , "author" , "body")

admin.site.register(MyBlog , MyBlog_Admin)
admin.site.register(Nums)