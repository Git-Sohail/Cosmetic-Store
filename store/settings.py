# Payment Settings
ESEWA_MERCHANT_CODE = 'EPAYTEST'  # Replace with your eSewa merchant code
ESEWA_PAYMENT_URL = 'https://uat.esewa.com.np/epay/main'  # Use production URL in production
ESEWA_SUCCESS_URL = 'https://your-domain.com/payment/esewa/callback/'
ESEWA_FAILURE_URL = 'https://your-domain.com/payment/esewa/callback/'

KHALTI_PUBLIC_KEY = 'test_public_key_123'  # Replace with your Khalti public key
KHALTI_SECRET_KEY = 'test_secret_key_123'  # Replace with your Khalti secret key
KHALTI_VERIFY_URL = 'https://khalti.com/api/v2/payment/verify/'  # Use production URL in production

# Email Settings for Payment Notifications
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
DEFAULT_FROM_EMAIL = 'Cosmetics Store <your-email@gmail.com>'

# Site URL for Payment Callbacks
SITE_URL = 'https://your-domain.com'  # Replace with your actual domain

# Add payment app to INSTALLED_APPS
INSTALLED_APPS = [
    # ... existing apps ...
    'payment',
] 