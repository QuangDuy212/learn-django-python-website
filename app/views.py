from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404


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


def shop(request):
    products = Product.objects.all()
    page_number = request.GET.get("page")  # Lấy số trang từ URL
    try:
        page_obj, is_paginated, total = paginate_queryset(products, page_number, 1)
    except Http404:
        page_obj, is_paginated, total = paginate_queryset(products, 1, 1)
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
    context = {}
    return render(request, "cart.html", context)
