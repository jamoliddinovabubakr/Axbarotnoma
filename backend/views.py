from django.shortcuts import render
from .models import Menu


def home(request):
    menus = Menu.objects.filter(status=True).filter(parent_id=0)
    context = {
        'menus': menus,
    }
    return render(request, "backend/content/home.html", context=context)


def login_page(request):
    return render(request, "backend/register/login.html")