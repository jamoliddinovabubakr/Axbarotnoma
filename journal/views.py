import os

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from article_app.models import Article, ExtraAuthor
from journal.forms import CreateJournalForm, UpdateJournalForm
from journal.models import Journal, JournalArticle
import PyPDF2

from user_app.decorators import allowed_users
from django.utils.translation import gettext_lazy as _


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url='login')
@allowed_users(role=['editor'])
def journal_dashboard(request):
    journals = Journal.objects.all()
    articles = Article.objects.filter(article_status_id=2, is_publish=True, is_publish_journal=False)
    data = {
        "journals": journals,
        "articles": articles
    }
    return render(request, "journal/journal_dashboard.html", context=data)


@login_required(login_url='login')
@allowed_users(role=['editor'])
def split_journal_pages(request, pk):
    journal = get_object_or_404(Journal, pk=pk)
    if request.method == "POST" and is_ajax(request):
        j_articles = JournalArticle.objects.filter(journal=journal)
        article_ids = request.POST.getlist('article')
        start_pages = request.POST.getlist('start_page')
        end_pages = request.POST.getlist('end_page')

        if j_articles.count() != len(article_ids):
            data = {"result": False, "message": _("Wrong Article Count")}
            return JsonResponse(data)
        full_file = journal.file_pdf.path
        pdf = PyPDF2.PdfFileReader(full_file)
        pages_count = pdf.getNumPages()
        last_article_end_page = int(end_pages[-1])
        if pages_count < last_article_end_page:
            data = {"result": False, "message": _("Journal page count is less than last article end page number! ")}
            return JsonResponse(data)
        for i in range(len(article_ids)):
            cwd = os.getcwd()
            article = get_object_or_404(Article, pk=int(article_ids[i]))
            start_page = int(start_pages[i])
            end_page = int(end_pages[i])
            if start_page == 0 or end_page == 0:
                data = {
                    "result": False,
                    "message": _(f"{i + 1}-article not entered!"),
                }
                return JsonResponse(data)
            if start_page >= end_page:
                data = {
                    "result": False,
                    "message": _(f"{i + 1}-article page must be {start_page} < {end_page}!"),
                }
                return JsonResponse(data)

            newpdf = PyPDF2.PdfFileWriter()
            for j in range(start_page, end_page + 1, 1):
                newpdf.addPage(pdf.getPage(j - 1))

            out_path = f"{cwd}\\media\\files\\split_article\\{article.id}.pdf"

            with open(out_path, "wb") as out:
                newpdf.write(out)

            table = get_object_or_404(JournalArticle, journal=journal, article=article)
            table.start_page = start_page
            table.end_page = end_page
            table.article_pdf = f"files\\split_article\\{article.id}.pdf"
            table.save()
            article.filePDF = table.article_pdf
            article.save()

        journal.is_split = True
        journal.save()
        data = {
            "result": True,
            "message": _("Splited Successfully"),
        }
        return JsonResponse(data)
    objects = JournalArticle.objects.filter(journal=journal)
    context = {
        'journal': journal,
        'objects': objects,
    }
    return render(request, 'journal/split_pages.html', context=context)


@login_required(login_url='login')
@allowed_users(role=['editor'])
def create_journal(request):
    if request.method == 'POST' and is_ajax(request):
        get_file = request.FILES.get('file_pdf', None)
        form = CreateJournalForm(request.POST, request.FILES)
        articles = Article.objects.filter(article_status_id=2, is_publish=True, is_publish_journal=False)
        if form.is_valid():
            journal = form.save(commit=False)
            journal.save()
            for article in articles:
                try:
                    JournalArticle.objects.create(
                        journal=journal,
                        article=article,
                    )
                    article.is_publish_journal = True
                    article.save()
                except:
                    print("Error Create Journal")

            data = {
                "result": True,
                "message": _("Created Journal Successfully!"),
            }
            return JsonResponse(data)
        else:
            data = {
                "result": False,
                "message": _("Form didn't valid!"),
            }
            return JsonResponse(data)
    context = {
        'form': CreateJournalForm(),
    }
    return render(request, "journal/create_journal.html", context=context)


def journal_detail(request, pk):
    journal = get_object_or_404(Journal, pk=pk)
    list_articles = JournalArticle.objects.filter(journal=journal)
    context = {
        'journal': journal,
        'list_articles': list_articles,
    }
    return render(request, "journal/journal_detail.html", context=context)


def journals_list(request):
    journals = Journal.objects.filter(is_publish=True, status=True).order_by('-id')
    context = {
        'journals': journals,
    }
    return render(request, "journal/journals.html", context=context)


@login_required(login_url='login')
@allowed_users(role=['editor'])
def edit_journal(request, pk):
    journal = get_object_or_404(Journal, pk=pk)
    if request.method == "POST" and is_ajax(request):
        form = UpdateJournalForm(request.POST, request.FILES, instance=journal)
        if not form.has_changed():
            data = {"message": "The information has not changed", "result": False}
            return JsonResponse(data)
        if form.is_valid():
            form.save()
            data = {
                "result": True,
                "message": "Succes"
            }
            return JsonResponse(data)
        else:
            data = {
                "result": False,
                "message": "Error"
            }
            return JsonResponse(data)
    context = {
        'form': UpdateJournalForm(instance=journal),
        'journal': journal,
    }
    return render(request, "journal/edit_journal.html", context=context)


@login_required(login_url='login')
@allowed_users(role=['editor'])
def delete_journal(request, pk):
    journal = get_object_or_404(Journal, pk=pk)
    if request.method == "POST" and is_ajax(request):
        journal_articles = JournalArticle.objects.filter(journal=journal)
        for item in journal_articles:
            article = item.article
            article.is_publish_journal = False
            article.save()
        journal.delete()
        return JsonResponse({"message": "Deleted Success"})

    data = {"journal": journal}
    return render(request, "journal/delete_journal.html", context=data)


def journal_article_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    authors = ExtraAuthor.objects.filter(article=article)
    return render(request, 'journal/journal_article_view.html', context={'article': article, "authors": authors})
