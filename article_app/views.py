from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Q, Model
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import translation
from django.views.decorators.csrf import requires_csrf_token

from user_app.decorators import allowed_users
from article_app.models import *
from article_app.models import ExtraAuthor
from article_app.forms import CreateArticleForm, UpdateArticleForm, CreateArticleFileForm, AddAuthorForm, \
    SendMessageForm
from django.core.paginator import Paginator
from user_app.models import User, Editor


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


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
def create_article(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == "POST" and is_ajax(request):
        country = request.POST.get('country', None)
        article_type = request.POST.get('article_type', None)
        article_lang = request.POST.get('article_lang', None)
        section = request.POST.get('section', None)
        title = request.POST.get('title', None)

        form = CreateArticleForm(request.POST)
        if form.is_valid() and country and article_type and article_lang and section and title:
            article = form.save(commit=False)
            article.author = user
            article.article_status_id = 6
            article.save()

            ExtraAuthor.objects.create(
                article=article,
                lname=article.author.last_name,
                fname=article.author.first_name,
                mname=article.author.middle_name,
                email=article.author.email,
                work=article.author.work,
            )
            data = {
                "result": True,
                "message": "Ok!",
                "redirect": f"/article/edit/{article.id}/",
            }
            return JsonResponse(data=data)
        else:
            data = {
                "result": False,
                "message": "Form is invalid!",
            }
            return JsonResponse(data=data)
    else:
        context = {
            'form': CreateArticleForm(),
        }
        return render(request, "article_app/crud/create_article.html", context=context)


@login_required(login_url='login')
def update_article(request, pk):
    user = request.user
    editor = Editor.objects.all().last()
    articles = Article.objects.filter(pk=pk)
    if articles.count() == 0:
        return render(request, 'user_app/not_access.html')
    article = articles.first()
    if user != article.author:
        return render(request, 'user_app/not_access.html')

    if request.method == "POST":
        form = UpdateArticleForm(request.POST, instance=article)
        if form.is_valid():
            files = ArticleFile.objects.filter(
                article=article).filter(file_status=1)
            title = str(request.POST.get('title')).replace(
                '<p>', '').replace('</p>', '')
            abstrk = str(request.POST.get('abstract')).replace(
                '<p>', '').replace('</p>', '')
            keywords = str(request.POST.get('keywords')).replace(
                '<p>', '').replace('</p>', '')
            references = str(request.POST.get('references')).replace(
                '<p>', '').replace('</p>', '')

            if len(abstrk) == 0 or len(keywords) == 0 or len(references) == 0 or len(title) == 0 or files.count() == 0:
                context = {
                    'form': UpdateArticleForm(instance=article),
                    'article': article,
                    'handle_error': 1,
                }
                return render(request, "article_app/crud/update_article.html", context=context)

            form.save()

            if article.article_status.id == 6:
                article.article_status = ArticleStatus.objects.get(pk=1)
                article.save()
                Notification.objects.create(
                    article=article,
                    from_user=article.author,
                    to_user=editor.user,
                    message=f"({editor.user.email})Assalomu aleykum. Yangi maqolamni yubordim!",
                    notification_status=NotificationStatus.objects.get(id=1),
                    is_update_article=True,
                )

            if article.article_status.id == 7 or article.article_status.id == 8:
                article.article_status = ArticleStatus.objects.get(pk=1)
                article.save()
                Notification.objects.create(
                    article=article,
                    from_user=article.author,
                    to_user=editor.user,
                    message=f"({editor.user.email})Assalomu aleykum. Maqolamni to'g'irlab qayta yubordim!",
                    notification_status=NotificationStatus.objects.get(id=1),
                    is_update_article=True,
                )

            return redirect('dashboard')

        else:
            data = {
                'result': 0,
                'message': "Formani to'liq to'ldiring...!",
            }
            return JsonResponse(data=data)
    else:
        context = {
            'form': UpdateArticleForm(instance=article),
            'article': article,
        }
        return render(request, "article_app/crud/update_article.html", context=context)


def create_article_file(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        form = CreateArticleFileForm(request.POST, request.FILES)
        get_file = request.FILES.get('file', None)
        if form.is_valid() and get_file is not None:
            files = ArticleFile.objects.filter(article_id=pk)
            if files.count() > 0:
                for f in files:
                    f.file_status = 0
                    f.save()

            new_file = form.save(commit=False)
            new_file.save()
            article.file = new_file
            article.save()
            data = {
                'result': True,
                'file_name': new_file.file_name(),
                'message': 'Success!'
            }
            return JsonResponse(data=data)
        else:
            data = {
                'result': False,
                'message': "Invalid!"
            }
            return JsonResponse(data=data)
    else:
        context = {
            'form': CreateArticleFileForm(),
            'article': article,
        }
        return render(request, "article_app/crud/create_file.html", context=context)


@login_required(login_url='login')
def article_view(request, pk):
    if is_ajax(request=request):
        article = get_object_or_404(Article, pk=pk)
        document = None
        author = article.author
        if article.file is not None:
            ob = ArticleFile.objects.filter(
                article_id=article.id).filter(file_status=1).first()
            document = ob.file.url

        data = {
            "id": article.id,
            "author": author.full_name,
            "section": article.section.name,
            "file": f"{document}",
            "title": article.title,
            "abstract": article.abstract,
            "keywords": article.keywords,
            "references": article.references,
            "article_status": article.article_status.name,
            "article_status_id": article.article_status.id,
            "is_publish": article.is_publish,
            "created_at": article.created_at.strftime("%d/%m/%Y, %H:%M:%S"),
            "updated_at": article.updated_at,
        }
        return JsonResponse(data=data)
    else:
        return redirect("dashboard")


@login_required(login_url='login')
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        article.delete()
        data = {
            "result": True,
            "message": "Your article was successfully deleted!",
        }
        return JsonResponse(data=data)
    else:
        return render(request, 'article_app/crud/delete_article.html', {'article': article})


def get_article_authors(request, pk):
    authors = ExtraAuthor.objects.filter(article_id=pk).order_by('id')
    return JsonResponse({"authors": list(authors.values(
        'id', 'lname', 'fname', 'mname', 'email', 'work', 'scientific_degree__name'
    ))})


@login_required(login_url='login')
def add_author(request, pk):
    user = request.user
    article = Article.objects.get(pk=pk)
    if user.id != article.author.id:
        return render(request, 'user_app/not_access.html')

    if request.method == 'POST':
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            if ExtraAuthor.objects.filter(article_id=pk).count() > 4:
                data = {'result': "limit_author",
                        'message': 'Mualliflarni qoshish limiti 4 ta!'}
                return JsonResponse(data)
            form.save()
            data = {
                'result': True,
                'message': 'Mualliflar muvaffaqiyatli yaratildi!'
            }
            return JsonResponse(data)
        else:
            data = {'result': False,
                    'message': 'Mualliflar muvaffaqiyatli yaratildi!'}
            return JsonResponse(data)
    context = {
        'form': AddAuthorForm(),
        'user': user,
        'article': article,
    }
    return render(request, "article_app/crud/add_authors.html", context=context)


@login_required(login_url='login')
def edit_author(request, pk):
    author = ExtraAuthor.objects.get(pk=pk)
    article = author.article

    if request.user.id != article.author.id:
        return render(request, 'user_app/not_access.html')

    if request.method == "POST":
        form = AddAuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            data = {
                'result': True,
                'message': 'Editing author successfully!'
            }
            return JsonResponse(data)
        else:
            return JsonResponse("Form is invalid")

    form = AddAuthorForm(instance=author)
    context = {
        'form': form,
        'author': author,
    }
    return render(request, "article_app/crud/edit_author.html", context=context)


@login_required(login_url='login')
def delete_author(request, pk):
    author = ExtraAuthor.objects.get(pk=pk)
    article = author.article
    if request.user.id != article.author.id:
        return render(request, 'user_app/not_access.html')
    if request.method == "POST":
        author.delete()
        data = {
            "result": True,
            "message": "Deleted Author Successfully"
        }
        return JsonResponse(data)
    else:
        return render(request, 'article_app/crud/delete_author.html', {'author': author})


@login_required(login_url='login')
def send_message(request, pk, user_id):
    article = Article.objects.get(pk=pk)
    current_user = User.objects.get(id=request.user.id)
    author = article.author
    author_id = author.id
    roles = current_user.get_roles

    if request.method == 'GET' and is_ajax(request):
        form = SendMessageForm()
        context = {
            'form': form,
            'article': article,
            'from_user': current_user,
            'user_id': user_id,
            'roles': roles,
        }
        return render(request, 'article_app/message/send_message.html', context=context)

    elif request.method == "POST" and is_ajax(request):
        form = SendMessageForm(request.POST)
        if form.is_valid():
            notif = form.save(commit=False)
            notif.notification_status = NotificationStatus.objects.get(pk=1)
            notif.save()
            data = {
                'result': True,
                'roles': roles,
                'message': 'Send Message Successfully!'
            }
            return JsonResponse(data)
        else:
            return JsonResponse("Form is invalid")
    else:
        return HttpResponse("Note Found Page.")


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


# @login_required(login_url='login')
# # @allowed_users(menu_url='get_magazines')
# def get_magazines(request):
#     search = request.GET.get('search')
#     magazines = Journal.objects.all()
#     paginator = Paginator(magazines, 10)
#     page_num = request.GET.get('page')
#     page = paginator.get_page(page_num)
#     p_n = paginator.count
#     page_count = page.paginator.page_range
#
#     context = {
#         'magazines': magazines,
#         'page_count': page_count,
#         'page': page,
#         'p_n': p_n,
#         'search': search,
#     }
#     return render(request, "article_app/magazines.html", context=context)


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


# def magazine_detail(request, pk):
#     magazine = get_object_or_404(Journal, pk=pk)
#     context = {
#         'magazine': magazine
#     }
#     return render(request, "article_app/magazine_detail.html", context=context)


# def all_magazine_son(request):
#     magazines = Journal.objects.all()
#     context = {
#         'magazines': magazines
#     }
#     return render(request, "article_app/all_magazine_son.html", context=context)
