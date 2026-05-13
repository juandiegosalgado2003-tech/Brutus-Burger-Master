from django.urls import path
from . import views

urlpatterns = [
    path('', views.hacer_pedido, name='hacer_pedido'),
    path('confirmado/<int:pk>/', views.pedido_confirmado, name='pedido_confirmado'),
]
