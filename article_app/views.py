from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Article, Category, Shartnoma
from .forms import CreateArticleForm, UpdateArticleForm


def main_page(request):
    context = {
        'menus': '',
    }
    return render(request, "article_app/main.html", context=context)


def my_articles(request):
    user = request.user
    get_my_articles = Article.objects.filter(author=user)
    context = {
        'user': user,
        'my_articles': get_my_articles,
    }
    return render(request, "article_app/my_articles.html", context=context)


def create_article(request):
    user = request.user
    if request.method == "POST":
        form = CreateArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            id = article.id
            return HttpResponseRedirect(f'/update_my_article/{id}/')
    else:
        context = {
            'form': CreateArticleForm(),
            'user': user,
        }
        return render(request, "article_app/crud/create_article.html", context=context)


def update_my_article(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        form = UpdateArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            ob = form.save(commit=False)
            ob.save()
            return redirect('my_articles')
    else:
        context = {
            'form': UpdateArticleForm(instance=article),
        }
        return render(request, "article_app/crud/update_article.html", context=context)
