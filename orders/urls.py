from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('create/', views.order_create, name='order_create'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
] 