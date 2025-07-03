from django.db import models
from django.utils.text import slugify
import os

def product_main_path(instance, filename):
    product_name = slugify(instance.nome)
    return os.path.join('products', product_name, 'main', filename)

def product_image_path(instance, filename):
    product_name = slugify(instance.product.name)
    return os.path.join('products', product_name, 'galery', filename)

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    sku = models.CharField(max_length=50, unique=True)
    price = models.FloatField()
    image = models.ImageField(upload_to=product_main_path)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'Product ID {self.id}: {self.name} {self.sku}'
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_image_path)

    def __str__(self):
        return f'Image from: Product ID {self.product.id}: {self.product.name} {self.product.sku}'