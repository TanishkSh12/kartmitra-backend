from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product-list'),
    path('category/<slug:category_slug>/', views.product_list, name='category-products'),
    path('<int:product_id>/', views.product_detail, name='product-detail'),
    path('api/<int:product_id>/', views.product_detail_api, name='product-detail-api'),
    path('simple/<int:product_id>/', views.simple_product_view, name='simple-product'),
    path('search/', views.search_products, name='search-products'),
]