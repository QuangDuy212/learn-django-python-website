from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_page, name="login"),
    path("logout", views.logout_page, name="logout"),
    path("shop", views.shop, name="shop"),
    path("about", views.about, name="about"),
    path("services", views.services, name="services"),
    path("blog", views.blog, name="blog"),
    path("contact", views.contact, name="contact"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("thankyou", views.thankyou, name="thankyou"),
    path("cart/<str:id>", views.add_to_cart, name="add_to_cart"),
    path("order", views.order, name="order"),
    path("cart/delete/<str:id>", views.remove_from_cart, name="remove_from_cart"),
    path(
        "cart/quantity/<str:id>/<str:quantity>",
        views.add_quantity,
        name="cart_quantity",
    ),
]
