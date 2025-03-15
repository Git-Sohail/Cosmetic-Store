from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Payment

@receiver(post_save, sender=Payment)
def handle_payment_status_change(sender, instance, created, **kwargs):
    """Handle payment status changes and send notifications"""
    if not created:  # Only handle updates
        payment = instance
        order = payment.order
        user = payment.user

        # Send email notifications based on payment status
        if payment.status == 'completed':
            subject = f'Payment Successful - Order #{order.id}'
            message = f'''
            Dear {user.get_full_name() or user.username},

            Your payment of Rs. {payment.amount} for Order #{order.id} has been completed successfully.

            Payment Details:
            - Amount: Rs. {payment.amount}
            - Method: {payment.get_payment_method_display()}
            - Transaction ID: {payment.transaction_id}

            Thank you for shopping with us!

            Best regards,
            Cosmetics Store Team
            '''
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )

        elif payment.status == 'failed':
            subject = f'Payment Failed - Order #{order.id}'
            message = f'''
            Dear {user.get_full_name() or user.username},

            We're sorry, but your payment for Order #{order.id} has failed.

            Payment Details:
            - Amount: Rs. {payment.amount}
            - Method: {payment.get_payment_method_display()}

            Please try again or contact our support team if you need assistance.

            Best regards,
            Cosmetics Store Team
            '''
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )

        elif payment.status == 'refunded':
            subject = f'Payment Refunded - Order #{order.id}'
            message = f'''
            Dear {user.get_full_name() or user.username},

            Your payment for Order #{order.id} has been refunded.

            Refund Details:
            - Amount: Rs. {payment.amount}
            - Method: {payment.get_payment_method_display()}
            - Transaction ID: {payment.transaction_id}

            If you have any questions, please contact our support team.

            Best regards,
            Cosmetics Store Team
            '''
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            ) 