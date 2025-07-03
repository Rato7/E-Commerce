from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'App/home.html', context={'products': products})

def product_page(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'App/product_page.html', context={'product': product})