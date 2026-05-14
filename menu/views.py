from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from .models import Producto, Categoria
from .forms import ProductoForm, CategoriaForm

# ── VISTA PÚBLICA (cliente) ──────────────────────────────────────
def inicio_cliente(request):
    categorias = Categoria.objects.prefetch_related('productos').all()
    productos_destacados = Producto.objects.filter(disponible=True, destacado=True)
    return render(request, 'cliente/inicio.html', {
        'categorias': categorias,
        'destacados': productos_destacados,
    })

# ── VISTAS PERSONAL (requiere login) ────────────────────────────
@login_required
@never_cache
def carta_lista(request):
    categorias = Categoria.objects.prefetch_related('productos').all()
    return render(request, 'menu/carta_lista.html', {'categorias': categorias})

@login_required
@never_cache
def producto_crear(request):
    form = ProductoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Producto agregado a la carta.')
        return redirect('carta_lista')
    return render(request, 'menu/producto_form.html', {'form': form, 'titulo': 'Nuevo Producto'})

@login_required
@never_cache
def producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if form.is_valid():
        form.save()
        messages.success(request, 'Producto actualizado.')
        return redirect('carta_lista')
    return render(request, 'menu/producto_form.html', {'form': form, 'titulo': 'Editar Producto', 'producto': producto})

@login_required
@never_cache
def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.warning(request, f'"{producto.nombre}" eliminado.')
        return redirect('carta_lista')
    return render(request, 'menu/confirmar_eliminar.html', {'objeto': producto})

@login_required
@never_cache
def categoria_crear(request):
    form = CategoriaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Categoría creada.')
        return redirect('carta_lista')
    return render(request, 'menu/categoria_form.html', {'form': form})

@login_required
@never_cache
def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if form.is_valid():
        form.save()
        messages.success(request, 'Categoría actualizada.')
        return redirect('carta_lista')
    return render(request, 'menu/categoria_form.html', {'form': form, 'categoria': categoria})

@login_required
@never_cache
def categoria_eliminar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.warning(request, f'Categoría "{categoria.nombre}" eliminada.')
        return redirect('carta_lista')
    return render(request, 'menu/confirmar_eliminar.html', {'objeto': categoria})
