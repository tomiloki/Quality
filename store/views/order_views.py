# store/views/order_views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from store.models import Order

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})

@login_required
def track_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'store/track_order.html', {'order': order})

# Vista para admins (actualización de estado)
from django.contrib.auth.decorators import user_passes_test

def admin_check(user):
    return user.is_staff or user.is_superuser

@user_passes_test(admin_check)
def update_order_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST.get('status') 
        order = get_object_or_404(Order, pk=order_id)
        order.status = new_status
        order.save()
        # Podríamos enviar notificación al usuario aquí
        return redirect('admin_dashboard')
    else:
        order = get_object_or_404(Order, pk=order_id)
        return render(request, 'store/update_order_status.html', {'order': order})
