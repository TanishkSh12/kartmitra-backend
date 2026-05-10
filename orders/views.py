from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem

@login_required(login_url='/users/login/')
def checkout(request):
    """Checkout page - Order confirmation"""
    cart = Cart.objects.get(user=request.user)
    
    if cart.items.count() == 0:
        messages.warning(request, "Your cart is empty!")
        return redirect('cart-view')
    
    if request.method == 'POST':
        # Get shipping details
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total_price,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            pincode=pincode
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.final_price
            )
        
        # Clear cart
        cart.items.all().delete()
        
        messages.success(request, f"Order placed successfully! Your Order ID: {order.order_id}")
        return redirect('order-detail', order_id=order.id)
    
    return render(request, 'orders/checkout.html', {'cart': cart})

@login_required(login_url='/users/login/')
def order_list(request):
    """User ke saare orders"""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required(login_url='/users/login/')
def order_detail(request, order_id):
    """Single order details"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})