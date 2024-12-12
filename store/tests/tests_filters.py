# store/tests/test_filters.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Product, Category

class FiltersTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        cat = Category.objects.create(name="Electrónica")
        Product.objects.create(name="Smartphone A", price=100, stock=10, category=cat)
        Product.objects.create(name="Smartphone B", price=200, stock=5, category=cat)
        Product.objects.create(name="Televisor 4K", price=500, stock=3, category=cat)

    def test_filter_by_price(self):
        response = self.client.get(reverse('product_list'), {'min_price': '150'})
        self.assertContains(response, "Smartphone B")
        self.assertContains(response, "Televisor 4K")
        self.assertNotContains(response, "Smartphone A")

