from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_personal, name='panel_personal'),
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('pedidos/<int:pk>/', views.detalle_pedido, name='detalle_pedido'),
    path('pedidos/eliminar-item/<int:item_id>/', views.eliminar_item_pedido, name='eliminar_item_pedido'),
    path('pedidos/agregar-item/<int:pedido_id>/', views.agregar_item_pedido, name='agregar_item_pedido'),
    path('pedidos/editar-comentario/<int:item_id>/', views.editar_comentario_item, name='editar_comentario_item'),
]
