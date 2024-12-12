# store/views/cart_views.py

from django.shortcuts import render, redirect
from store.models import Product
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0.00')
    for product_id, quantity in cart.items():
        product = Product.objects.get(pk=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'store/cart.html', context)

@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    messages.success(request, "Producto agregado al carrito con éxito.")
    return redirect('view_cart')

@login_required
def update_cart_item(request, product_id):
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        if new_quantity > 0:
            cart[str(product_id)] = new_quantity
        else:
            cart.pop(str(product_id), None)
        request.session['cart'] = cart
    return redirect('view_cart')

@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('view_cart')

@login_required
def checkout(request):
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')
        user = request.user
        cart = request.session.get('cart', {})
        
        if not cart:
            return redirect('view_cart')
        
        from store.models import Order, OrderItem
        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address,
            payment_method=payment_method,
            total=0
        )

        total = Decimal('0.00')
        for product_id, quantity in cart.items():
            product = Product.objects.get(pk=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )
            total += product.price * quantity
            product.stock -= quantity
            product.save()

        order.total = total
        order.save()

        # Vaciar carrito
        request.session['cart'] = {}

        return redirect('order_history')

    return render(request, 'store/checkout.html')
