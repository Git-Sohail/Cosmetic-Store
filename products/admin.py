from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_image', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Image', {
            'fields': ('image', 'category_image_preview'),
            'classes': ('wide', 'extrapretty')
        }),
    )

    def category_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; '
                'border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return format_html(
            '<div style="width: 50px; height: 50px; border-radius: 8px; '
            'background: linear-gradient(45deg, #f3f4f6, #e5e7eb); '
            'display: flex; align-items: center; justify-content: center;">'
            '<span style="color: #9ca3af;">No Image</span></div>'
        )
    category_image.short_description = 'Image'

    def category_image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; border-radius: 8px; '
                'box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return "No image uploaded"
    category_image_preview.short_description = 'Image Preview'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ('created_at', 'updated_at', 'category_image_preview')
        return ('category_image_preview',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_image', 'category', 'price', 'stock', 'available', 'created_at')
    list_filter = ('available', 'created_at', 'category')
    list_editable = ('price', 'stock', 'available')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('Image', {
            'fields': ('image', 'product_image_preview'),
            'classes': ('wide', 'extrapretty')
        }),
        ('Pricing and Stock', {
            'fields': ('price', 'stock', 'available'),
            'classes': ('wide',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )

    def product_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; '
                'border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return format_html(
            '<div style="width: 50px; height: 50px; border-radius: 8px; '
            'background: linear-gradient(45deg, #f3f4f6, #e5e7eb); '
            'display: flex; align-items: center; justify-content: center;">'
            '<span style="color: #9ca3af;">No Image</span></div>'
        )
    product_image.short_description = 'Image'

    def product_image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; border-radius: 8px; '
                'box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return "No image uploaded"
    product_image_preview.short_description = 'Image Preview'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ('created_at', 'updated_at', 'product_image_preview', 'sold_count')
        return ('product_image_preview', 'sold_count')

    def make_available(self, request, queryset):
        updated = queryset.update(available=True)
        self.message_user(request, f'{updated} products were marked as available.')
    make_available.short_description = "Mark selected products as available"

    def make_unavailable(self, request, queryset):
        updated = queryset.update(available=False)
        self.message_user(request, f'{updated} products were marked as unavailable.')
    make_unavailable.short_description = "Mark selected products as unavailable"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'helpful_count', 'reported', 'moderated', 'created_at')
    list_filter = ('rating', 'reported', 'moderated', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    readonly_fields = ('helpful_count',)
    actions = ['approve_reviews', 'reject_reviews']

    fieldsets = (
        ('Review Details', {
            'fields': ('product', 'user', 'rating', 'comment')
        }),
        ('Moderation', {
            'fields': ('reported', 'moderated', 'helpful_count'),
            'classes': ('wide',)
        }),
    )

    def helpful_count(self, obj):
        count = obj.get_helpful_count() if obj else 0
        return format_html(
            '<span class="helpful-count">{}</span>',
            count
        )
    helpful_count.short_description = 'Helpful Votes'

    def approve_reviews(self, request, queryset):
        for review in queryset:
            review.moderate(approved=True)
        self.message_user(request, f'{queryset.count()} reviews were approved.')
    approve_reviews.short_description = "Approve selected reviews"

    def reject_reviews(self, request, queryset):
        for review in queryset:
            review.moderate(approved=False)
        self.message_user(request, f'{queryset.count()} reviews were rejected.')
    reject_reviews.short_description = "Reject selected reviews"

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('created_at', 'updated_at', 'product', 'user')
        return self.readonly_fields
