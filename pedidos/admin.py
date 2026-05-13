from django.contrib import admin
from .models import Pedido, DetallePedido

class DetalleInline(admin.TabularInline):
    model = DetallePedido
    extra = 0

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'cliente_nombre', 'metodo_pago', 'estado', 'total', 'fecha_creacion']
    list_filter = ['estado', 'metodo_pago']
    inlines = [DetalleInline]
