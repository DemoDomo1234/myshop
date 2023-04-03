from django.urls import path
from .views import (login_view, logout_view, signup, update,
                    logout_view, detail, change_password,
                    special_view, callback_gateway_view)

app_name = "account"
urlpatterns = [
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('singup', signup, name='singup'),
    path('update/<id>', update, name='update_user'),
    path('detail/<id>', detail, name='detail'),
    path('change/<id>', change_password, name='change'),
    path('special', special_view, name='special'),
    path('callback-gateway', callback_gateway_view, name='callback_gateway'),

]