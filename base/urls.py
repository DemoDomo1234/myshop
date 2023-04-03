from django.urls import path
from .views import *

app_name = 'base'

urlpatterns = [
    path('create-list', create_list, name='create_list'),
    path('update-list/<id>', update_list, name='update_list'), 
    path('delete-list/<id>', delete_list, name='delete_list'),
    path('notifications/<id>', notifications , name='notifications'),
    path('list/<id>', list_view, name='lists'),
    path('unlist/<id>' , unlist_view , name = 'unlist'),
    path('list-detail/<id>', detail_list, name='detail_list'),
    path('create-images/<id>', create_image, name='create_image'),
    path('update-images/<id>', update_image, name='update_image'), 
    path('delete-images/<id>', delete_image, name='delete_image'),
    path('create-category', create_category, name='create_category'),
    path('category/<id>', category_list, name='category_list'),
]