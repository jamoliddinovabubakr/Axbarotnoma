from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from .models import Article, Category, Shartnoma, Authors
from .forms import CreateArticleForm, UpdateArticleForm, AddAuthorForm


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
    authors = Authors.objects.filter(article=article)
    if request.method == "POST":
        form = UpdateArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            print("OK")
            ob = form.save(commit=False)
            ob.save()
            return redirect('my_articles')
    else:
        context = {
            'form': UpdateArticleForm(instance=article),
            'authors': authors,
            'article': article
        }
        return render(request, "article_app/crud/update_article.html", context=context)


def add_author(request, pk):
    user = request.user
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.save()
            return redirect('update_my_article', pk=pk)
    else:
        context = {
            'form': AddAuthorForm(),
            'user': user,
            'article': article,
        }
        return render(request, "article_app/crud/add_authors.html", context=context)


def edit_author(request, pk, id):
    author = Authors.objects.get(pk=pk)
    if request.method == "POST":
        form = AddAuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('update_my_article', pk=author.article.id)
        else:
            return redirect('profile')
    else:
        form = AddAuthorForm(instance=author)
        context = {
            'form': form,
            'author': author,
        }
        return render(request, "article_app/crud/edit_author.html", context=context)


def delete_author(request, pk):
    author = Authors.objects.get(pk=pk)
    if request.method == "POST":
        author.delete()
        return redirect('update_my_article', pk=author.article.id)
    else:
        return render(request, 'article_app/crud/delete_author.html', {'author': author})