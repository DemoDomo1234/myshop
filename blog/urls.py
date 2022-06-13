from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('' , home , name = 'list'),
    path('create' , create , name = 'create'),
    path('update/<id>' , update , name = 'update'), 
    path('delete/<id>' , delete , name = 'delete'),
    path('detail/<id>' , detail , name = 'detail'),
    path('like/<id>' , like , name = 'like'),
    path('unlike/<id>' , unlike , name = 'unlike'),
    path('shop/<id>' , shop , name = 'shop'),
    path('unshop/<id>' , unshop , name = 'unshop'),
    path('cart' , cart , name = 'cart'),
    path('send' , send_email , name='send'),
    path('create-list' , create_list , name = 'create_list'),
    path('update-list/<id>' , update_list , name = 'update_list'), 
    path('delete-list/<id>' , delete_list , name = 'delete_list'),
    path('notifications/<id>' , notifications , name = 'notifications'),
    path('un-notifications/<id>' , un_notifications , name = 'un_notifications'),
    path('list/<id>' , list_view , name = 'lists'),
    path('unlist/<id>' , unlist_view , name = 'unlist'),
    path('list-detail/<id>' , detail_list , name = 'detail_list'),
    path('share/<id>' , share_post , name='share'),
    path('add-address' , add_address , name = 'add_address'),
    path('update-address/<id>' , update_address , name = 'update_address'),
    path('delete-address/<id>' , delete_address , name = 'delete_address'),
    path('create-images/<id>' , create_image , name = 'create_image'),
    path('update-images/<id>' , update_image , name = 'update_image'), 
    path('delete-images/<id>' , delete_image , name = 'delete_image'),
    path('create-category' , create_category , name = 'create_category'),
    path('category/<id>' , category_list , name = 'category_list'),
    path('pdf/<id>' , order_pdf , name='pdf'),
    path('order-detail/<id>' , order_detail , name='order_detail'),
    path('crate-image-myblog' , create_image_myblog , name='create_images_myblog'),
]