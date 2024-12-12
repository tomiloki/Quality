from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from store.models import Product, Order, OrderItem
from store.forms import ProductForm
from django.db.models import Sum
from datetime import datetime, timedelta
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

def admin_check(user):
    return user.is_staff or user.is_superuser

@user_passes_test(admin_check)
def admin_dashboard(request):
    products = Product.objects.all()
    low_stock_products = products.filter(stock__lt=5)
    logger.info("El usuario %s accedió al admin_dashboard", request.user.username)
    return render(request, 'store/admin_dashboard.html', {
        'products': products,
        'low_stock': low_stock_products.exists()
    })

@user_passes_test(admin_check)
def add_product(request):
    logger.info("El usuario %s accedió a add_product", request.user.username)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            logger.info("Producto %s creado por el usuario %s", product.name, request.user.username)
            return redirect('admin_dashboard')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})

@user_passes_test(admin_check)
def edit_product(request, product_id):
    logger.info("El usuario %s accedió a edit_product para producto_id %d", request.user.username, product_id)
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            logger.info("Producto %s (ID %d) editado por el usuario %s", product.name, product.id, request.user.username)
            return redirect('admin_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/edit_product.html', {'form': form})

@user_passes_test(admin_check)
def delete_product(request, product_id):
    logger.info("El usuario %s accedió a delete_product para producto_id %d", request.user.username, product_id)
    product = get_object_or_404(Product, pk=product_id)
    product_name = product.name
    product.delete()
    logger.info("Producto %s (ID %d) eliminado por el usuario %s", product_name, product_id, request.user.username)
    return redirect('admin_dashboard')

@user_passes_test(admin_check)
def update_order_status(request, order_id):
    logger.info("El usuario %s accedió a update_order_status para order_id %d", request.user.username, order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order = get_object_or_404(Order, pk=order_id)
        order.status = new_status
        order.save()

        subject = "Actualización de estado de tu pedido"
        message = f"Hola {order.user.username}, tu pedido #{order.id} ahora está: {order.get_status_display()}"
        from_email = "no-reply@mitienda.com"
        recipient_list = [order.user.email]
        send_mail(subject, message, from_email, recipient_list)

        logger.info("El estado del pedido #%d se ha cambiado a %s por el usuario %s", order.id, new_status, request.user.username)

        return redirect('admin_dashboard')
    else:
        order = get_object_or_404(Order, pk=order_id)
        return render(request, 'store/update_order_status.html', {'order': order})

@user_passes_test(admin_check)
def admin_reports(request):
    logger.info("El usuario %s accedió a admin_reports", request.user.username)
    last_month = datetime.now() - timedelta(days=30)
    total_sales = Order.objects.filter(created_at__gte=last_month, status='delivered').aggregate(Sum('total'))['total__sum'] or 0
    top_products = OrderItem.objects.filter(order__created_at__gte=last_month) \
                                    .values('product__name') \
                                    .annotate(total_qty=Sum('quantity')) \
                                    .order_by('-total_qty')[:5]

    return render(request, 'store/admin_reports.html', {
        'total_sales': total_sales,
        'top_products': top_products,
    })
