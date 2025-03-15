from .cart import Cart as SessionCart
from .models import Cart, CartItem

def cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        # Calculate total items
        total_items = sum(item.quantity for item in cart_items)
        return {'cart': cart_items, 'cart_obj': cart, 'cart_count': total_items}
    else:
        cart = SessionCart(request)
        return {'cart': cart, 'cart_count': len(cart)} 