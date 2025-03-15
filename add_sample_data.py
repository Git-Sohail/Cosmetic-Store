import os
import django
from django.utils.text import slugify
from decimal import Decimal
from django.core.files import File
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetics_store.settings')
django.setup()

from products.models import Category, Product

# Sample categories with images
categories = [
    {
        'name': 'Makeup',
        'description': 'Professional makeup products for all occasions',
        'image': 'categories/2025/03/14/makeup-category.jpg',
        'products': [
            {
                'name': 'Matte Lipstick - Ruby Red',
                'description': 'Long-lasting matte lipstick in a classic red shade',
                'price': 24.99,
                'stock': 50,
                'image': 'products/2025/03/14/matte-lipstick-red.jpg',
            },
            {
                'name': 'Foundation - Natural Beige',
                'description': '24-hour wear foundation with natural finish',
                'price': 34.99,
                'stock': 30,
                'image': 'products/2025/03/14/foundation-beige.jpg',
            },
            {
                'name': 'Eyeshadow Palette - Nude',
                'description': '12-color nude eyeshadow palette',
                'price': 45.99,
                'stock': 25,
                'image': 'products/2025/03/14/nude-palette.jpg',
            },
        ]
    },
    {
        'name': 'Skincare',
        'description': 'Natural and effective skincare products',
        'image': 'categories/2025/03/14/skincare-category.jpg',
        'products': [
            {
                'name': 'Hydrating Face Cream',
                'description': 'Deeply moisturizing face cream with hyaluronic acid',
                'price': 29.99,
                'stock': 40,
                'image': 'products/2025/03/14/face-cream.jpg',
            },
            {
                'name': 'Vitamin C Serum',
                'description': 'Brightening serum with 20% vitamin C',
                'price': 49.99,
                'stock': 35,
                'image': 'products/2025/03/14/vitamin-c-serum.jpg',
            },
            {
                'name': 'Gentle Cleanser',
                'description': 'pH-balanced gentle facial cleanser',
                'price': 19.99,
                'stock': 60,
                'image': 'products/2025/03/14/cleanser.jpg',
            },
        ]
    },
    {
        'name': 'Hair Care',
        'description': 'Professional hair care products',
        'image': 'categories/2025/03/14/haircare-category.jpg',
        'products': [
            {
                'name': 'Shampoo - Repair & Restore',
                'description': 'Repairing shampoo for damaged hair',
                'price': 27.99,
                'stock': 45,
                'image': 'products/2025/03/14/repair-shampoo.jpg',
            },
            {
                'name': 'Conditioner - Deep Moisture',
                'description': 'Deep conditioning treatment for dry hair',
                'price': 27.99,
                'stock': 45,
                'image': 'products/2025/03/14/deep-conditioner.jpg',
            },
            {
                'name': 'Hair Oil - Argan',
                'description': 'Pure argan oil for hair treatment',
                'price': 39.99,
                'stock': 30,
                'image': 'products/2025/03/14/argan-oil.jpg',
            },
        ]
    },
    {
        'name': 'Fragrances',
        'description': 'Luxury fragrances and perfumes',
        'image': 'categories/2025/03/14/fragrances-category.jpg',
        'products': [
            {
                'name': 'Floral Perfume - Spring Blossom',
                'description': 'Light and fresh floral fragrance',
                'price': 59.99,
                'stock': 25,
                'image': 'products/2025/03/14/spring-perfume.jpg',
            },
            {
                'name': 'Woody Cologne - Forest Mist',
                'description': 'Rich woody fragrance for men',
                'price': 49.99,
                'stock': 30,
                'image': 'products/2025/03/14/forest-cologne.jpg',
            },
            {
                'name': 'Vanilla Body Mist',
                'description': 'Sweet vanilla body mist',
                'price': 24.99,
                'stock': 40,
                'image': 'products/2025/03/14/vanilla-mist.jpg',
            },
        ]
    },
    {
        'name': 'Tools & Brushes',
        'description': 'Professional makeup tools and brushes',
        'image': 'categories/2025/03/14/tools-category.jpg',
        'products': [
            {
                'name': 'Foundation Brush Set',
                'description': 'Set of 3 professional foundation brushes',
                'price': 39.99,
                'stock': 20,
                'image': 'products/2025/03/14/foundation-brushes.jpg',
            },
            {
                'name': 'Eye Shadow Brush Set',
                'description': 'Complete set of eyeshadow brushes',
                'price': 29.99,
                'stock': 30,
                'image': 'products/2025/03/14/eyeshadow-brushes.jpg',
            },
            {
                'name': 'Beauty Blender',
                'description': 'Original beauty sponge for flawless application',
                'price': 19.99,
                'stock': 50,
                'image': 'products/2025/03/14/beauty-blender.jpg',
            },
        ]
    }
]

def add_sample_data():
    for category_data in categories:
        # Create or get category
        category, created = Category.objects.get_or_create(
            name=category_data['name'],
            slug=slugify(category_data['name']),
            defaults={
                'description': category_data['description']
            }
        )
        
        # Set category image if it was just created
        if created:
            image_path = os.path.join(settings.MEDIA_ROOT, category_data['image'])
            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    category.image.save(
                        os.path.basename(image_path),
                        File(f),
                        save=True
                    )
            print(f"Created category: {category.name}")
        else:
            print(f"Using existing category: {category.name}")

        # Create products for this category
        for product_data in category_data['products']:
            product, created = Product.objects.get_or_create(
                category=category,
                name=product_data['name'],
                slug=slugify(product_data['name']),
                defaults={
                    'description': product_data['description'],
                    'price': Decimal(str(product_data['price'])),
                    'stock': product_data['stock']
                }
            )
            
            # Set product image if it was just created
            if created:
                image_path = os.path.join(settings.MEDIA_ROOT, product_data['image'])
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        product.image.save(
                            os.path.basename(image_path),
                            File(f),
                            save=True
                        )
                print(f"Created product: {product.name}")
            else:
                print(f"Using existing product: {product.name}")

if __name__ == '__main__':
    add_sample_data() 