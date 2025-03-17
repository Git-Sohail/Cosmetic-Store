from django.conf import settings
from .cart import Cart as SessionCart
from .models import Cart, CartItem

def cart(request):
    """
    Context processor that provides cart data for both authenticated and anonymous users.
    For authenticated users, it uses the database Cart model.
    For anonymous users, it uses the session-based Cart.
    """
    try:
        if request.user.is_authenticated:
            # Get or create cart for authenticated user
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_items = cart.items.all()
            total_items = sum(item.quantity for item in cart_items)
            total_price = cart.get_total_price()
            return {
                'cart': cart_items,
                'cart_obj': cart,
                'cart_count': total_items,
                'cart_total': total_price
            }
        else:
            # Use session-based cart for anonymous users
            session_cart = SessionCart(request)
            return {
                'cart': session_cart,
                'cart_count': len(session_cart),
                'cart_total': session_cart.get_total_price()
            }
    except Exception as e:
        # Provide empty cart data in case of errors
        return {
            'cart': [],
            'cart_count': 0,
            'cart_total': 0
        }