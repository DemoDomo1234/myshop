from django.urls import path
from .views import *
app_name = 'coment'
urlpatterns = [
    path('update/<id>' , update , name = 'update'), 
    path('delete/<id>' , delete , name = 'delete'),
    path('likes/<id>' , likes , name = 'likes'),
    path('unlikes/<id>' , unlikes , name = 'unlikes'),
    path('blog-update/<id>' , blog_update , name = 'blog_update'), 
    path('blog-delete/<id>' , blog_delete , name = 'blog_delete'),
    path('blog-likes/<id>' , blog_likes , name = 'blog_likes'),
    path('blog-unlikes/<id>' , blog_unlikes , name = 'blog_unlikes'),
]
