# from django.conf import settings
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.db.models import Q, Model
# from django.http import JsonResponse
# from django.shortcuts import render, redirect, get_object_or_404
# from django.utils import translation
#
# from user_app.decorators import allowed_users
# from article_app.models import Article, Section, Author, Journal, Post, BlankPage, Submission
# from .forms import CreateArticleForm, UpdateArticleForm, AddAuthorForm, CreateCategoryForm, CreateMagazineForm, \
#     UpdateMagazineForm, CreateMyResendArticleForm
# from django.core.paginator import Paginator
#
#
# def main_page(request):
#     user_language = 'uz'
#     post = Post.objects.last()
#     context = {
#         'post': post,
#     }
#     return render(request, "article_app/main.html", context=context)
#
#
# def post_detail(request, slug):
#     post = get_object_or_404(Post, url=slug)
#     context = {
#         'post': post,
#     }
#     return render(request, "article_app/post_detail.html", context=context)
#
#
# @login_required(login_url='login')
# def my_articles(request):
#     user = request.user
#     get_my_articles = Article.objects.filter(author=user).filter(
#             Q(state__id=2) | Q(state__id=3)
#         )
#     paginator = Paginator(get_my_articles, 10)
#     page_num = request.GET.get('page')
#     page = paginator.get_page(page_num)
#     p_n = paginator.count
#     page_count = page.paginator.page_range
#
#     context = {
#         'user': user,
#         'my_articles': get_my_articles,
#         'page_count': page_count,
#         'page': page,
#         'p_n': p_n,
#     }
#     return render(request, "article_app/my_articles.html", context=context)
#
#
# @login_required(login_url='login')
# def create_article(request):
#     user = request.user
#     if request.method == "POST":
#         form = CreateArticleForm(request.POST)
#         if form.is_valid():
#
#             title = form.cleaned_data['title'],
#             category = form.cleaned_data['category'],
#
#             article, created = Article.objects.get_or_create(title=list(title)[0], author=user)
#             for item in category[0]:
#                 article.category.add(int(item))
#
#             Authors.objects.create(
#                 article=article,
#                 last_name=user.last_name,
#                 first_name=user.first_name,
#                 middle_name=user.middle_name,
#                 email=user.email,
#                 work_place='No',
#                 author_order=1
#             )
#             return redirect('update_my_article', pk=article.id)
#         else:
#             context = {
#                 'form': CreateArticleForm(),
#                 'user': user,
#             }
#             return render(request, "article_app/crud/create_article.html", context=context)
#     else:
#         context = {
#             'form': CreateArticleForm(),
#             'user': user,
#         }
#         return render(request, "article_app/crud/create_article.html", context=context)
#
#
# @login_required(login_url='login')
# def update_my_article(request, pk):
#     article = Article.objects.get(pk=pk)
#     if request.user != article.author:
#         return render(request, 'user_app/not_access.html')
#     authors = Authors.objects.filter(article=article)
#
#     if request.method == "POST":
#         user = request.user
#         form = UpdateArticleForm(request.POST, request.FILES, instance=article)
#         if form.is_valid():
#             sending = State.objects.get(pk=4)
#             ob = form.save(commit=False)
#             ob.state = sending
#             ob.save()
#
#             MyResendArticle.objects.create(
#                 author=user,
#                 article=article,
#                 file_word=ob.file,
#                 message='Maqolangiz 14 ish kunida ko\'rib chiqladi.',
#                 state=sending,
#             )
#
#             return redirect('sending_article_form')
#         else:
#             context = {
#                 'form': UpdateArticleForm(instance=article),
#                 'article': article,
#                 'handle_error': 1,
#             }
#             return render(request, "article_app/crud/update_article.html", context=context)
#     else:
#         file_name = str(article.file.name).split('/')[-1]
#         context = {
#             'form': UpdateArticleForm(instance=article),
#             'article': article,
#             'handle_error': 0,
#             'file_name': str(file_name),
#         }
#         return render(request, "article_app/crud/update_article.html", context=context)
#
#
# def get_article_authors(request, pk):
#     authors = Authors.objects.filter(article__id=pk)
#     return JsonResponse({"authors": list(authors.values(
#         'id', 'article', 'first_name', 'last_name', 'middle_name', 'email', 'work_place', 'author_order'
#     ))})
#
#
# @login_required(login_url='login')
# def resend_article(request, pk):
#     last_resend = MyResendArticle.objects.get(pk=pk)
#     article = Article.objects.get(pk=last_resend.article.pk)
#     sending = State.objects.get(pk=4)
#
#     if request.method == "POST":
#         form = CreateMyResendArticleForm(request.POST, request.FILES)
#         if form.is_valid():
#             ob = form.save(commit=False)
#             ob.state = sending
#             ob.save()
#
#             article.state = sending
#             article.save()
#
#             last_resend.status = False
#             last_resend.save()
#
#             return redirect('sending_article_form')
#     else:
#         context = {
#             'form': CreateMyResendArticleForm(),
#             'article': article,
#         }
#         return render(request, "article_app/crud/resendform.html", context=context)
#
#
# @login_required(login_url='login')
# def update_resend_article(request, pk):
#     last_resend = MyResendArticle.objects.get(pk=pk)
#     article = last_resend.article
#     if request.user.id != article.author.id:
#         return render(request, 'user_app/not_access.html')
#     authors = Authors.objects.filter(article=article)
#     sending = State.objects.get(pk=4)
#
#     if request.method == "POST":
#         form = UpdateArticleForm(request.POST, request.FILES, instance=article)
#         if form.is_valid():
#             ob = form.save(commit=False)
#             ob.state = sending
#             ob.save()
#
#             return redirect('sending_article_form')
#     else:
#         file_name = str(article.file.name).split('/')[-1]
#         context = {
#             'form': UpdateArticleForm(instance=article),
#             'authors': authors,
#             'article': article,
#             'file_name': file_name,
#         }
#         return render(request, "article_app/crud/update_resendform.html", context=context)
#
#
# @login_required(login_url='login')
# def sending_article_form(request):
#     is_have = False
#     user = request.user
#
#     send_mylast_article = my_resends = None
#     last_article = Article.objects.filter(author=user).last()
#
#     if last_article:
#         get_mylast_articles = MyResendArticle.objects.filter(article=last_article).filter(status=True)
#         is_have = True
#         if get_mylast_articles.count() > 0:
#             send_mylast_article = get_mylast_articles.last()
#             my_resends = MyResendArticle.objects.filter(author=user).exclude(pk=send_mylast_article.pk).filter(
#                 status=False).filter(
#                 Q(state__name='Rad etildi') | Q(state__name='Tasdiqlandi') | Q(state__name='Qayta yuborish')
#             )
#         else:
#             my_resends = MyResendArticle.objects.filter(author=user).filter(status=False).filter(
#                 Q(state__name='Rad etildi') | Q(state__name='Tasdiqlandi') | Q(state__name='Qayta yuborish')
#             )
#
#     context = {
#         'is_have': is_have,
#         'last_article': last_article,
#         'my_resends': my_resends,
#         'send_mylast_article': send_mylast_article,
#     }
#     return render(request, "article_app/sending_article_form.html", context=context)
#
#
# @login_required(login_url='login')
# def add_author(request, pk):
#     user = request.user
#     article = Article.objects.get(pk=pk)
#     if request.user.id != article.author.id:
#         return render(request, 'user_app/not_access.html')
#     last_resent = MyResendArticle.objects.filter(article=article).last()
#
#     if request.method == 'POST':
#         form = AddAuthorForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Mualliflar muvaffaqiyatli yaratildi!")
#             data = {
#                 'message': 'form is saved'
#             }
#             return JsonResponse(data)
#     else:
#         context = {
#             'form': AddAuthorForm(),
#             'user': user,
#             'article': article,
#         }
#         return render(request, "article_app/crud/add_authors.html", context=context)
#
#
# @login_required(login_url='login')
# def edit_author(request, pk):
#     author = Authors.objects.get(pk=pk)
#     article = author.article
#     if request.user.id != article.author.id:
#         return render(request, 'user_app/not_access.html')
#     last_resent = MyResendArticle.objects.filter(article=article).last()
#     if request.method == "POST":
#         form = AddAuthorForm(request.POST, instance=author)
#         if form.is_valid():
#             form.save()
#             if article.state is None:
#                 return redirect('update_my_article', pk=article.pk)
#             return redirect('update_resend_article', pk=last_resent.pk)
#         else:
#             return redirect('profile')
#     else:
#         form = AddAuthorForm(instance=author)
#         context = {
#             'form': form,
#             'author': author,
#         }
#         return render(request, "article_app/crud/edit_author.html", context=context)
#
#
# @login_required(login_url='login')
# def delete_author(request, pk):
#     author = Authors.objects.get(pk=pk)
#     article = author.article
#     if request.user.id != article.author.id:
#         return render(request, 'user_app/not_access.html')
#     if request.method == "POST":
#         author.delete()
#         return redirect('update_my_article', pk=author.article.id)
#     else:
#         return render(request, 'article_app/crud/delete_author.html', {'author': author})
#
#
# @login_required(login_url='login')
# def delete_myarticle(request, pk):
#     resent_article = get_object_or_404(MyResendArticle, pk=pk)
#     article = resent_article.article
#     articles = MyResendArticle.objects.filter(article=article)
#     article_count = articles.count()
#
#     if request.method == "POST":
#         notif = Notification.objects.get(my_resend__pk=resent_article.pk)
#         if article_count == 1:
#             article.delete()
#         resent_article.delete()
#         notif.delete()
#         return redirect('sending_article_form')
#     else:
#         return render(request, 'article_app/crud/delete_myarticle.html',
#                       {'article': article, 'resent_article': resent_article})
#
#
# @login_required(login_url='login')
# @allowed_users(menu_url='get_category')
# def get_category(request):
#     categories = Category.objects.all()
#     context = {
#         'categories': categories,
#     }
#     return render(request, 'article_app/categories_page.html', context=context)
#
#
# @login_required(login_url='login')
# @allowed_users(perm='add_category')
# def create_category(request):
#     if request.method == "POST":
#         form = CreateCategoryForm(request.POST)
#         if form.is_valid():
#             category = form.save(commit=False)
#             category.save()
#             return redirect('get_category')
#     else:
#         context = {
#             'form': CreateCategoryForm(),
#         }
#         return render(request, "article_app/crud/add_category.html", context=context)
#
#
# @login_required(login_url='login')
# @allowed_users(perm='change_category')
# def edit_category(request, pk):
#     category = Category.objects.get(pk=pk)
#     if request.method == "POST":
#         form = CreateCategoryForm(request.POST, instance=category)
#         if form.is_valid():
#             category = form.save(commit=False)
#             category.save()
#             return redirect('get_category')
#     else:
#         context = {
#             'form': CreateCategoryForm(instance=category),
#             'category': category,
#         }
#         return render(request, "article_app/crud/edit_category.html", context=context)
#
#
# @login_required(login_url='login')
# @allowed_users(perm='delete_category')
# def delete_category(request, pk):
#     category = Category.objects.get(pk=pk)
#     if request.method == "POST":
#         category.delete()
#         return redirect('get_category')
#     else:
#         return render(request, 'article_app/crud/delete_category.html', {'category': category})
#
#
# @login_required(login_url='login')
# @allowed_users(perm='add_magazine')
# def create_magazine(request):
#     user = request.user
#     if request.method == "POST":
#         form = CreateMagazineForm(request.POST)
#         if form.is_valid():
#             magazine = form.save(commit=False)
#             magazine.save()
#             return redirect('edit_magazine', pk=magazine.id)
#     else:
#         context = {
#             'form': CreateMagazineForm(),
#             'user': user,
#         }
#         return render(request, "article_app/crud/create_magazine.html", context=context)
#
#
# @login_required(login_url='login')
# @allowed_users(perm='change_magazine')
# def edit_magazine(request, pk):
#     jurnal = Journal.objects.get(pk=pk)
#     if request.method == "POST":
#         form = UpdateMagazineForm(request.POST, request.FILES, instance=jurnal)
#         if form.is_valid():
#             form.save()
#
#             return redirect('get_magazines')
#     else:
#         context = {
#             'form': UpdateMagazineForm(instance=jurnal),
#             'jurnal': jurnal,
#         }
#         return render(request, "article_app/crud/edit_magazine.html", context=context)
#
#
# @login_required(login_url='login')
# @allowed_users(menu_url='get_magazines')
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
#
#
# def about_journal(request):
#     journal_ab = BlankPage.objects.get(id=1)
#     return render(request, "article_app/about_journal.html", {
#         "ob": journal_ab
#     })
#
#
# def talabnoma(request):
#     t = BlankPage.objects.last()
#     return render(request, "article_app/talabnoma.html", {
#         "ob": t,
#     })
#
#
# def magazine_detail(request, pk):
#     magazine = get_object_or_404(Journal, pk=pk)
#     context = {
#         'magazine': magazine
#     }
#     return render(request, "article_app/magazine_detail.html", context=context)
#
#
# def all_magazine_son(request):
#     magazines = Journal.objects.all()
#     context = {
#         'magazines': magazines
#     }
#     return render(request, "article_app/all_magazine_son.html", context=context)