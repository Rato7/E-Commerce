from django.urls import path
from . import views

app_name = 'App'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:product_id>/', views.product_page, name='product_page'),
    path('cart/', views.cart_detail, name='cart'),
    path('cart/add/<int:product_id>/', views.cart_add, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='remove_from_cart'),
]