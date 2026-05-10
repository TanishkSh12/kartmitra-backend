from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart-view'),
    path('add/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('update/<int:item_id>/', views.update_cart_quantity, name='update-cart'),
    path('count/', views.cart_count, name='cart-count'),
]