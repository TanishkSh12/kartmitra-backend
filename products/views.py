from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db import models
from django.core.paginator import Paginator
from .models import Product, Category
def product_list(request, category_slug=None):
    products = Product.objects.filter(is_available=True)
    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
        try:
            current_category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            pass
    category_slug_param = request.GET.get('category_slug')
    if category_slug_param and not category_slug:
        products = products.filter(category__slug=category_slug_param)
        try:
            current_category = Category.objects.get(slug=category_slug_param)
        except Category.DoesNotExist:
            pass
    gender = request.GET.get('gender')
    if gender and gender != 'all':
        products = products.filter(gender=gender)
    colors = request.GET.getlist('color')
    if colors:
        products = products.filter(color__in=colors)
    fabrics = request.GET.getlist('fabric')
    if fabrics:
        products = products.filter(fabric__in=fabrics)
    shape = request.GET.get('shape')
    if shape:
        products = products.filter(dial_shape=shape)
    q = request.GET.get('q', '')
    if q:
        products = products.filter(
            models.Q(name__icontains=q) | 
            models.Q(description__icontains=q) |
            models.Q(product_code__icontains=q)
        )
    sort_by = request.GET.get('sort')
    if sort_by == 'low_to_high':
        products = products.order_by('price')
    elif sort_by == 'high_to_low':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')
    all_categories = Category.objects.filter(is_active=True)
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    products_count = products.count() 
    return render(request, 'products/product_list.html', {
        'products': page_obj,
        'page_obj': page_obj,
        'sort_by': sort_by,
        'current_category': current_category,
        'all_categories': all_categories,
        'products_count': products_count,
        'query': q,
        'current_gender': gender,
    })
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    return render(request, 'products/product_detail.html', {'product': product})
def search_products(request):
    """Search products by name or description"""
    return product_list(request)  
def product_detail_api(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    data = {
        'id': product.id,
        'name': product.name,
        'price': str(product.price),
        'discount_price': str(product.discount_price) if product.discount_price else None,
        'final_price': str(product.final_price),
        'stock': product.stock,
        'description': product.description,
        'category': product.category.name if product.category else None,
        'is_available': product.is_available,
        'created_at': product.created_at,
        'gender': getattr(product, 'gender', None),
        'color': getattr(product, 'color', None),
        'fabric': getattr(product, 'fabric', None),
    }
    
    return JsonResponse(data)
def simple_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return HttpResponse(f"Product: {product.name}, Price: {product.final_price}")
def home(request):
    """Homepage view with featured products and categories"""
    trending_products = Product.objects.filter(is_available=True)[:10]
    categories = Category.objects.filter(is_active=True)
    all_products = Product.objects.filter(is_available=True)[:24]
    context = {
        'trending_products': trending_products,
        'categories': categories,
        'products': all_products,
    }
    return render(request, 'homepage.html', context)

def category_products(request, category_slug):
    """View products by category"""
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    products = Product.objects.filter(category=category, is_available=True)
    
    subcategory_slug = request.GET.get('sub')
    if subcategory_slug:
        products = products.filter(subcategory__slug=subcategory_slug)
    gender = request.GET.get('gender')
    if gender:
        products = products.filter(gender=gender)
    colors = request.GET.getlist('color')
    if colors:
        products = products.filter(color__in=colors)
    
    fabrics = request.GET.getlist('fabric')
    if fabrics:
        products = products.filter(fabric__in=fabrics)
    sort_by = request.GET.get('sort')
    if sort_by == 'low_to_high':
        products = products.order_by('price')
    elif sort_by == 'high_to_low':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')
    all_categories = Category.objects.filter(is_active=True)
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'products/category_products.html', {
        'category': category,
        'products': page_obj,
        'page_obj': page_obj,
        'sort_by': sort_by,
        'all_categories': all_categories,
        'products_count': products.count(),
    })