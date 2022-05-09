from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from .models import Article, Category
from .forms import AddArticleForm


def main_page(request):
    context = {
        'menus': '',
    }
    return render(request, "article_app/main.html", context=context)


def add_article(request):
    if request.method == "POST":
        form = AddArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            return redirect('profile_page')
    else:
        context = {
            'form': AddArticleForm(),
        }
        return render(request, "article_app/add_article.html", context=context)


