from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product, Category

class ProductSearch:
    def __init__(self, request):
        self.request = request
        self.query = request.GET.get('search', '')
        self.category = request.GET.get('category', '')
        self.min_price = request.GET.get('min_price', '')
        self.max_price = request.GET.get('max_price', '')
        self.sort_by = request.GET.get('sort', '')
        self.in_stock = request.GET.get('in_stock', '')
        self.page = request.GET.get('page', 1)
        self.per_page = 12

    def get_queryset(self):
        queryset = Product.objects.filter(available=True)

        # Search by name or description
        if self.query:
            queryset = queryset.filter(
                Q(name__icontains=self.query) |
                Q(description__icontains=self.query)
            )

        # Filter by category
        if self.category:
            queryset = queryset.filter(category__slug=self.category)

        # Filter by price range
        if self.min_price:
            queryset = queryset.filter(price__gte=float(self.min_price))
        if self.max_price:
            queryset = queryset.filter(price__lte=float(self.max_price))

        # Filter by stock status
        if self.in_stock == 'true':
            queryset = queryset.filter(stock__gt=0)

        # Apply sorting
        if self.sort_by:
            if self.sort_by == 'name_asc':
                queryset = queryset.order_by('name')
            elif self.sort_by == 'name_desc':
                queryset = queryset.order_by('-name')
            elif self.sort_by == 'price_asc':
                queryset = queryset.order_by('price')
            elif self.sort_by == 'price_desc':
                queryset = queryset.order_by('-price')
            elif self.sort_by == 'newest':
                queryset = queryset.order_by('-created_at')
            elif self.sort_by == 'popularity':
                queryset = queryset.order_by('-sold_count')

        return queryset

    def get_suggestions(self):
        if len(self.query) < 3:
            return []

        suggestions = Product.objects.filter(
            Q(name__icontains=self.query) |
            Q(description__icontains=self.query)
        ).values_list('name', flat=True)[:5]

        return list(suggestions)

    def get_price_range(self):
        min_price = Product.objects.filter(available=True).order_by('price').first()
        max_price = Product.objects.filter(available=True).order_by('-price').first()
        return {
            'min': min_price.price if min_price else 0,
            'max': max_price.price if max_price else 0
        }

    def get_categories(self):
        return Category.objects.all()

    def get_results(self):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.per_page)
        products = paginator.get_page(self.page)

        return {
            'products': products,
            'suggestions': self.get_suggestions() if self.query else [],
            'price_range': self.get_price_range(),
            'categories': self.get_categories(),
            'total_results': queryset.count(),
            'query': self.query,
            'category': self.category,
            'min_price': self.min_price,
            'max_price': self.max_price,
            'sort_by': self.sort_by,
            'in_stock': self.in_stock
        } 