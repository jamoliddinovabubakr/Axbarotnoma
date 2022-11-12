from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Model
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import translation

from user_app.decorators import allowed_users
from article_app.models import *
from user_app.models import Author
from article_app.forms import CreateArticleForm, UpdateArticleForm, CreateArticleFileForm
from django.core.paginator import Paginator


def main_page(request):
    user_language = 'uz'
    post = Post.objects.last()
    context = {
        'post': post,
    }
    return render(request, "article_app/main.html", context=context)


def post_detail(request, slug):
    post = get_object_or_404(Post, url=slug)
    context = {
        'post': post,
    }
    return render(request, "article_app/post_detail.html", context=context)


@login_required(login_url='login')
def my_articles(request):
    user = request.user
    get_my_articles = Article.objects.filter(author=user).filter(
            Q(state__id=2) | Q(state__id=3)
        )
    paginator = Paginator(get_my_articles, 10)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    p_n = paginator.count
    page_count = page.paginator.page_range

    context = {
        'user': user,
        'my_articles': get_my_articles,
        'page_count': page_count,
        'page': page,
        'p_n': p_n,
    }
    return render(request, "article_app/my_articles.html", context=context)


@login_required(login_url='login')
def create_article(request):
    user = request.user
    author = Author.objects.get(user=user)
    if request.method == "POST":
        form = CreateArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.article_status_id = 7
            article.save()
            return redirect('update_article', pk=article.id)
        else:
            context = {
                'form': CreateArticleForm(),
                'author': author,
            }
            return render(request, "article_app/crud/create_article.html", context=context)
    else:
        context = {
            'form': CreateArticleForm(),
            'author': author,
        }
        return render(request, "article_app/crud/create_article.html", context=context)


@login_required(login_url='login')
def update_article(request, pk):
    user = request.user
    article = Article.objects.get(pk=pk)
    author = Author.objects.get(user=user)
    if user != author.user:
        return render(request, 'user_app/not_access.html')

    if request.method == "POST":
        form = UpdateArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            submit = ArticleStatus.objects.get(pk=1)
            ob = form.save(commit=False)
            ob.article_status = submit
            ob.save()

            return redirect('dashboard')
        else:
            context = {
                'form': UpdateArticleForm(instance=article),
                'article': article,
                'handle_error': 1,
            }
            return render(request, "article_app/crud/update_article.html", context=context)
    else:
        context = {
            'form': UpdateArticleForm(instance=article),
            'article': article,
            'handle_error': 0,
        }
        return render(request, "article_app/crud/update_article.html", context=context)


def create_article_file(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        form = CreateArticleFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.save()
            article.file = file
            article.save()
            data = {
                'result': 'success',
                'message': 'Created File Successfully!.'
            }
            return redirect('update_article', article.id)
        else:
            context = {
                'form': UpdateArticleForm(instance=article),
                'article': article,
                'message': "Form invalid!",
            }
            return render(request, "article_app/crud/update_article.html", context=context)
    else:
        context = {
            'form': CreateArticleFileForm(),
            'article': article,
        }
        return render(request, "article_app/crud/create_file.html", context=context)


@login_required(login_url='login')
def article_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    document = None
    if article.file is not None:
        ob = ArticleFile.objects.filter(article_id=article.id).filter(file_status=1).last()
        document = ob.file.url

    data = {
        "id": article.id,
        "author": article.author.user.full_name,
        "section": article.section.name,
        "file": f"{document}",
        "title": article.title,
        "abstract": article.abstract,
        "keywords": article.keywords,
        "references": article.references,
        "article_status": article.article_status.name,
        "is_publish": article.is_publish,
        "created_at": article.created_at,
        "updated_at": article.updated_at,
    }
    return JsonResponse(data=data)


@login_required(login_url='login')
def delete_article(request, pk):
    resent_article = get_object_or_404(Submission, pk=pk)
    article = resent_article.article
    articles = Submission.objects.filter(article=article)
    article_count = articles.count()

    if request.method == "POST":
        notif = Notification.objects.get(my_resend__pk=resent_article.pk)
        if article_count == 1:
            article.delete()
        resent_article.delete()
        notif.delete()
        return redirect('sending_article_form')
    else:
        return render(request, 'article_app/crud/delete_myarticle.html',
                      {'article': article, 'resent_article': resent_article})


def get_article_authors(request, pk):
    authors = Author.objects.filter(article__id=pk)
    return JsonResponse({"authors": list(authors.values(
        'id', 'article'
    ))})


@login_required(login_url='login')
def add_author(request, pk):
    # user = request.user
    # article = Article.objects.get(pk=pk)
    # if request.user.id != article.author.id:
    #     return render(request, 'user_app/not_access.html')
    # last_resent = Submission.objects.filter(article=article).last()
    #
    # if request.method == 'POST':
    #     form = AddAuthorForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, "Mualliflar muvaffaqiyatli yaratildi!")
    #         data = {
    #             'message': 'form is saved'
    #         }
    #         return JsonResponse(data)
    # else:
        context = {
            # 'form': AddAuthorForm(),
            # 'user': user,
            # 'article': article,
        }
        return render(request, "article_app/crud/add_authors.html", context=context)


@login_required(login_url='login')
def edit_author(request, pk):
    # author = Author.objects.get(pk=pk)
    # article = author.article
    # if request.user.id != article.author.id:
    #     return render(request, 'user_app/not_access.html')
    # last_resent = Submission.objects.filter(article=article).last()
    # if request.method == "POST":
    #     form = AddAuthorForm(request.POST, instance=author)
    #     if form.is_valid():
    #         form.save()
    #         if article.state is None:
    #             return redirect('update_my_article', pk=article.pk)
    #         return redirect('update_resend_article', pk=last_resent.pk)
    #     else:
    #         return redirect('profile')
    # else:
    #     form = AddAuthorForm(instance=author)
        context = {
            # 'form': form,
            # 'author': author,
        }
        return render(request, "article_app/crud/edit_author.html", context=context)


@login_required(login_url='login')
def delete_author(request, pk):
    author = Author.objects.get(pk=pk)
    article = author.article
    if request.user.id != article.author.id:
        return render(request, 'user_app/not_access.html')
    if request.method == "POST":
        author.delete()
        return redirect('update_my_article', pk=author.article.id)
    else:
        return render(request, 'article_app/crud/delete_author.html', {'author': author})


@login_required(login_url='login')
# @allowed_users(menu_url='get_category')
def get_category(request):
    # categories = Category.objects.all()
    context = {
        # 'categories': categories,
    }
    return render(request, 'article_app/categories_page.html', context=context)


@login_required(login_url='login')
# @allowed_users(perm='add_category')
def create_section(request):
    # if request.method == "POST":
    #     form = CreateSectionForm(request.POST)
    #     if form.is_valid():
    #         category = form.save(commit=False)
    #         category.save()
    #         return redirect('get_category')
    # else:
        context = {
            # 'form': CreateCategoryForm(),
        }
        return render(request, "article_app/crud/add_category.html", context=context)


@login_required(login_url='login')
# @allowed_users(perm='change_category')
def edit_category(request, pk):
    # category = Category.objects.get(pk=pk)
    # if request.method == "POST":
    #     form = CreateCategoryForm(request.POST, instance=category)
    #     if form.is_valid():
    #         category = form.save(commit=False)
    #         category.save()
    #         return redirect('get_category')
    # else:
        context = {
            # 'form': CreateCategoryForm(instance=category),
            # 'category': category,
        }
        return render(request, "article_app/crud/edit_category.html", context=context)


@login_required(login_url='login')
# @allowed_users(perm='delete_category')
def delete_category(request, pk):
    category = Section.objects.get(pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect('get_category')
    else:
        return render(request, 'article_app/crud/delete_category.html', {'category': category})


@login_required(login_url='login')
# @allowed_users(perm='add_magazine')
def create_magazine(request):
    # user = request.user
    # if request.method == "POST":
    #     form = CreateJournalForm(request.POST)
    #     if form.is_valid():
    #         magazine = form.save(commit=False)
    #         magazine.save()
    #         return redirect('edit_magazine', pk=magazine.id)
    # else:
        context = {
            # 'form': CreateMagazineForm(),
            # 'user': user,
        }
        return render(request, "article_app/crud/create_magazine.html", context=context)


@login_required(login_url='login')
# @allowed_users(perm='change_magazine')
def edit_magazine(request, pk):
    # jurnal = Journal.objects.get(pk=pk)
    # if request.method == "POST":
    #     form = UpdateMagazineForm(request.POST, request.FILES, instance=jurnal)
    #     if form.is_valid():
    #         form.save()
    #
    #         return redirect('get_magazines')
    # else:
        context = {
            # 'form': UpdateMagazineForm(instance=jurnal),
            # 'jurnal': jurnal,
        }
        return render(request, "article_app/crud/edit_magazine.html", context=context)


@login_required(login_url='login')
# @allowed_users(menu_url='get_magazines')
def get_magazines(request):
    search = request.GET.get('search')
    magazines = Journal.objects.all()
    paginator = Paginator(magazines, 10)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    p_n = paginator.count
    page_count = page.paginator.page_range

    context = {
        'magazines': magazines,
        'page_count': page_count,
        'page': page,
        'p_n': p_n,
        'search': search,
    }
    return render(request, "article_app/magazines.html", context=context)


def about_journal(request):
    journal_ab = BlankPage.objects.get(id=1)
    return render(request, "article_app/about_journal.html", {
        "ob": journal_ab
    })


def talabnoma(request):
    t = BlankPage.objects.last()
    return render(request, "article_app/talabnoma.html", {
        "ob": t,
    })


def magazine_detail(request, pk):
    magazine = get_object_or_404(Journal, pk=pk)
    context = {
        'magazine': magazine
    }
    return render(request, "article_app/magazine_detail.html", context=context)


def all_magazine_son(request):
    magazines = Journal.objects.all()
    context = {
        'magazines': magazines
    }
    return render(request, "article_app/all_magazine_son.html", context=context)