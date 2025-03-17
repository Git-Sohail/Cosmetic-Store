import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key'

DEBUG = True

ALLOWED_HOSTS = []

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

INSTALLED_APPS = [
    'jazzmin',  # Beautiful admin interface
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'crispy_forms',
    'crispy_tailwind',
    
    # Local apps
    'users.apps.UsersConfig',
    'products.apps.ProductsConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
    'payment.apps.PaymentConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cosmetics_store.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cosmetics_store.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Admin Interface Customization
JAZZMIN_SETTINGS = {
    "site_title": "Cosmetics Store Admin",
    "site_header": "Cosmetics Store",
    "site_brand": "Cosmetics Store",
    "welcome_sign": "Welcome to the Cosmetics Store Admin Panel",
    "copyright": "Cosmetics Store Ltd",
    "search_model": ["users.User", "products.Product"],
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Site", "url": "/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": False,
    "hide_apps": [],
    "hide_models": [],
    "icons": {
        "auth": "fas fa-users-cog",
        "users.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "products.product": "fas fa-box-open",
        "products.category": "fas fa-tags",
        "orders.order": "fas fa-shopping-cart",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": "admin/css/custom_admin.css",
    "custom_js": None,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Message tags
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}