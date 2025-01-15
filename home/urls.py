from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("shop", views.shop, name="shop"),
    path("about", views.about, name="about"),
    path("services", views.services, name="services"),
    path("blog", views.blog, name="blog"),
    path("contact", views.contact, name="contact"),
]
