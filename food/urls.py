from django.urls import path
from . import views
from .views import UserLoginView, UserLogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),

    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('indian/', views.indian_food, name='indian_food'),
    path('western/', views.western_food, name='western_food'),

    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.cart, name='cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),

    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
]
