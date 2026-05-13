from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=200, blank=True)
    icono = models.CharField(max_length=10, default='🍔', help_text='Emoji para la categoría')
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'nombre']
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    disponible = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False, help_text='Aparece primero en el menú')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-destacado', 'categoria', 'nombre']

    def __str__(self):
        return f"{self.nombre} — ${self.precio:,.0f}"
