from django.urls import path
from . import views

app_name = 'App'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:product_id>/', views.product_page, name='product_page')
]