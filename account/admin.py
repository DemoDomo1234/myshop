from django.contrib import admin
from .models import User

class User_Admin(admin.ModelAdmin):
    list_display = ("name", "usename")
    list_filter = ("email" , "username" , "number" )
    search_fields = ("username" , "name" , "familie")

admin.site.register(User )

