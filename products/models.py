from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category Name")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Category Image")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    GENDER_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('kids', 'Kids'),
        ('unisex', 'Unisex'),
    ]
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Category")
    name = models.CharField(max_length=200, verbose_name="Product Name")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (₹)")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Discount Price")
    stock = models.IntegerField(default=0, verbose_name="Stock Quantity")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Product Image")
    is_available = models.BooleanField(default=True, verbose_name="Available")
    is_featured = models.BooleanField(default=False, verbose_name="Featured Product")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    thumbnail = models.ImageField(upload_to='products/thumbnails/', blank=True, null=True)
    
    # Filter fields
    color = models.CharField(max_length=50, blank=True, null=True, verbose_name="Color")
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='unisex', verbose_name="Gender")
    fabric = models.CharField(max_length=50, blank=True, null=True, verbose_name="Fabric")
    dial_shape = models.CharField(max_length=50, blank=True, null=True, verbose_name="Dial Shape")
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def final_price(self):
        """Return discount price if available else regular price"""
        if self.discount_price:
            return self.discount_price
        return self.price
    
    @property
    def discount_amount(self):
        """Return discount percentage"""
        if self.discount_price:
            discount = ((self.price - self.discount_price) / self.price) * 100
            return round(discount)
        return 0
    
    @property
    def saved_amount(self):
        """Return how much money you save"""
        if self.discount_price:
            return self.price - self.discount_price
        return 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    is_main = models.BooleanField(default=False, verbose_name="Main Image")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} - Image {self.id}"
    
    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"