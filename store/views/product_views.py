# store/views/product_views.py
# store/views/product_views.py
from django.shortcuts import render, get_object_or_404
from store.models import Product, Category

from django.core.paginator import Paginator

def product_list(request):
    category_name = request.GET.get('category')
    q = request.GET.get('q')

    products = Product.objects.all().order_by('name')
    categories = Category.objects.all()

    if category_name:
        products = products.filter(category__name=category_name)
    if q:
        products = products.filter(name__icontains=q)

    paginator = Paginator(products, 9)  # 9 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_name,
        'search_query': q
    }
    return render(request, 'store/product_list.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'store/product_detail.html', {'product': product})