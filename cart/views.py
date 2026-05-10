from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product
from .models import Cart, CartItem
@login_required(login_url='/users/login/')
def cart_view(request):
    """Cart page dikhane ke liye"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart.html', {'cart': cart})
@login_required(login_url='/users/login/')
def add_to_cart(request, product_id):
    """Product cart mein add karo"""
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"{product.name} quantity increased to {cart_item.quantity}")
    else:
        messages.success(request, f"{product.name} added to cart!")
    return redirect('cart-view')
@login_required(login_url='/users/login/')
def remove_from_cart(request, item_id):
    """Cart se item remove karo"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f"{product_name} removed from cart!")
    return redirect('cart-view')
@login_required(login_url='/users/login/')
def update_cart_quantity(request, item_id):
    """Cart item ki quantity update karo"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart updated!")
        else:
            cart_item.delete()
            messages.success(request, "Item removed!")
    return redirect('cart-view')
@login_required(login_url='/users/login/')
def cart_count(request):
    """AJAX ke liye cart item count"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return JsonResponse({'count': cart.total_items})