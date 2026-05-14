from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('menu.urls')),
    path('hacer-pedido/', include('pedidos.urls_cliente')),
    path('personal/', include('pedidos.urls')),
    path('personal/mesas/', include('mesas.urls')),
    path('personal/reportes/', include('reportes.urls')),
    path('personal/carta/', include('menu.urls_personal')),
    path('usuarios/', include('usuarios.urls')),
    # Servir media files en producción
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
