from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages


def paginate_queryset(queryset, page, per_page=10):
    """
    Hàm phân trang dữ liệu.

    Args:
        queryset: Queryset hoặc danh sách dữ liệu cần phân trang.
        page: Số trang hiện tại (lấy từ request.GET['page']).
        per_page: Số lượng bản ghi trên mỗi trang (mặc định là 10).

    Returns:
        Một tuple gồm:
        - page_obj: Trang dữ liệu hiện tại.
        - is_paginated: True nếu dữ liệu được phân trang, False nếu không.
    """
    paginator = Paginator(queryset, per_page)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        # Nếu `page` không phải số, trả về trang đầu tiên
        page_obj = paginator.page(1)
    except EmptyPage:
        # Nếu `page` vượt quá số lượng trang, trả về trang cuối cùng
        page_obj = paginator.page(paginator.num_pages)

    is_paginated = paginator.num_pages > 1  # Kiểm tra có cần phân trang hay không
    total = paginator.num_pages
    return page_obj, is_paginated, total


# Create your views here.
def index(request):
    products = Product.objects.all()[:3]
    context = {"products": products}
    return render(request, "home.html", context)


def auth(request):
    context = {}
    return render(request, "auth.html", context)


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "auth.html")


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            Customer.objects.create(user=user, name=username, email=email)
            messages.success(request, "Account created successfully")
            return redirect("login")
    return render(request, "auth.html")


def shop(request):
    products = Product.objects.all()
    page_number = request.GET.get("page")  # Lấy số trang từ URL
    try:
        page_obj, is_paginated, total = paginate_queryset(products, page_number)
    except Http404:
        page_obj, is_paginated, total = paginate_queryset(products, 1)
    products = Product.objects.all()
    if is_paginated:
        numbers = range(1, total + 1)
    else:
        numbers = range(1)
    context = {
        "products": products,
        "page_objs": page_obj,
        "numbers": numbers,
        "total": total,
    }
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


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart = Cart.objects.get(customer=customer)
        items = cart.items.all()
        total = sum([item.Total for item in items])
    else:
        items = []
        total = 0
    context = {"items": items, "total": total}
    return render(request, "cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart = Cart.objects.get(customer=customer)
        items = cart.items.all()
        total = sum([item.Total for item in items])
    else:
        items = []
        total = 0
    context = {"items": items, "total": total}
    return render(request, "checkout.html", context)


def order(request):
    if request.method == "POST":
        # Lấy dữ liệu từ form
        first_name = request.POST.get("c_fname")
        last_name = request.POST.get("c_lname")
        address = request.POST.get("c_address")
        country = request.POST.get("c_state_country")
        email = request.POST.get("c_email_address")
        phone = request.POST.get("c_phone")
        note = request.POST.get("c_order_notes")
        if request.user.is_authenticated:
            customer = request.user.customer
            cart = Cart.objects.get(customer=customer)
            items = cart.items.all()
            total = sum([item.Total for item in items])
        else:
            items = []
            total = 0
        order = Order.objects.create(customer=request.user.customer)
        order.firstname = first_name
        order.lastname = last_name
        order.address = address
        order.state = country
        order.email = email
        order.phone = phone
        order.note = note
        order.save()
        for item in items:
            order_item = OrderItem.objects.create(product=item.product, order=order)
            order_item.quantity = item.quantity
            order_item.save()
        # Xử lý dữ liệu form (ví dụ: lưu vào cơ sở dữ liệu)
        # ...

        # Chuyển hướng đến trang cảm ơn sau khi đặt hàng thành công
        return redirect("thankyou")


def thankyou(request):
    context = {}
    return render(request, "thankyou.html", context)


def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    cart, created = Cart.objects.get_or_create(customer=request.user.customer)
    if cart is None:
        cart = Cart.objects.create(customer=request.user.customer)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if cart_item is not None:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()
    cart.save()
    return redirect("shop")


def add_quantity(request, id, quantity):
    cart_item = CartItem.objects.get(id=id)
    if quantity == "1":
        cart_item.quantity += 1
    elif quantity == "-1":
        cart_item.quantity -= 1
    cart_item.save()
    return redirect("cart")


def remove_from_cart(request, id):
    cart_item = CartItem.objects.get(id=id)
    cart_item.delete()
    return redirect("cart")
