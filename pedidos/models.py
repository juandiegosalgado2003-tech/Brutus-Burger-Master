from django.db import models
from menu.models import Producto
from mesas.models import Mesa

class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_preparacion', 'En preparación'),
        ('listo', 'Listo'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    PAGO = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
    ]

    # Datos del cliente
    cliente_nombre = models.CharField(max_length=100)
    cliente_telefono = models.CharField(max_length=20, blank=True)
    metodo_pago = models.CharField(max_length=20, choices=PAGO, default='efectivo')
    # Tarjeta (solo si paga con tarjeta)
    tarjeta_numero = models.CharField(max_length=4, blank=True, help_text='Últimos 4 dígitos')
    tarjeta_tipo = models.CharField(max_length=20, blank=True, help_text='Visa, Mastercard, etc.')

    mesa = models.ForeignKey(Mesa, on_delete=models.SET_NULL, null=True, blank=True)
    notas = models.TextField(blank=True, help_text='Instrucciones especiales')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Pedido #{self.pk} — {self.cliente_nombre}"

    def calcular_total(self):
        self.total = sum(i.subtotal() for i in self.items.all())
        self.save(update_fields=['total'])


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre}"
