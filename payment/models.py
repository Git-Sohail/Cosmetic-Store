from django.db import models
from django.conf import settings
from orders.models import Order

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('esewa', 'eSewa'),
        ('khalti', 'Khalti'),
    )
    
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )

    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    payment_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['payment_id']),
            models.Index(fields=['order']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f'Payment {self.payment_id} for Order {self.order.id}'

    def mark_as_completed(self, transaction_id, payment_details):
        self.status = 'completed'
        self.transaction_id = transaction_id
        self.payment_details = payment_details
        self.save()
        self.order.mark_as_paid()

    def mark_as_failed(self, payment_details):
        self.status = 'failed'
        self.payment_details = payment_details
        self.save()

    def mark_as_refunded(self, payment_details):
        self.status = 'refunded'
        self.payment_details = payment_details
        self.save()
        self.order.mark_as_refunded()
