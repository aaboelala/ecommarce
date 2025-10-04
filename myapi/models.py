from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from ecommerceapp import settings

# Create your models here.

class UserModel(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    slug=models.SlugField(unique=True , blank=True)
    description = models.TextField()
    image=models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    rating=models.ForeignKey('Rating',on_delete=models.CASCADE,related_name='products',null=True,blank=True)
    

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(self.name)
            if Product.objects.filter(slug=self.slug).exists():
                count = 1
                new_slug = f"{self.slug}-{count}"
                while Product.objects.filter(slug=new_slug).exists():
                    count += 1
                    new_slug = f"{self.slug}-{count}"
                self.slug = new_slug
        super().save(*args, **kwargs)
        

            
        
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    image=models.ImageField(upload_to='category/')
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)


    def __str__(self):
        return self.name
    
    
    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(self.name)
            if Category.objects.filter(slug=self.slug).exists():
                count = 1
                new_slug = f"{self.slug}-{count}"
                while Category.objects.filter(slug=new_slug).exists():
                    count += 1
                    new_slug = f"{self.slug}-{count}"
                self.slug = new_slug
        super().save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cart_code = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"Cart of {self.cart_code}"
    
    def total_price(self):
        total = sum(item.get_total_price() for item in self.items.all())
        return total
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart of {self.cart.user.username}"
    
    def get_total_price(self):
        return self.quantity * self.product.price
    


class Rating(models.Model):

    RATING_CHOICES = [
    (1, '1 poor'),
    (2, '2 fair'),
    (3, '3 good'),
    (4, '4 very good'),
    (5, '5 excellent'),
]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(choices=RATING_CHOICES)
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Rating {self.score} by {self.user.username} for {self.product.name}"
    
    class Meta:
        unique_together = ('product', 'user')
        ordering = ['-created_at']

class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_ratings')
    average_rating = models.FloatField(default=0.0)
    total_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Average Rating for {self.product.name}: {self.average_rating} based on {self.total_reviews} reviews"
    
    
class Wishlist(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='wishlist')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="wishlist_user")  
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('product', 'user')

       

class Order(models.Model):
    stripe_checkout_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    customer_email = models.EmailField()
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Paid", "Paid")])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.stripe_checkout_id} - {self.status}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"Order {self.product.name} - {self.order.stripe_checkout_id}"
    



    

