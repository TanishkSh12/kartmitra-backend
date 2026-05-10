from django.shortcuts import render
from products.models import Product, Category
def home(request):
    products = Product.objects.filter(is_available=True)[:12]  # 12 products for homepage
    categories = Category.objects.filter(is_active=True)[:8]   # 8 categories for homepage
    return render(request, 'homepage.html', {
        'products': products,
        'categories': categories
    })
    