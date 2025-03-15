from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category_detail', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sold_count = models.PositiveIntegerField(default=0)
    wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='wishlist', blank=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id, self.slug])

    def get_image_url(self):
        if self.image:
            return self.image.url
        return '/static/images/no-image.png'

    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0

    def get_rating_distribution(self):
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        reviews = self.reviews.all()
        for review in reviews:
            distribution[review.rating] += 1
        return distribution

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    helpful_votes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='helpful_reviews', blank=True)
    reported = models.BooleanField(default=False)
    moderated = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]
        unique_together = ('product', 'user')

    def __str__(self):
        return f'Review by {self.user.username} on {self.product.name}'

    def get_helpful_count(self):
        return self.helpful_votes.count()

    def toggle_helpful(self, user):
        if user in self.helpful_votes.all():
            self.helpful_votes.remove(user)
            return False
        else:
            self.helpful_votes.add(user)
            return True

    def report(self):
        self.reported = True
        self.save()

    def moderate(self, approved):
        self.moderated = True
        if not approved:
            self.delete()
        self.save()
