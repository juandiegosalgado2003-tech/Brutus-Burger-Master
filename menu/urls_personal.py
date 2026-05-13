from django.urls import path
from . import views

urlpatterns = [
    path('', views.carta_lista, name='carta_lista'),
    path('producto/nuevo/', views.producto_crear, name='producto_crear'),
    path('producto/<int:pk>/editar/', views.producto_editar, name='producto_editar'),
    path('producto/<int:pk>/eliminar/', views.producto_eliminar, name='producto_eliminar'),
    path('categoria/nueva/', views.categoria_crear, name='categoria_crear'),
    path('categoria/<int:pk>/editar/', views.categoria_editar, name='categoria_editar'),
]
