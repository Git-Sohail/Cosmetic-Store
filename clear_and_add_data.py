import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetics_store.settings')
django.setup()

from products.models import Category, Product

def clear_data():
    print("Clearing existing data...")
    products_count = Product.objects.count()
    categories_count = Category.objects.count()
    
    Product.objects.all().delete()
    Category.objects.all().delete()
    
    print(f"Removed {products_count} products and {categories_count} categories.")

def verify_data():
    print("\nVerifying current data:")
    print(f"Categories: {Category.objects.count()}")
    print(f"Products: {Product.objects.count()}")
    print("\nCategories and their products:")
    for category in Category.objects.all():
        print(f"- {category.name}: {category.products.count()} products")

if __name__ == '__main__':
    print("=== Starting data reset and population ===")
    clear_data()
    
    print("\n=== Adding sample data ===")
    from add_sample_data import add_sample_data
    add_sample_data()
    
    print("\n=== Final verification ===")
    verify_data() 