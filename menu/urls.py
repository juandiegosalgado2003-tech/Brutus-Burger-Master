from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_cliente, name='inicio'),
]
