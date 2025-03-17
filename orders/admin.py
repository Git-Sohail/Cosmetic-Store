from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    readonly_fields = ['product_image', 'total_price']
    fields = ['product', 'product_image', 'quantity', 'price', 'total_price']

    def product_image(self, obj):
        if obj.product and obj.product.image:
            return format_html(
                '<img src="{}" style="width: 32px; height: 32px; object-fit: cover; '
                'border-radius: 4px; box-shadow: 0 1px 2px rgba(0,0,0,0.1);" />',
                obj.product.image.url
            )
        return "—"
    product_image.short_description = 'Image'

    def total_price(self, obj):
        if obj.price and obj.quantity:
            total = obj.price * obj.quantity
            return format_html('<span style="color: #2ecc71;">${:.2f}</span>', total)
        return "—"
    total_price.short_description = 'Total'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_info', 'status_badge', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['id', 'user__username', 'user__email', 'address']
    inlines = [OrderItemInline]
    readonly_fields = ['order_summary', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': (
                'user', 'first_name', 'last_name', 'email', 'phone',
                'address', 'status', 'total_amount', 'notes'
            )
        }),
        ('Order Summary', {
            'fields': ('order_summary',),
            'classes': ('wide',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def user_info(self, obj):
        if obj.user:
            return format_html(
                '<div style="display: flex; align-items: center; gap: 8px;">'
                '<div style="width: 32px; height: 32px; border-radius: 16px; '
                'background: linear-gradient(45deg, #ff3366, #ff9fb3); '
                'display: flex; align-items: center; justify-content: center; '
                'color: white; font-weight: 500;">{}</div>'
                '<div><strong>{} {}</strong><br/>'
                '<span style="color: #666; font-size: 0.85em;">{}</span></div>'
                '</div>',
                obj.first_name[0].upper() if obj.first_name else obj.user.username[0].upper(),
                obj.first_name,
                obj.last_name,
                obj.email
            )
        return "—"
    user_info.short_description = 'Customer'

    def status_badge(self, obj):
        status_colors = {
            'pending': '#f1c40f',
            'processing': '#3498db',
            'shipped': '#2ecc71',
            'delivered': '#27ae60',
            'cancelled': '#e74c3c'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; '
            'border-radius: 12px; font-size: 0.85em;">{}</span>',
            status_colors.get(obj.status.lower(), '#95a5a6'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def order_summary(self, obj):
        items = obj.items.all()
        if not items:
            return "No items in this order"
        
        summary = '<div style="margin-bottom: 20px;">'
        for item in items:
            summary += format_html(
                '<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">'
                '<img src="{}" style="width: 48px; height: 48px; object-fit: cover; border-radius: 6px;" />'
                '<div style="flex-grow: 1;">'
                '<strong>{}</strong><br/>'
                '<span style="color: #666;">Quantity: {} × ${:.2f}</span>'
                '</div>'
                '<div style="color: #2ecc71; font-weight: 500;">${:.2f}</div>'
                '</div>',
                item.product.image.url if item.product.image else '/static/images/no-image.png',
                item.product.name,
                item.quantity,
                item.price,
                item.quantity * item.price
            )
        
        summary += format_html(
            '<div style="border-top: 1px solid #eee; margin-top: 12px; padding-top: 12px;">'
            '<div style="display: flex; justify-content: space-between; font-weight: 500;">'
            '<span>Total Amount:</span>'
            '<span style="color: #2ecc71; font-size: 1.1em;">${:.2f}</span>'
            '</div></div>',
            obj.total_amount
        )
        
        return format_html(summary + '</div>')
    order_summary.short_description = 'Order Summary'

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
