# store/tests/test_payments.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Product, Order, OrderItem

class PaymentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='buyer', email='buyer@example.com', password='12345')
        self.client.login(username='buyer', password='12345')
        self.product = Product.objects.create(name='Test Product Payment', price=50.00, stock=10)
        
        # Simular checkout
        cart = {str(self.product.id): 2}  # 2 unidades
        session = self.client.session
        session['cart'] = cart
        session.save()

        # Realizar checkout
        response = self.client.post(reverse('checkout'), {
            'shipping_address': 'Calle Falsa 123',
            'payment_method': 'tarjeta'
        })
        self.order = Order.objects.filter(user=self.user).first()

    def test_payment_process(self):
        # Ahora simulamos el pago
        response = self.client.post(reverse('payment_process'), {'order_id': self.order.id})
        self.assertRedirects(response, reverse('order_history'))
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'paid')
