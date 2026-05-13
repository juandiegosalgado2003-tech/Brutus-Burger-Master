from django.db import models

class Mesa(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    capacidad = models.PositiveIntegerField(default=4)
    disponible = models.BooleanField(default=True)

    class Meta:
        ordering = ['numero']

    def __str__(self):
        return f"Mesa {self.numero}"
