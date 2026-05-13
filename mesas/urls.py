from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista, name='mesas_lista'),
    path('nueva/', views.crear, name='mesas_crear'),
    path('<int:pk>/editar/', views.editar, name='mesas_editar'),
    path('<int:pk>/toggle/', views.toggle, name='mesas_toggle'),
]
