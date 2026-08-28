from django.db import models
from django.contrib.auth.models import User

        
class Item(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

class Products(models.Model):

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    owner_name = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Products"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    ordered_at = models.DateTimeField(auto_now_add=True)
    STATUS_PENDING = 'pending'
    STATUS_SHIPPED = 'shipped'
    STATUS_DELIVERED = 'delivered'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_SHIPPED, 'Shipped'),
        (STATUS_DELIVERED, 'Delivered'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    def __str__(self):
        return f"{self.product.name} - {self.user.username}"
    
    class Meta:
        ordering = ['-ordered_at']
        verbose_name_plural = "Orders"
    
    def save(self, *args, **kwargs):
        # ensure total_price is consistent with product price and quantity
        try:
            unit_price = self.product.price
        except Exception:
            unit_price = 0
        self.total_price = unit_price * (self.quantity or 1)
        super().save(*args, **kwargs)