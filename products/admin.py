from django.contrib import admin
from .models import Category, Product, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created_at']
    list_filter = ['available', 'created_at', 'updated_at', 'category']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    date_hierarchy = 'created_at'
    ordering = ['name']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at', 'reported', 'moderated', 'helpful_count']
    list_filter = ['rating', 'created_at', 'reported', 'moderated']
    search_fields = ['product__name', 'user__username', 'comment']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    raw_id_fields = ['product', 'user']
    readonly_fields = ['created_at', 'updated_at', 'helpful_votes']
    actions = ['approve_reviews', 'reject_reviews', 'mark_as_moderated']

    def helpful_count(self, obj):
        return obj.get_helpful_count()
    helpful_count.short_description = 'Helpful Votes'

    def approve_reviews(self, request, queryset):
        for review in queryset:
            review.moderate(approved=True)
        self.message_user(request, f'{queryset.count()} reviews were approved.')
    approve_reviews.short_description = 'Approve selected reviews'

    def reject_reviews(self, request, queryset):
        for review in queryset:
            review.moderate(approved=False)
        self.message_user(request, f'{queryset.count()} reviews were rejected and deleted.')
    reject_reviews.short_description = 'Reject selected reviews'

    def mark_as_moderated(self, request, queryset):
        queryset.update(moderated=True)
        self.message_user(request, f'{queryset.count()} reviews were marked as moderated.')
    mark_as_moderated.short_description = 'Mark selected reviews as moderated'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('helpful_votes')
