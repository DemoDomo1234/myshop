from django.urls import path
from .views import login_view, logout_view , signup , update , logout_view , detail , change_password

app_name = "account"
urlpatterns = [
    path('login' , login_view , name = 'login'),
    path('logout' , logout_view , name = 'logout'),
    path('singup' , signup , name = 'singup'),
    path('update/<id>' , update , name = 'update'),
    path('detail/<id>' , detail , name = 'detail'),
    path('change/<id>' , change_password , name = 'change'),
]