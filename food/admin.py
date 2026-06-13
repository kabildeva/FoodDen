from django.contrib import admin
from .models import FoodItem, Cart, CartItem, Order, OrderItem

# Basic models
admin.site.register(FoodItem)
admin.site.register(Cart)
admin.site.register(CartItem)

# Inline Order Items inside Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

# Register Order ONLY ONCE (with inline)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ("id", "user", "total_amount", "is_paid", "created_at")
