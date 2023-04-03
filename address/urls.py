from django.urls import path
from .views import *

app_name = 'address'

urlpatterns = [
    path('add-address', add_address, name='add_address'),
    path('update-address/<id>', update_address, name='update_address'),
    path('delete-address/<id>', delete_address, name='delete_address'),
]