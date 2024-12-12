# store/urls.py
# store/urls.py
from django.urls import path
from .views.product_views import product_list, product_detail
from .views.payment_views import payment_process
from .views.cart_views import view_cart, add_to_cart, update_cart_item, remove_from_cart, checkout
from .views.order_views import order_history, track_order
from .views.user_views import user_login, user_logout, user_register
from .views.admin_views import admin_dashboard, add_product, edit_product, delete_product, update_order_status, admin_reports

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),

    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),

    path('orders/history/', order_history, name='order_history'),
    path('orders/track/<int:order_id>/', track_order, name='track_order'),

    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),

    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/product/add/', add_product, name='add_product'),
    path('admin/product/edit/<int:product_id>/', edit_product, name='edit_product'),
    path('admin/product/delete/<int:product_id>/', delete_product, name='delete_product'),
    path('admin/order/update_status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('admin/reports/', admin_reports, name='admin_reports'),
    
    path('payment/process/', payment_process, name='payment_process'),
]
