from django.contrib import admin
from .models import User 


class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "username")
    list_filter = ("email", "username", "number" )
    search_fields = ("username", "name", "familie")

admin.site.register(User, UserAdmin)
