from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login

from .models import Product, Cart, CartItem, Address
from .forms import RegisterForm, AddressForm

# Função para checar se é dono (owner)
def is_owner(user):
    return user.is_authenticated and getattr(user, 'is_owner', False)

# Register
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('App:home')
    else:
        form = RegisterForm()

    return render(request, 'Registration/register.html', {'form': form})

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

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    return redirect('App:product_page', product_id=product.id)

@login_required
def cart_remove(request, cart_item_id):
    item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    if request.method == 'POST':
        item.delete()
    return redirect('App:cart_detail')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = cart.total()

    addresses = Address.objects.filter(user=request.user)

    print(addresses)

    return render(request, 'App/cart.html', context={'cart': cart, 'items': items, 'total': total, 'addresses': addresses})

@login_required
def address_page(request):

    addresses = Address.objects.filter(user=request.user)

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('App:address_page')

    return render(request, 'App/address_page.html', context={'addresses':addresses})

# DASHBOARD - apenas para donos (is_owner)

@user_passes_test(is_owner)
def dashboard_home(request):
    # Você pode enviar dados específicos para a dashboard aqui
    return render(request, 'App/dashboard/home.html')
