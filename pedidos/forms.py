from django import forms
from .models import Pedido, DetallePedido
from menu.models import Producto
from mesas.models import Mesa

class PedidoClienteForm(forms.ModelForm):
    """Formulario que llena el cliente al hacer su pedido"""
    class Meta:
        model = Pedido
        fields = ['cliente_nombre', 'cliente_telefono', 'mesa', 'metodo_pago',
                  'tarjeta_numero', 'tarjeta_tipo', 'notas']
        widgets = {
            'cliente_nombre': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Tu nombre completo', 'required': True
            }),
            'cliente_telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono (opcional)'
            }),
            'mesa': forms.Select(attrs={'class': 'form-select'}),
            'metodo_pago': forms.RadioSelect(),
            'tarjeta_numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Últimos 4 dígitos',
                'maxlength': '4'
            }),
            'tarjeta_tipo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Visa, Mastercard...'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Sin cebolla, extra salsa... (opcional)'
            }),
        }
        labels = {
            'cliente_nombre': 'Tu nombre',
            'cliente_telefono': 'Teléfono',
            'mesa': 'Mesa (opcional)',
            'metodo_pago': 'Método de pago',
            'tarjeta_numero': 'Últimos 4 dígitos de la tarjeta',
            'tarjeta_tipo': 'Tipo de tarjeta',
            'notas': 'Instrucciones especiales',
        }

class EstadoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['estado']
        widgets = {'estado': forms.Select(attrs={'class': 'form-select'})}
