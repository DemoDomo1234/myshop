from django.urls import path
from .views import *

app_name = 'blog'
urlpatterns = [
    path('', home, name='list'),
    path('create', create, name='create'),
    path('update/<id>', update, name='update'), 
    path('delete/<id>', delete, name='delete'),
    path('detail/<id>', detail, name='detail'),
    path('like/<id>', like, name='like'),
    path('saved/<id>', saved, name='saved'),
    path('tag-list/<id>', tag_list, name='tag_list'),
    path('category/<id>', category_list, name='category_list'),

]