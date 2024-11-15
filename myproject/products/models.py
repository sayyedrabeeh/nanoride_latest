from django.db import models

# Create your models here.
class Categories(models.Model):
    brand_name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    status = models.CharField(max_length=10, default='listed')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.brand_name 
 

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ratings = models.FloatField(default=0.0)
    comments = models.TextField(blank=True)
    size = models.CharField(max_length=20)      

    status = models.CharField(max_length=10, default='listed') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)   
    stock = models.PositiveIntegerField(default=0) 
 
    # Foreign Key relationship
    category = models.ForeignKey('Categories', on_delete=models.CASCADE,default=0 )      
    
     
    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/extra/')


