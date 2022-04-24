from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect


def main_page(request):
    context = {
        'menus': '',
    }
    return render(request, "article_app/main.html", context=context)





