import os
import django
import requests
from urllib.parse import urljoin

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetics_store.settings')
django.setup()

from django.conf import settings

# Create necessary directories
category_dir = os.path.join(settings.MEDIA_ROOT, 'categories', '2025', '03', '14')
product_dir = os.path.join(settings.MEDIA_ROOT, 'products', '2025', '03', '14')
default_dir = os.path.join(settings.MEDIA_ROOT, 'default')

for directory in [category_dir, product_dir, default_dir]:
    os.makedirs(directory, exist_ok=True)

# Using picsum.photos for placeholder images
BASE_URL = "https://picsum.photos/"

# Category images
category_images = {
    'makeup-category.jpg': f"{BASE_URL}800/400",
    'skincare-category.jpg': f"{BASE_URL}800/400",
    'haircare-category.jpg': f"{BASE_URL}800/400",
    'fragrances-category.jpg': f"{BASE_URL}800/400",
    'tools-category.jpg': f"{BASE_URL}800/400",
}

# Product images
product_images = {
    'matte-lipstick-red.jpg': f"{BASE_URL}400/400",
    'foundation-beige.jpg': f"{BASE_URL}400/400",
    'nude-palette.jpg': f"{BASE_URL}400/400",
    'face-cream.jpg': f"{BASE_URL}400/400",
    'vitamin-c-serum.jpg': f"{BASE_URL}400/400",
    'cleanser.jpg': f"{BASE_URL}400/400",
    'repair-shampoo.jpg': f"{BASE_URL}400/400",
    'deep-conditioner.jpg': f"{BASE_URL}400/400",
    'argan-oil.jpg': f"{BASE_URL}400/400",
    'spring-perfume.jpg': f"{BASE_URL}400/400",
    'forest-cologne.jpg': f"{BASE_URL}400/400",
    'vanilla-mist.jpg': f"{BASE_URL}400/400",
    'foundation-brushes.jpg': f"{BASE_URL}400/400",
    'eyeshadow-brushes.jpg': f"{BASE_URL}400/400",
    'beauty-blender.jpg': f"{BASE_URL}400/400",
}

def download_image(url, filepath):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded: {filepath}")
            return True
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
    return False

def download_all_images():
    # Download category images
    for filename, url in category_images.items():
        filepath = os.path.join(category_dir, filename)
        download_image(url, filepath)

    # Download product images
    for filename, url in product_images.items():
        filepath = os.path.join(product_dir, filename)
        download_image(url, filepath)

    # Download a default image
    default_image_path = os.path.join(default_dir, 'no-image.jpg')
    download_image(f"{BASE_URL}400/400", default_image_path)

if __name__ == '__main__':
    download_all_images() 