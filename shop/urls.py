from django.contrib import admin
from django.urls import path , include 
from django.conf import settings
from django.conf.urls.static import static
from azbankgateways.urls import az_bank_gateways_urls

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('prodact.urls', namespace='prodact')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('account/', include('account.urls', namespace='account')),
    path('coment/', include('coment.urls', namespace='coment')),
    path('order/', include('order.urls', namespace='order')),
    path('seller/', include('seller.urls', namespace='seller')),
    path('address/', include('address.urls', namespace='address')),
    path('base/', include('base.urls', namespace='base')),
    path('mdeditor/', include('mdeditor.urls')),
    path('bankgateways/', az_bank_gateways_urls()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
