from django.shortcuts import render,redirect
from .models import Cart,CartItem
from django.shortcuts import get_object_or_404
from products.models import Product
from order.models import OrderItem,Order
from user_profile.models import Address
from django.contrib.auth.decorators import login_required


@login_required(login_url='/auth/login/')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('num-product', 1))  
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if item_created:
        cart_item.quantity = quantity   
    else:
        cart_item.quantity += quantity  
    cart_item.save()   
    return redirect('cart:cart_view')  
def cart_view(request):
    cart = Cart.objects.get(user=request.user)   
    cart_items = []   
    total_price = 0   
    for item in cart.items.all():
        item_total = item.product.price * item.quantity   
        total_price += item_total   
        cart_items.append({
            'product': item.product,
            'quantity': item.quantity,
            'item_total': item_total,
        })
    addresses = Address.objects.filter(user=request.user)   
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'addresses': addresses,
    }
    if request.method == "POST":
        shipping_address_id = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')
        if not shipping_address_id or not payment_method:
            context['error'] = "Please select a shipping address and payment method."
            return render(request, 'cart/cart.html', context)
        shipping_address = Address.objects.get(id=shipping_address_id)
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            total_price=total_price,
            payment_type=payment_method,
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                subtotal_price=item.product.price * item.quantity,
            )
            product = item.product
            product.stock -= item.quantity
            product.save() 
        cart.items.all().delete()
        return redirect('order:orders')   
    return render(request, 'cart/cart.html', context) 
def remove_cart_item(request, product_id):
    cart = Cart.objects.get(user=request.user)
    CartItem.objects.filter(cart=cart, product__id=product_id).delete()
    return redirect('cart:cart_view')
