# store/tests/test_orders.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Product, Order, OrderItem
from decimal import Decimal

class OrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='12345')
        self.client.login(username='buyer', password='12345')
        self.product = Product.objects.create(name='Test Product', price=20.00, stock=10)
        self.client.get(reverse('add_to_cart', args=[self.product.id]))

    def test_checkout_creates_order(self):
        response = self.client.post(reverse('checkout'), {
            'shipping_address': '123 Test St',
            'payment_method': 'tarjeta'
        })
        # Debe redirigir al order_history
        self.assertRedirects(response, reverse('order_history'))
        order = Order.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.total, Decimal('20.00'))
        # Verificar que stock disminuyó
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 9)
