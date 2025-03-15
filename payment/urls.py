from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('initiate/<int:order_id>/', views.initiate_payment, name='initiate_payment'),
    path('esewa/callback/', views.esewa_callback, name='esewa_callback'),
    path('khalti/callback/', views.khalti_callback, name='khalti_callback'),
    path('history/', views.payment_history, name='payment_history'),
] 