from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django import forms
from .models import Mesa

class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['numero', 'capacidad', 'disponible']
        widgets = {
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

@login_required
@never_cache
def lista(request):
    mesas = Mesa.objects.all()
    return render(request, 'mesas/lista.html', {'mesas': mesas})

@login_required
@never_cache
def crear(request):
    form = MesaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Mesa creada.')
        return redirect('mesas_lista')
    return render(request, 'mesas/form.html', {'form': form, 'titulo': 'Nueva Mesa'})

@login_required
@never_cache
def editar(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    form = MesaForm(request.POST or None, instance=mesa)
    if form.is_valid():
        form.save()
        messages.success(request, 'Mesa actualizada.')
        return redirect('mesas_lista')
    return render(request, 'mesas/form.html', {'form': form, 'titulo': f'Editar Mesa {mesa.numero}'})

@login_required
@never_cache
def toggle(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    mesa.disponible = not mesa.disponible
    mesa.save()
    return redirect('mesas_lista')
