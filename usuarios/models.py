from django.db import models
from django.contrib.auth.models import User
import random, string

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    intentos_fallidos = models.IntegerField(default=0)
    bloqueado = models.BooleanField(default=False)
    bloqueado_hasta = models.DateTimeField(null=True, blank=True)
    codigo_2fa = models.CharField(max_length=6, blank=True)
    codigo_2fa_expira = models.DateTimeField(null=True, blank=True)
    codigo_2fa_usado = models.BooleanField(default=True)

    def generar_codigo_2fa(self):
        self.codigo_2fa = ''.join(random.choices(string.digits, k=6))
        from django.utils import timezone
        from datetime import timedelta
        self.codigo_2fa_expira = timezone.now() + timedelta(minutes=5)
        self.codigo_2fa_usado = False
        self.save()
        return self.codigo_2fa

    def __str__(self):
        return f"Perfil de {self.usuario.username}"
