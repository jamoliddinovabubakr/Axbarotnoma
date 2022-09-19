from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from user_app.decorators import allowed_users
from .models import Article, Category, Authors, Magazine, Post, BlankPage, MyResendArticle
from user_app.models import User, State
from .forms import CreateArticleForm, UpdateArticleForm, AddAuthorForm, CreateCategoryForm, CreateMagazineForm, UpdateMagazineForm
from django.core.paginator import Paginator
from article_app.merge_multiple_word_files import combine_all_docx


def main_page(request):
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
    search = request.GET.get('search')
    n_show = request.GET.get('n_show')

    if search is None:
        get_my_articles = Article.objects.filter(author=user).filter(
            Q(state__id=2) | Q(state__id=3)
        )
        search = ''
    else:
        get_my_articles = Article.objects.filter(author=user).filter(
            Q(title__icontains=search) | Q(category__name__icontains=search)
        )

    if n_show is None:
        n_show = 10

    if n_show == '0':
        n_show = get_my_articles.count()

    paginator = Paginator(get_my_articles, int(n_show))
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    p_n = paginator.count
    page_count = page.paginator.page_range

    if n_show == p_n:
        n_show = 0

    context = {
        'user': user,
        'my_articles': get_my_articles,
        'page_count': page_count,
        'page': page,
        'p_n': p_n,
        'search': search,
        'n_show': int(n_show),
    }
    return render(request, "article_app/my_articles.html", context=context)


@login_required(login_url='login')
def create_article(request):
    user = request.user
    if request.method == "POST":
        form = CreateArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            articleId = article.id

            Authors.objects.create(
                article=article,
                last_name=user.last_name,
                first_name=user.first_name,
                middle_name=user.middle_name,
                email=user.email,
                work_place='-',
                author_order=1
            )
            return redirect('update_my_article', pk=articleId)
    else:
        context = {
            'form': CreateArticleForm(),
            'user': user,
        }
        return render(request, "article_app/crud/create_article.html", context=context)


@login_required(login_url='login')
def update_my_article(request, pk):
    article = Article.objects.get(pk=pk)
    authors = Authors.objects.filter(article=article)

    if request.method == "POST":
        form = UpdateArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            ob = form.save(commit=False)
            ob.state = State.objects.get(pk=4)
            ob.save()
            return redirect('my_articles')
    else:
        file_name = str(article.file.name).split('/')[-1]
        context = {
            'form': UpdateArticleForm(instance=article),
            'authors': authors,
            'article': article,
            'file_name': file_name,
        }
        return render(request, "article_app/crud/update_article.html", context=context)



@login_required(login_url='login')
def sending_article_form(request):
    is_have = False
    user = request.user
    last_article = Article.objects.filter(author=user).last()
    print(last_article)
    
    get_mylast_article = MyResendArticle.objects.filter(article=last_article)
    if get_mylast_article:
        is_have=True
    print(get_mylast_article)
    context = {
        'get_mylast_article': get_mylast_article,
        'is_have': is_have,
        'last_article': last_article,
    }
    return render(request, "article_app/sending_article_form.html", context=context)


@login_required(login_url='login')
def add_author(request, pk):
    user = request.user
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('update_my_article', pk=pk)
    else:
        context = {
            'form': AddAuthorForm(),
            'user': user,
            'article': article,
        }
        return render(request, "article_app/crud/add_authors.html", context=context)



@login_required(login_url='login')
def edit_author(request, pk):
    author = Authors.objects.get(pk=pk)
    article = Article.objects.filter(extra_autjhor__id=pk)
    if request.method == "POST":
        form = AddAuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('update_my_article', pk=article.id)
        else:
            return redirect('profile')
    else:
        form = AddAuthorForm(instance=author)
        context = {
            'form': form,
            'author': author,
        }
        return render(request, "article_app/crud/edit_author.html", context=context)


@login_required(login_url='login')
def delete_author(request, pk):
    author = Authors.objects.get(pk=pk)
    if request.method == "POST":
        author.delete()
        return redirect('update_my_article', pk=author.article.id)
    else:
        return render(request, 'article_app/crud/delete_author.html', {'author': author})


@login_required(login_url='login')
def delete_myarticle(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        article.delete()
        return redirect('my_articles')
    else:
        return render(request, 'article_app/crud/delete_myarticle.html', {'article': article})


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN', 'BOSH MUHARRIR'])
def get_category(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'article_app/categories_page.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN', 'BOSH MUHARRIR'])
def create_category(request):
    if request.method == "POST":
        form = CreateCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('get_category')
    else:
        context = {
            'form': CreateCategoryForm(),
        }
        return render(request, "article_app/crud/add_category.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN', 'BOSH MUHARRIR'])
def edit_category(request, pk):
    category = Category.objects.get(pk=pk)
    if request.method == "POST":
        form = CreateCategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('get_category')
    else:
        context = {
            'form': CreateCategoryForm(instance=category),
            'category': category,
        }
        return render(request, "article_app/crud/edit_category.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN', 'BOSH MUHARRIR'])
def delete_category(request, pk):
    category = Category.objects.get(pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect('get_category')
    else:
        return render(request, 'article_app/crud/delete_category.html', {'category': category})


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN', 'BOSH MUHARRIR'])
def create_magazine(request):
    user = request.user
    if request.method == "POST":
        form = CreateMagazineForm(request.POST)
        if form.is_valid():
            magazine = form.save(commit=False)
            magazine.save()
            jurnalId = magazine.id
            return redirect('edit_magazine', pk=jurnalId)
    else:
        context = {
            'form': CreateMagazineForm(),
            'user': user,
        }
        return render(request, "article_app/crud/create_magazine.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN', 'BOSH MUHARRIR'])
def edit_magazine(request, pk):
    jurnal = Magazine.objects.get(pk=pk)

    if request.method == "POST":
        form = UpdateMagazineForm(request.POST, request.FILES, instance=jurnal)
        if form.is_valid():
            choosen_article = form.cleaned_data['article']
            form.save()

            return redirect('get_magazines')
    else:
        context = {
            'form': UpdateMagazineForm(instance=jurnal),
            'jurnal': jurnal,
        }
        return render(request, "article_app/crud/edit_magazine.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN', 'BOSH MUHARRIR'])
def get_magazines(request):
    search = request.GET.get('search')
    n_show = request.GET.get('n_show')

    if search is None:
        magazines = Magazine.objects.all()
        search = ''
    else:
        magazines = Magazine.objects.filter(
            Q(number_magazine__icontains=search) | Q(category__name__icontains=search)
        )

    if n_show is None:
        n_show = 10

    if n_show == '0':
        n_show = magazines.count()

    paginator = Paginator(magazines, int(n_show))
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    p_n = paginator.count
    page_count = page.paginator.page_range

    if n_show == p_n:
        n_show = 0

    context = {
        'magazines': magazines,
        'page_count': page_count,
        'page': page,
        'p_n': p_n,
        'search': search,
        'n_show': int(n_show),
    }
    return render(request, "article_app/magazines.html", context=context)


def about_journal(request):
    journal_ab = BlankPage.objects.get(id=1)
    return render(request, "article_app/about_journal.html", {
        "ob": journal_ab
    })


def talabnoma(request):
    talabnoma = BlankPage.objects.get(id=2)
    return render(request, "article_app/talabnoma.html", {
        "ob": talabnoma
    })


def magazine_detail(request, pk):
    magazine = get_object_or_404(Magazine, pk=pk)
    context = {
        'magazine': magazine
    }
    return render(request, "article_app/magazine_detail.html", context=context)


def all_magazine_son(request):
    magazines = Magazine.objects.all()
    context = {
        'magazines': magazines
    }
    return render(request, "article_app/all_magazine_son.html", context=context)