from django.urls import path
from . import views

app_name = 'cart'  

urlpatterns = [
    path('cart/',views.cart_view,name='cart_view'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),


]
