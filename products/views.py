from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Product, Category, Review
from .search import ProductSearch
from cart.forms import CartAddProductForm

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {
        'categories': categories
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    request.GET = request.GET.copy()
    request.GET['category'] = slug
    
    search = ProductSearch(request)
    results = search.get_results()
    results['category'] = category
    
    return render(request, 'products/category_detail.html', results)

def product_list(request, category_slug=None):
    search = ProductSearch(request)
    results = search.get_results()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON response for AJAX requests (search suggestions)
        return JsonResponse({
            'suggestions': results['suggestions']
        })
    
    return render(request, 'products/product_list.html', results)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    
    # Get related products from the same category
    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]
    
    # Get product reviews with helpful votes count
    reviews = product.reviews.filter(moderated=True).order_by('-created_at')
    
    # Get rating statistics
    rating_distribution = product.get_rating_distribution()
    average_rating = product.get_average_rating()
    
    # Check if user has already reviewed
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = product.reviews.filter(user=request.user).exists()
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'related_products': related_products,
        'reviews': reviews,
        'rating_distribution': rating_distribution,
        'average_rating': average_rating,
        'user_has_reviewed': user_has_reviewed
    })

@login_required
def product_review(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating and comment:
            # Check if user has already reviewed this product
            if product.reviews.filter(user=request.user).exists():
                messages.error(request, 'You have already reviewed this product.')
            else:
                review = product.reviews.create(
                    user=request.user,
                    rating=rating,
                    comment=comment
                )
                messages.success(request, 'Your review has been submitted and is pending moderation.')
        else:
            messages.error(request, 'Please provide both rating and comment.')
    
    return redirect('products:product_detail', id=id, slug=slug)

@login_required
@require_POST
def review_helpful(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    is_helpful = review.toggle_helpful(request.user)
    
    return JsonResponse({
        'helpful_count': review.get_helpful_count(),
        'is_helpful': is_helpful
    })

@login_required
@require_POST
def report_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.report()
    messages.success(request, 'Thank you for reporting this review. Our moderators will look into it.')
    
    return redirect('products:product_detail', id=review.product.id, slug=review.product.slug)

@login_required
def add_to_wishlist(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    
    if request.method == 'POST':
        if product in request.user.wishlist.all():
            request.user.wishlist.remove(product)
            messages.info(request, f'{product.name} removed from wishlist.')
        else:
            request.user.wishlist.add(product)
            messages.success(request, f'{product.name} added to wishlist.')
    
    return redirect('products:product_detail', id=id, slug=slug)

def search_suggestions(request):
    search = ProductSearch(request)
    suggestions = search.get_suggestions()
    return JsonResponse({'suggestions': suggestions})

def quick_view_product(request, product_id):
    """AJAX endpoint for quick view product details"""
    product = get_object_or_404(Product, id=product_id, available=True)
    
    data = {
        'id': product.id,
        'name': product.name,
        'price': str(product.price),
        'description': product.description[:150] + '...' if len(product.description) > 150 else product.description,
        'image_url': product.get_image_url(),
        'stock': product.stock,
        'url': product.get_absolute_url(),
        'in_stock': product.stock > 0,
        'low_stock': 0 < product.stock <= 5
    }
    
    return JsonResponse(data)
