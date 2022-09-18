from django.urls import path
from .views import (login_view, logout_view , signup , update ,
                    logout_view , detail , change_password , special_view ,
                    create_seller_account , update_seller_account ,
                    create_company_seller , update_company_seller ,
                    callback_gateway_view)

app_name = "account"
urlpatterns = [
    path('login' , login_view , name = 'login'),
    path('logout' , logout_view , name = 'logout'),
    path('singup' , signup , name = 'singup'),
    path('update/<id>' , update , name = 'update_user'),
    path('detail/<id>' , detail , name = 'detail'),
    path('change/<id>' , change_password , name = 'change'),
    path('special' , special_view , name = 'special'),
    path('callback-gateway' , callback_gateway_view , name = 'callback_gateway'),
    path('seller-create' , create_seller_account , name = 'create_seller'),
    path('seller-update/<id>' , update_seller_account , name = 'update_seller'), 
    path('company-create' , create_company_seller , name = 'create'),
    path('company-update/<id>' , update_company_seller , name = 'update'), 
]