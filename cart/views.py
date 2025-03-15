from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from products.models import Product
from .forms import CartAddProductForm
from .models import Cart, CartItem
from .cart import Cart as SessionCart

def cart_detail(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        return render(request, 'cart/cart_detail.html', {'cart': cart_items, 'cart_obj': cart})
    else:
        cart = SessionCart(request)
        return render(request, 'cart/cart_detail.html', {'cart': cart})

@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        quantity = cd['quantity']
        override = cd['override']
        
        if request.user.is_authenticated:
            # Use model-based cart for authenticated users
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                if override:
                    cart_item.quantity = quantity
                else:
                    cart_item.quantity += quantity
                cart_item.save()
        else:
            # Use session-based cart for anonymous users
            cart = SessionCart(request)
            cart.add(product=product, quantity=quantity, override_quantity=override)
    
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        # Use model-based cart for authenticated users
        cart = Cart.objects.get(user=request.user)
        CartItem.objects.filter(cart=cart, product=product).delete()
    else:
        # Use session-based cart for anonymous users
        cart = SessionCart(request)
        cart.remove(product)
    
    return redirect('cart:cart_detail')
