from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Product

class CartTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(
            name='Test Product', price=10.00, stock=100
        )

    def test_add_to_cart(self):
        # Debe requerir login
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('add_to_cart', args=[self.product.id]))
        self.assertRedirects(response, reverse('view_cart'))
        cart = self.client.session.get('cart', {})
        self.assertEqual(cart[str(self.product.id)], 1)

    def test_update_cart_item(self):
        self.client.login(username='testuser', password='12345')
        # Primero agregar
        self.client.get(reverse('add_to_cart', args=[self.product.id]))
        # Ahora actualizar cantidad a 3
        response = self.client.post(reverse('update_cart_item', args=[self.product.id]), {'quantity': 3})
        self.assertRedirects(response, reverse('view_cart'))
        cart = self.client.session.get('cart', {})
        self.assertEqual(cart[str(self.product.id)], 3)

    def test_remove_from_cart(self):
        self.client.login(username='testuser', password='12345')
        self.client.get(reverse('add_to_cart', args=[self.product.id]))
        self.client.get(reverse('remove_from_cart', args=[self.product.id]))
        cart = self.client.session.get('cart', {})
        self.assertNotIn(str(self.product.id), cart)
