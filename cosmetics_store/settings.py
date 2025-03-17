"""
Django settings for cosmetics_store project.
"""

import os
from pathlib import Path
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    # Django Admin Theme
    'jazzmin',
    
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party Apps
    'crispy_forms',
    'crispy_tailwind',
    'widget_tweaks',  # Form widget tweaks
    
    # Local Apps
    'users.apps.UsersConfig',
    'products.apps.ProductsConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
    'payment.apps.PaymentConfig',
]

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

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
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'cosmetics_store.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'products:product_list'
LOGOUT_REDIRECT_URL = 'products:product_list'

# Payment Settings
ESEWA_MERCHANT_CODE = 'EPAYTEST'  # Replace with your eSewa merchant code
ESEWA_PAYMENT_URL = 'https://uat.esewa.com.np/epay/main'  # Use production URL in production
ESEWA_SUCCESS_URL = 'https://uat.esewa.com.np/epay/success'  # Use production URL in production
ESEWA_FAILURE_URL = 'https://uat.esewa.com.np/epay/failure'  # Use production URL in production

# Site URL for Payment Callbacks
SITE_URL = 'https://your-domain.com'  # Replace with your actual domain

# Cart Settings
CART_SESSION_ID = 'cart'

# Message Tags
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}

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
