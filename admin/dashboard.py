from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from orders.models import Order
from products.models import Product, Category
from users.models import CustomUser
from newsletter.models import NewsletterSubscriber

@staff_member_required
def admin_dashboard(request):
    # Date ranges
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    
    # Orders statistics
    total_orders = Order.objects.count()
    recent_orders = Order.objects.order_by('-created_at')[:5]
    
    # Sales statistics
    total_sales = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0
    daily_sales = Order.objects.filter(created_at__date=today).aggregate(total=Sum('total_price'))['total'] or 0
    weekly_sales = Order.objects.filter(created_at__date__gte=start_of_week).aggregate(total=Sum('total_price'))['total'] or 0
    monthly_sales = Order.objects.filter(created_at__date__gte=start_of_month).aggregate(total=Sum('total_price'))['total'] or 0
    
    # Product statistics
    total_products = Product.objects.count()
    out_of_stock = Product.objects.filter(stock=0).count()
    low_stock = Product.objects.filter(stock__lte=10).exclude(stock=0).count()
    top_selling = Product.objects.annotate(sold=Count('orderitem')).order_by('-sold')[:5]
    
    # Category statistics
    category_sales = Category.objects.annotate(
        total_sales=Sum('products__orderitem__price'),
        products_count=Count('products')
    ).order_by('-total_sales')[:5]
    
    # User statistics
    total_users = CustomUser.objects.count()
    new_users_today = CustomUser.objects.filter(date_joined__date=today).count()
    new_users_week = CustomUser.objects.filter(date_joined__date__gte=start_of_week).count()
    new_users_month = CustomUser.objects.filter(date_joined__date__gte=start_of_month).count()
    
    # Newsletter statistics
    total_subscribers = NewsletterSubscriber.objects.count()
    active_subscribers = NewsletterSubscriber.objects.filter(is_active=True).count()
    
    context = {
        'total_orders': total_orders,
        'recent_orders': recent_orders,
        'total_sales': total_sales,
        'daily_sales': daily_sales,
        'weekly_sales': weekly_sales,
        'monthly_sales': monthly_sales,
        'total_products': total_products,
        'out_of_stock': out_of_stock,
        'low_stock': low_stock,
        'top_selling': top_selling,
        'category_sales': category_sales,
        'total_users': total_users,
        'new_users_today': new_users_today,
        'new_users_week': new_users_week,
        'new_users_month': new_users_month,
        'total_subscribers': total_subscribers,
        'active_subscribers': active_subscribers,
    }
    
    return render(request, 'admin/dashboard.html', context) 