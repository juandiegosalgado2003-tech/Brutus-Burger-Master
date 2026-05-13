from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_personal, name='panel_personal'),
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('pedidos/<int:pk>/', views.detalle_pedido, name='detalle_pedido'),
]
