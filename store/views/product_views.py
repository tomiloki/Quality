# store/views/product_views.py
# store/views/product_views.py
import logging
from django.shortcuts import render, get_object_or_404
from store.models import Product, Category
from django.core.paginator import Paginator

logger = logging.getLogger(__name__)

def product_list(request):
    logger.info("Entrando a la vista product_list con parámetros: %s", request.GET)
    category_name = request.GET.get('category')
    q = request.GET.get('q')
    order = request.GET.get('order')  # 'price_asc', 'price_desc', 'name_asc', 'name_desc'
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()

    # Filtro por categoría
    if category_name:
        products = products.filter(category__name=category_name)

    # Búsqueda por nombre
    if q:
        products = products.filter(name__icontains=q)

    # Filtro por rango de precios
    if min_price:
        try:
            min_p = float(min_price)
            products = products.filter(price__gte=min_p)
        except ValueError:
            logger.warning("Valor no numérico para min_price: %s", min_price)

    if max_price:
        try:
            max_p = float(max_price)
            products = products.filter(price__lte=max_p)
        except ValueError:
            logger.warning("Valor no numérico para max_price: %s", max_price)

    # Ordenamiento
    if order == 'price_asc':
        products = products.order_by('price')
    elif order == 'price_desc':
        products = products.order_by('-price')
    elif order == 'name_asc':
        products = products.order_by('name')
    elif order == 'name_desc':
        products = products.order_by('-name')
    else:
        # orden por defecto por nombre asc
        products = products.order_by('name')

    # Paginación
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_name,
        'search_query': q,
        'order': order,
        'min_price': min_price,
        'max_price': max_price,
    }

    logger.info("Product_list renderizado con éxito con %d productos.", page_obj.paginator.count)
    return render(request, 'store/product_list.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'store/product_detail.html', {'product': product})