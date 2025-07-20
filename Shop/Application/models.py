from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.conf import settings
import os

def product_main_path(instance, filename):
    product_name = slugify(instance.name)
    return os.path.join('products', product_name, 'main', filename)

def product_image_path(instance, filename):
    product_name = slugify(instance.product.name)
    return os.path.join('products', product_name, 'galery', filename)

# User
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, whatsapp, password=None, **extra_fields):
        if not email:
            raise ValueError('O E-mail é obrigatório!')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, whatsapp=whatsapp, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, name, whatsapp, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not password:
            raise ValueError('SuperUser precisa ter senha!')
        return self.create_user(email, name, whatsapp, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # seus campos
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=150)
    whatsapp = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # aqui mudou
        blank=True,
        help_text="Grupos para permissões do usuário.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # aqui mudou
        blank=True,
        help_text="Permissões específicas para o usuário.",
        verbose_name="user permissions",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'whatsapp']

    def __str__(self):
        return self.email

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    cep = models.CharField(max_length=9)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    complement = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.street}, {self.number} - {self.city}'

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

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    update_at = models.DateTimeField(auto_now=True)

    def total(self):
        return sum(item.total() for item in self.items.all())
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity  = models.PositiveIntegerField(default=1)

    def total(self):
        return self.product.price * self.quantity