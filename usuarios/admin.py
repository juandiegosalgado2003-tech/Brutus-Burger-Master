from django.contrib import admin
from .models import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'intentos_fallidos', 'bloqueado', 'bloqueado_hasta']
    list_editable = ['bloqueado']
    actions = ['desbloquear']

    def desbloquear(self, request, queryset):
        queryset.update(bloqueado=False, intentos_fallidos=0, bloqueado_hasta=None)
    desbloquear.short_description = 'Desbloquear cuentas seleccionadas'
