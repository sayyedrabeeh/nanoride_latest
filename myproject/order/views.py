from django.shortcuts import render, get_object_or_404
from .models import OrderItem,Order
from django.http import JsonResponse

# Create your views here.
def order(request):
    
    order_items = OrderItem.objects.filter(order__user=request.user)
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'order/order.html', context)

def order_admin(request):
    orders = Order.objects.all()  
    order_items = OrderItem.objects.all()
    context = {
        'orders': orders,
        'order_items': order_items,
    }
    return render(request, 'order/order_admin.html', context)

def order_admin(request, order_id=None):
    if order_id:
        order = get_object_or_404(Order, order_id=order_id)
        shipping_address = order.shipping_address
        print(shipping_address)  
        order_items = OrderItem.objects.filter(order=order)
        context = {
            'order': order,
            'order_items': order_items,
            'selected_order_id': order.order_id,
            'shipping_address': shipping_address
        }
        return render(request, 'order/order_admin.html', context)
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'order/order_admin.html', context)

def update_orderitem_status(request, orderitem_id):
    if request.method == 'POST':
        try:
            order_item = get_object_or_404(OrderItem, orderitem_id=orderitem_id)   
            new_status = request.POST.get('status')
            if new_status:
                if new_status == "Cancelled" and order_item.status != "Cancelled":
                    product = order_item.product
                    product.stock += order_item.quantity
                    product.save()
                order_item.status = new_status
                order_item.save()
                return JsonResponse({'message': 'Order item status updated successfully!'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid status selected'}, status=400)
        except Exception as e:
            print("Error:", e)
            return JsonResponse({'error': 'Something went wrong'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)