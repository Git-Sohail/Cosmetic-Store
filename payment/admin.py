from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'order', 'user', 'amount', 'payment_method', 'status', 'created_at']
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['payment_id', 'order__id', 'user__username', 'transaction_id']
    readonly_fields = ['payment_id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    actions = ['mark_as_completed', 'mark_as_failed', 'mark_as_refunded']

    def mark_as_completed(self, request, queryset):
        for payment in queryset:
            payment.mark_as_completed(
                transaction_id=payment.transaction_id or 'admin_completed',
                payment_details={'admin_action': 'completed'}
            )
        self.message_user(request, f'{queryset.count()} payments marked as completed.')
    mark_as_completed.short_description = 'Mark selected payments as completed'

    def mark_as_failed(self, request, queryset):
        for payment in queryset:
            payment.mark_as_failed({'admin_action': 'failed'})
        self.message_user(request, f'{queryset.count()} payments marked as failed.')
    mark_as_failed.short_description = 'Mark selected payments as failed'

    def mark_as_refunded(self, request, queryset):
        for payment in queryset:
            payment.mark_as_refunded({'admin_action': 'refunded'})
        self.message_user(request, f'{queryset.count()} payments marked as refunded.')
    mark_as_refunded.short_description = 'Mark selected payments as refunded'
