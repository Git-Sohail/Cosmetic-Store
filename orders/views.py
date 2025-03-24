from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Order
from .forms import OrderCreateForm
from cart.cart import Cart
from products.models import Product

# Create your views here.

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    orders = paginator.get_page(page)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_create(request):
    cart = Cart(request)
    if not cart:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = cart.get_total_price()
            order.save()

            # Create order items
            for item in cart:
                order.items.create(
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # Clear the cart
            cart.clear()
            return redirect('orders:order_success', order_id=order.id)
    else:
        form = OrderCreateForm()
        if request.user.is_authenticated:
            form.fields['email'].initial = request.user.email
            form.fields['first_name'].initial = request.user.first_name
            form.fields['last_name'].initial = request.user.last_name
            form.fields['phone'].initial = request.user.phone_number
            form.fields['address'].initial = request.user.address

    return render(request, 'orders/order_form.html', {
        'form': form,
        'cart': cart
    })

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})

@login_required
def buy_now(request, product_id):
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Invalid request method.'
        }, status=400)

    try:
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        # Check if product is in stock
        if product.stock < quantity:
            return JsonResponse({
                'success': False,
                'message': f'Sorry, only {product.stock} items available in stock.'
            })
        
        # Create order directly
        order = Order.objects.create(
            user=request.user,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            email=request.user.email,
            phone=request.user.phone_number,
            address=request.user.address,
            total_amount=product.price * quantity,
            status='pending'
        )
        
        # Create order item
        order.items.create(
            product=product,
            price=product.price,
            quantity=quantity
        )
        
        # Update product stock
        product.stock -= quantity
        product.sold_count += quantity
        product.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Your order has been placed successfully!',
            'order_id': order.id,
            'product_name': product.name,
            'quantity': quantity,
            'total_amount': f'Rs. {order.total_amount}'
        })
    
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Product not found.'
        }, status=404)
    except ValueError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid quantity value.'
        }, status=400)
    except Exception as e:
        print(f"Error in buy_now view: {str(e)}")  # Add error logging
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while processing your order. Please try again.'
        }, status=500)
