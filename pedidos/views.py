import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Pedido, DetallePedido
from .forms import PedidoClienteForm, EstadoForm
from menu.models import Producto
from mesas.models import Mesa

# ── VISTA CLIENTE: hacer pedido ──────────────────────────────────
def hacer_pedido(request):
    categorias_con_productos = __import__('menu.models', fromlist=['Categoria']).Categoria.objects.prefetch_related('productos').filter(productos__disponible=True).distinct()
    mesas_disponibles = Mesa.objects.filter(disponible=True)

    if request.method == 'POST':
        form = PedidoClienteForm(request.POST)
        items_json = request.POST.get('items_json', '[]')
        try:
            items = json.loads(items_json)
        except:
            items = []

        if form.is_valid() and items:
            pedido = form.save(commit=False)
            pedido.save()
            for item in items:
                try:
                    producto = Producto.objects.get(pk=item['id'], disponible=True)
                    DetallePedido.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=item['cantidad'],
                        precio_unitario=producto.precio
                    )
                except Producto.DoesNotExist:
                    pass
            pedido.calcular_total()
            return redirect('pedido_confirmado', pk=pedido.pk)
        elif not items:
            messages.error(request, 'Debes agregar al menos un producto al pedido.')
    else:
        form = PedidoClienteForm()

    return render(request, 'cliente/hacer_pedido.html', {
        'form': form,
        'categorias': categorias_con_productos,
    })

def pedido_confirmado(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    return render(request, 'cliente/pedido_confirmado.html', {'pedido': pedido})

# ── VISTAS PERSONAL ──────────────────────────────────────────────
@login_required
def panel_personal(request):
    pedidos = Pedido.objects.exclude(estado='entregado').exclude(estado='cancelado')
    return render(request, 'pedidos/panel.html', {'pedidos': pedidos, 'estados': Pedido.ESTADOS})

@login_required
def lista_pedidos(request):
    estado = request.GET.get('estado', '')
    pedidos = Pedido.objects.all()
    if estado:
        pedidos = pedidos.filter(estado=estado)
    return render(request, 'pedidos/lista.html', {
        'pedidos': pedidos,
        'estados': Pedido.ESTADOS,
        'estado_filtro': estado,
    })

@login_required
def detalle_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    form_estado = EstadoForm(request.POST or None, instance=pedido)
    if request.method == 'POST' and form_estado.is_valid():
        form_estado.save()
        messages.success(request, 'Estado actualizado.')
        return redirect('panel_personal')
    productos = Producto.objects.filter(disponible=True).order_by('categoria__nombre', 'nombre')
    return render(request, 'pedidos/detalle.html', {'pedido': pedido, 'form_estado': form_estado, 'productos': productos})

@login_required
@require_POST
def eliminar_item_pedido(request, item_id):
    item = get_object_or_404(DetallePedido, pk=item_id)
    pedido = item.pedido
    item.delete()
    pedido.calcular_total()
    messages.success(request, 'Producto eliminado del pedido.')
    return redirect('detalle_pedido', pk=pedido.pk)

@login_required
@require_POST
def agregar_item_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    producto_id = request.POST.get('producto_id')
    cantidad = int(request.POST.get('cantidad', 1))
    
    if producto_id and cantidad > 0:
        producto = get_object_or_404(Producto, pk=producto_id)
        # Check if item already exists in order
        item_existente = pedido.items.filter(producto=producto).first()
        if item_existente:
            item_existente.cantidad += cantidad
            item_existente.save()
        else:
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio
            )
        pedido.calcular_total()
        messages.success(request, f'{producto.nombre} agregado al pedido.')
    return redirect('detalle_pedido', pk=pedido.pk)

@login_required
@require_POST
def editar_comentario_item(request, item_id):
    item = get_object_or_404(DetallePedido, pk=item_id)
    notas = request.POST.get('notas', '')
    item.notas = notas
    item.save()
    messages.success(request, f'Comentario actualizado para {item.producto.nombre}.')
    return redirect('detalle_pedido', pk=item.pedido.pk)
