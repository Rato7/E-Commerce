from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Product, Cart, CartItem

# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'App/home.html', context={'products': products})

def product_page(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'App/product_page.html', context={'product': product})

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1)) if request.method == 'POST' else 1

    # Pega ou cria o carrinho do usuário
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Tenta pegar o item do carrinho, se já existir
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        # Se o item já existia, só soma a quantidade
        cart_item.quantity += quantity
    else:
        # Se criou agora, já tem a quantidade padrão
        cart_item.quantity = quantity

    cart_item.save()

    return redirect('App:product_page', product_id=product.id)

@login_required
def cart_remove(request, product_id):
    item = get_object_or_404(CartItem, id=product_id, cart__user=request.user)
    if request.method == 'POST':
        item.delete()
    return redirect('App:cart')

@login_required
def cart_detail(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()
    total = cart.total()
    return render(request, 'App/cart.html', context={'cart': cart, 'items':items, 'total': total})