from django.contrib import admin
from django.urls import path , include 
from django.conf import settings
from django.conf.urls.static import static
from azbankgateways.urls import az_bank_gateways_urls

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('blog.urls')),
    path('appblog/' , include('appblog.urls')),
    path('account/' , include('account.urls')),
    path('coment/' , include('coment.urls')),
    path('mdeditor/', include('mdeditor.urls')),
    path('bankgateways/', az_bank_gateways_urls()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
