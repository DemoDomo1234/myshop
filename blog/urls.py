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
    path('shop/<id>' , shop , name = 'shop'),
    path('unshop/<id>' , unshop , name = 'unshop'),
    path('order' , order , name = 'order'),
    path('send' , send_email , name='send'),
    path('create-list' , create_list , name = 'create_list'),
    path('update-list/<id>' , update_list , name = 'update_list'), 
    path('delete-list/<id>' , delete_list , name = 'delete_list'),
    path('notifications/<id>' , notifications , name = 'notifications'),
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
    path('tag-list/<id>' , tag_list , name='tag_list'),
    path('brand-list/<id>' , brand_list , name='brand_list'),
    path('pdf/<id>' , order_pdf , name='pdf'),
    path('order-detail/<id>' , order_detail , name='order_detail'),
    path('sellers/<id>' , sellers , name='sellers'),
    path('sellers-update/<id>' , sellers_update , name='sellers_update'),
    path('sellers-delete/<id>' , sellers_delete , name='sellers_delete'),
    path('color-num/<id>' , color_num , name='color_num'),
    path('color-num-update/<id>' , color_num_update , name='color_num_update'),
    path('color-num-delete/<id>' , color_num_delete , name='color_num_delete'),
    path('go-to-gateway' , go_to_gateway_view , name = 'go_to_gateway'),
    path('callback-gateway' , callback_gateway_view , name = 'callback_gateway'),
    path('item-update/<id>' , item_update , name = 'item_update'),
    path('select-seller' , select_seller , name = 'select'),
    path('inter-num' , inter_num , name = 'inter'),



]