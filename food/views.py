from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import FoodItem, Cart, CartItem, Order, OrderItem
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

# ---------- AUTH ----------

def login_view(request):
    if 'email' in request.POST:
        User.objects.create_user(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password')
        )
        return redirect('login')

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'app/login.html')


def home(request):
    return render(request, 'app/home.html')


# ---------- FOOD MENUS ----------

def indian_food(request):
    foods = FoodItem.objects.filter(category='Indian')
    return render(request, 'app/indian_food.html', {'foods': foods})


def western_food(request):
    foods = FoodItem.objects.filter(category="Western")
    print(foods)
    return render(request, 'app/western_food.html', {'foods': foods})



# ---------- CART ----------

@login_required
def add_to_cart(request, food_id):
    if request.method == "POST":
        food = get_object_or_404(FoodItem, id=food_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            food_item=food
        )

        if not created:
            item.quantity += 1
        item.save()

        total_items = CartItem.objects.filter(cart=cart).count()

        return JsonResponse({
            "success": True,
            "cart_count": total_items
        })

    return JsonResponse({"success": False})


@login_required
def cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'app/cart.html', {'cart': cart})


@login_required
@require_POST
@login_required
def update_cart(request):
    item_id = request.POST.get("item_id")
    action = request.POST.get("action")

    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if action == "inc":
        item.quantity += 1
        item.save()
    elif action == "dec":
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
            return JsonResponse({
                "removed": True,
                "cart_total": item.cart.total_price
            })
        item.save()

    return JsonResponse({
        "removed": False,
        "quantity": item.quantity,
        "item_total": item.subtotal,
        "cart_total": item.cart.total_price
    })
@login_required
def clear_cart(request):
    if request.method == "POST":
        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})

def cart_count(request):
    if request.user.is_authenticated:
        from .models import Cart
        cart = Cart.objects.filter(user=request.user).first()
        return {'cart_count': cart.items.count() if cart else 0}
    return {'cart_count': 0}

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)

    if not cart.items.exists():
        messages.error(request, "Your cart is empty")
        return redirect("cart")

    return render(request, "app/checkout.html", {"cart": cart})


@login_required
def place_order(request):
    if request.method != "POST":
        return redirect("checkout")

    cart = Cart.objects.get(user=request.user)

    if not cart.items.exists():
        messages.error(request, "Cart is empty")
        return redirect("cart")

    # Create Order
    order = Order.objects.create(
        user=request.user,
        name=request.POST["name"],
        phone=request.POST["phone"],
        address=request.POST["address"],
        payment_method=request.POST["payment"],
        total_amount=cart.total_price,
        is_paid=False
    )

    # Save Order Items
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            food_item=item.food_item,
            quantity=item.quantity
        )

    # Clear Cart
    cart.items.all().delete()

    messages.success(request, "Order placed successfully 🎉")
    return redirect("home")

class UserLoginView(LoginView):
    template_name = 'app/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy('home')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')