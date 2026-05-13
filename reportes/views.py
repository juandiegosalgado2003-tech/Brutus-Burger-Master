from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F
from django.utils import timezone
from datetime import timedelta
from pedidos.models import Pedido, DetallePedido

@login_required
def dashboard(request):
    hoy = timezone.now().date()
    ventas_hoy = Pedido.objects.filter(fecha_creacion__date=hoy, estado='entregado').aggregate(
        total=Sum('total'), cantidad=Count('id'))
    ventas_semana = Pedido.objects.filter(
        fecha_creacion__date__gte=hoy - timedelta(days=7), estado='entregado'
    ).aggregate(total=Sum('total'), cantidad=Count('id'))
    top_productos = DetallePedido.objects.filter(
        pedido__fecha_creacion__date__gte=hoy - timedelta(days=30)
    ).values(nombre=F('producto__nombre')).annotate(
        total_vendido=Sum('cantidad'),
        ingresos=Sum(F('cantidad') * F('precio_unitario'))
    ).order_by('-total_vendido')[:5]
    pedidos_hoy = Pedido.objects.filter(fecha_creacion__date=hoy).values('estado').annotate(cantidad=Count('id'))
    return render(request, 'reportes/dashboard.html', {
        'ventas_hoy': ventas_hoy,
        'ventas_semana': ventas_semana,
        'top_productos': top_productos,
        'pedidos_hoy': pedidos_hoy,
        'hoy': hoy,
    })
