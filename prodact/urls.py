from django.urls import path
from .views import *

app_name = 'prodact'

urlpatterns = [
    path('', home, name='list'),
    path('create', create, name='create'),
    path('update/<id>', update, name='update'), 
    path('delete/<id>', delete, name='delete'),
    path('detail/<id>', detail, name='detail'),
    path('like/<id>', like, name='like'),
    path('send', send_email, name='send'),
    path('share/<id>', share_post, name='share'),
    path('tag-list/<id>', tag_list, name='tag_list'),
    path('brand-list/<id>', brand_list, name='brand_list'),
]