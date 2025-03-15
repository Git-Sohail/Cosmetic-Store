from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from orders.models import Order
from .models import Payment
from .utils import generate_esewa_payment_url, verify_esewa_payment, verify_khalti_payment

# Create your views here.

@login_required
def initiate_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        if payment_method not in ['esewa', 'khalti']:
            messages.error(request, 'Invalid payment method.')
            return redirect('orders:order_detail', order_id=order_id)
        
        # Create payment record
        payment = Payment.objects.create(
            order=order,
            user=request.user,
            amount=order.total_price,
            payment_method=payment_method,
            payment_id=str(uuid.uuid4())
        )
        
        if payment_method == 'esewa':
            # Generate eSewa payment URL
            payment_url = generate_esewa_payment_url(payment)
            return redirect(payment_url)
        else:
            # For Khalti, we'll use their JavaScript SDK
            return render(request, 'payment/khalti_payment.html', {
                'payment': payment,
                'khalti_public_key': settings.KHALTI_PUBLIC_KEY
            })
    
    return render(request, 'payment/payment_methods.html', {
        'order': order
    })

@require_POST
def esewa_callback(request):
    """Handle eSewa payment callback"""
    try:
        data = json.loads(request.body)
        payment_id = data.get('payment_id')
        payment = get_object_or_404(Payment, payment_id=payment_id)
        
        if verify_esewa_payment(data):
            payment.mark_as_completed(
                transaction_id=data.get('transaction_id'),
                payment_details=data
            )
            messages.success(request, 'Payment completed successfully!')
            return redirect('orders:order_detail', order_id=payment.order.id)
        else:
            payment.mark_as_failed(data)
            messages.error(request, 'Payment verification failed.')
            return redirect('orders:order_detail', order_id=payment.order.id)
            
    except Exception as e:
        messages.error(request, f'Payment processing error: {str(e)}')
        return redirect('orders:order_list')

@require_POST
def khalti_callback(request):
    """Handle Khalti payment callback"""
    try:
        data = json.loads(request.body)
        payment_id = data.get('payment_id')
        payment = get_object_or_404(Payment, payment_id=payment_id)
        
        if verify_khalti_payment(data):
            payment.mark_as_completed(
                transaction_id=data.get('idx'),
                payment_details=data
            )
            return JsonResponse({'status': 'success'})
        else:
            payment.mark_as_failed(data)
            return JsonResponse({'status': 'error'})
            
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
def payment_history(request):
    """Display user's payment history"""
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'payment/payment_history.html', {
        'payments': payments
    })
