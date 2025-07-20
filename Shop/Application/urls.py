from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'App'

urlpatterns = [
    path('', views.home, name='home'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/register/', views.register, name='register'),

    path('accounts/address/', views.address_page, name='address_page'),

    path('<int:product_id>/', views.product_page, name='product_page'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:cart_item_id>/', views.cart_remove, name='cart_remove'),

    path('dashboard/', views.dashboard_home)
]