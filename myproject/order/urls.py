from django.urls import path
from . import views

app_name = 'order'  

urlpatterns = [
     path('order_admin/',views.order_admin,name='order_admin'),
     path('order_summary/', views.order, name='orders'),
     path('order_admin/<int:order_id>/', views.order_admin, name='order_admin_with_order'),
     path('update_orderitem_status/<int:orderitem_id>/', views.update_orderitem_status, name='update_orderitem_status'),
 
]
