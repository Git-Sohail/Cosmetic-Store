from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    readonly_fields = ['product_image', 'total_price', 'product_details']
    fields = ['product', 'product_image', 'product_details', 'quantity', 'price', 'total_price']

    def product_image(self, obj):
        if obj.product and obj.product.image:
            return format_html(
                '<img src="{}" style="width: 32px; height: 32px; object-fit: cover; '
                'border-radius: 4px; box-shadow: 0 1px 2px rgba(0,0,0,0.1);" />',
                obj.product.image.url
            )
        return "—"
    product_image.short_description = 'Image'

    def product_details(self, obj):
        if obj.product:
            return format_html(
                '<div style="font-size: 12px;">'
                '<strong>Name:</strong> {}<br>'
                '<strong>Category:</strong> {}<br>'
                '<strong>Stock:</strong> {}<br>'
                '<strong>Price:</strong> ${:.2f}'
                '</div>',
                obj.product.name,
                obj.product.category.name,
                obj.product.stock,
                obj.product.price
            )
        return "—"
    product_details.short_description = 'Product Details'

    def total_price(self, obj):
        if obj.price and obj.quantity:
            total = obj.price * obj.quantity
            return format_html('<span style="color: #2ecc71;">${:.2f}</span>', total)
        return "—"
    total_price.short_description = 'Total'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_info', 'status_badge', 'total_amount', 'created_at', 'customer_location']
    list_filter = ['status', 'created_at']
    search_fields = ['id', 'user__username', 'user__email', 'address', 'phone']
    inlines = [OrderItemInline]
    readonly_fields = ['order_summary', 'created_at', 'updated_at', 'customer_location']
    
    fieldsets = (
        ('Order Information', {
            'fields': (
                'user', 'first_name', 'last_name', 'email', 'phone',
                'address', 'status', 'total_amount', 'notes'
            )
        }),
        ('Customer Location', {
            'fields': ('customer_location',),
            'classes': ('wide',)
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
        return format_html(
            '<div style="font-size: 12px;">'
            '<strong>Name:</strong> {}<br>'
            '<strong>Email:</strong> {}<br>'
            '<strong>Phone:</strong> {}'
            '</div>',
            f"{obj.first_name} {obj.last_name}",
            obj.email,
            obj.phone
        )
    user_info.short_description = 'Customer Info'

    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'processing': 'blue',
            'shipped': 'purple',
            'delivered': 'green',
            'cancelled': 'red'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def customer_location(self, obj):
        return format_html(
            '<div style="font-size: 12px;">'
            '<strong>Address:</strong> {}<br>'
            '<strong>Phone:</strong> {}'
            '</div>',
            obj.address,
            obj.phone
        )
    customer_location.short_description = 'Customer Location'

    def order_summary(self, obj):
        items_html = ''
        for item in obj.items.all():
            items_html += f'''
                <div style="margin-bottom: 10px; padding: 8px; background: #f8f9fa; border-radius: 4px;">
                    <strong>{item.product.name}</strong><br>
                    Quantity: {item.quantity}<br>
                    Price: ${item.price}<br>
                    Total: ${item.get_cost()}
                </div>
            '''
        return format_html(items_html)
    order_summary.short_description = 'Order Items'

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
