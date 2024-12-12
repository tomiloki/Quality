import logging
from django.core.management.base import BaseCommand
from store.models import Category, Product

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Crea datos de ejemplo en la base de datos"

    def handle(self, *args, **options):
        # Crea categorías de ejemplo
        categories_data = ["Electrónica", "Hogar", "Juguetes", "Ropa"]
        categories = []
        for cat_name in categories_data:
            cat, created = Category.objects.get_or_create(name=cat_name)
            if created:
                logger.info(f"Categoría creada: {cat_name}")
            categories.append(cat)

        # Crea productos de ejemplo en la primera categoría
        cat_electronica = Category.objects.get(name="Electrónica")
        products_data = [
            {"name": "Smartphone", "price": 299.99, "stock": 50, "description": "Un teléfono inteligente de última generación."},
            {"name": "Televisor 4K", "price": 699.99, "stock": 20, "description": "TV 4K ultra HD."},
            {"name": "Laptop Gamer", "price": 1299.99, "stock": 10, "description": "Laptop para juegos exigentes."}
        ]

        for p_data in products_data:
            p, created = Product.objects.get_or_create(
                name=p_data["name"],
                category=cat_electronica,
                defaults={
                    "price": p_data["price"],
                    "stock": p_data["stock"],
                    "description": p_data["description"]
                }
            )
            if created:
                logger.info(f"Producto creado: {p_data['name']}")
            else:
                logger.info(f"Producto {p_data['name']} ya existía, no se creó otro.")

        self.stdout.write(self.style.SUCCESS("Datos de ejemplo creados con éxito."))
