from django.contrib import admin
from .models import Coments ,ComentsBlog

class ComentsAdmin(admin.ModelAdmin):
    list_display = ("titel", "user" , "body")
    list_filter = ("date" , "titel" , "user" , "body" )
    search_fields = ("titel" , "user" , "body")

admin.site.register(Coments , ComentsAdmin)

class ComentsBlogAdmin(admin.ModelAdmin):
    list_display = ("titel", "user" , "body")
    list_filter = ("date" , "titel" , "user" , "body" )
    search_fields = ("titel" , "user" , "body")

admin.site.register(ComentsBlog , ComentsBlogAdmin)