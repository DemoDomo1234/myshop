from django.urls import path
from .views import (
                    create_seller_account, update_seller_account,
                    create_company_seller, update_company_seller
                    )

app_name = "seller"
urlpatterns = [

    path('seller-create', create_seller_account, name='create_seller'),
    path('seller-update/<id>', update_seller_account, name='update_seller'), 
    path('company-create', create_company_seller, name='create'),
    path('company-update/<id>', update_company_seller, name='update'), 
]