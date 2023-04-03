from django.urls import path
from .views import *

app_name = 'order'

urlpatterns = [
    path('shop/<id>', shop, name='shop'),
    path('unshop/<id>', unshop, name='unshop'),
    path('order', order, name='order'),
    path('pdf/<id>', order_pdf, name='pdf'),
    path('order-detail/<id>', order_detail, name='order_detail'),
    path('go-to-gateway', go_to_gateway_view, name='go_to_gateway'),
    path('callback-gateway', callback_gateway_view, name='callback_gateway'),
    path('item-update/<id>', item_update, name='item_update'),
    path('select-seller/<id>', select_seller, name='select'),
    path('inter-num/<id>', inter_num, name='inter'),
]