from django.db import models
from django.contrib.auth.models import User


# =====================
# FOOD
# =====================
class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# =====================
# CART
# =====================
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.food_item.price * self.quantity


# =====================
# ORDER (PERMANENT)
# =====================
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="Pending")


    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    total_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=30,
        choices=[
            ("COD", "Cash on Delivery"),
            ("ONLINE", "Online Payment"),
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.food_item.name} x {self.quantity}"
    