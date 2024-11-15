from django.db import models
from django.conf import settings
from products.models import Product

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE )
    quantity = models.PositiveIntegerField(default=1)

    def item_total(self):
        return self.product.price * self.quantity 


    def __str__(self):
        return f"{self.variant} (x{self.quantity})"
    