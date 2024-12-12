# store/views/product_views.py
# store/views/product_views.py
from django.shortcuts import render, get_object_or_404
# store/views/product_views.py
from django.shortcuts import render
from store.models import Product, Category
from django.core.paginator import Paginator

def product_list(request):
    category_name = request.GET.get('category')
    q = request.GET.get('q')
    order = request.GET.get('order')  # 'price_asc', 'price_desc', 'name_asc', 'name_desc'
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()

    if category_name:
        products = products.filter(category__name=category_name)
    if q:
        products = products.filter(name__icontains=q)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Ordenar
    if order == 'price_asc':
        products = products.order_by('price')
    elif order == 'price_desc':
        products = products.order_by('-price')
    elif order == 'name_asc':
        products = products.order_by('name')
    elif order == 'name_desc':
        products = products.order_by('-name')
    else:
        products = products.order_by('name')

    paginator = Paginator(products, 9)  # 9 productos por página
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
    return render(request, 'store/product_list.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'store/product_detail.html', {'product': product})