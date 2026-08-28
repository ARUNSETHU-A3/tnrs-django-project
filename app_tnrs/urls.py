from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('404/', views.page_not_found, name='page_not_found'),
    path('buy/<int:item_id>/', views.buy_product, name='buy_product'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('orders/', views.view_orders, name='view_orders'),
    # Custom admin dashboard (only for superusers)
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/products/add/', views.product_create, name='product_create'),
    path('admin-dashboard/products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('admin-dashboard/products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('admin-dashboard/products/<int:pk>/toggle/', views.product_toggle_availability, name='product_toggle_availability'),
    path('admin-dashboard/orders/<int:pk>/update-status/', views.order_update_status, name='order_update_status'),
]

