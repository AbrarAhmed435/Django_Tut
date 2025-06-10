import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model extending Django's AbstractUser
class User(AbstractUser):
    pass  # Currently no extra fields; can be extended later


# Product model to represent items that can be ordered
class Product(models.Model):
    name = models.CharField(max_length=100)  # Product name, max length 100 chars
    description = models.TextField()  # Detailed description of the product
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price with 2 decimals
    stock = models.PositiveBigIntegerField()  # Quantity available in stock (non-negative)
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # Optional product image

    @property
    def in_stock(self):
        # Returns True if stock is more than zero, otherwise False
        return self.stock > 0

    def __str__(self):
        # String representation of the product for admin or shell
        return self.name


# Order model representing a customer's order
class Order(models.Model):
    # Choices for order status using Django's TextChoices for convenience
    class StatusChoices(models.TextChoices):
        PENDING = 'Pending'
        CONFIRMED = 'confirmed'
        CANCELLED = 'Cancelled'

    order_id = models.UUIDField(
        primary_key=True,  # Primary key for uniqueness
        default=uuid.uuid4  # Auto-generate a unique UUID
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE  # If user deleted, delete their orders too
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when order is created
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING  # Default status is Pending
    )
    # Many-to-many relationship to Product through intermediate model OrderItem
    product = models.ManyToManyField(
        Product,
        through='OrderItem',
        related_name='orders'  # Allows reverse access from Product to related orders
    )

    def __str__(self):
        # Readable string for orders
        return f"Order {self.order_id} by {self.user.username}"


# Intermediate model to store additional info for many-to-many relationship between Order and Product
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE  # Delete items if order is deleted
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE  # Delete items if product is deleted
    )
    quantity = models.PositiveIntegerField()  # Quantity of this product in the order (must be positive)

    @property
    def item_subtotal(self):
        # Calculates total price for this item line = price * quantity
        return self.product.price * self.quantity

    def __str__(self):
        # String representation showing quantity, product, and order info
        return f"{self.quantity}X {self.product.name} in Order {self.order.order_id}"
