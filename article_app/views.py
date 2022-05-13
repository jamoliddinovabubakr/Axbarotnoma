from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from .models import Article, Category, Shartnoma
from .forms import AddArticleForm
from user_app.forms import UpdateUserForm1


def main_page(request):
    context = {
        'menus': '',
    }
    return render(request, "article_app/main.html", context=context)


def add_article(request):
    user = request.user
    print("1")
    if request.method == "POST":
        print("2")
        form = AddArticleForm(request.POST, request.FILES)
        if form.is_valid():
            print("3")
            article = form.save(commit=False)
            article.save()
            print("4")
            return redirect('profile_page')
    else:
        context = {
            'form': AddArticleForm(),
            'user': user,
            'shartnoma1': Shartnoma.objects.get(name='shartnoma1'),
            'shartnoma2': Shartnoma.objects.get(name='shartnoma2'),
        }
        return render(request, "article_app/add_article.html", context=context)



