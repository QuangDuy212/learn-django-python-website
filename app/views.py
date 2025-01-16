from django.shortcuts import render
from django.http import HttpResponse
from .models import *


# Create your views here.
def index(request):
    products = Product.objects.all()[:3]
    context = {"products": products}
    return render(request, "home.html", context)


def shop(request):
    context = {}
    return render(request, "shop.html", context)


def about(request):
    context = {}
    return render(request, "about.html", context)


def services(request):
    context = {}
    return render(request, "services.html", context)


def blog(request):
    context = {}
    return render(request, "blog.html", context)


def contact(request):
    context = {}
    return render(request, "contact.html", context)
