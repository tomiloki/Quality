# store/views/payment_views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from store.models import Order

@login_required
def payment_process(request):
    # Este es un endpoint ficticio que simula el pago.
    # En un escenario real, aquí interactuaríamos con la API de Stripe/PayPal.
    if request.method == 'POST':
        # Supongamos que el pago se aprobó con éxito
        order_id = request.POST.get('order_id')
        order = Order.objects.get(pk=order_id, user=request.user)
        # Cambiamos el estado del pedido a 'paid' (asumiendo que existe ese estado)
        order.status = 'paid'
        order.save()
        # Podríamos redirigir a order_history o una página de confirmación
        return redirect('order_history')
    else:
        # Si llegamos aquí sin POST, redirigir a la lista de pedidos o homepage
        return redirect('product_list')
