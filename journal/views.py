from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from article_app.models import Article
from journal.forms import CreateJournalForm, UpdateJournalForm
from journal.models import SplitPdf, Journal
import PyPDF2

from post.models import BlankPage


@login_required(login_url='login')
def split_pdf(request):
    journal = Journal.objects.last()
    if request.method == "POST":
        for i in journal.article.all():
            start_page = request.POST[f'start_page{i.id}']
            finish_page = request.POST[f'end_page{i.id}']
            if start_page is not None:
                filename = journal.file_pdf.path
                pdf = PyPDF2.PdfFileReader(
                    open(f"{filename}", "rb"))
                if start_page == '' or finish_page == '' \
                        or int(start_page) >= int(finish_page):
                    context = {
                        'journal': journal,
                        'article_number': journal.article.all(),
                        'error': "Forma to'liq kiritilmagan"
                    }
                    return render(request, 'journal/splitpdf.html', context=context)
                page_start_int = int(start_page)
                page_end_int = int(finish_page)
                newpdf = PyPDF2.PdfFileWriter(f"{filename}")
                for k in range(page_start_int, page_end_int):
                    newpdf.addPage(pdf.getPage(k-1))
                newpdf.addPage(pdf.getPage(page_end_int-1))
                with open(
                        f"media/split_files//{Article.objects.get(pk=i.id).author.id}_{Article.objects.get(pk=i.id).id}.pdf",
                        "wb") as f:
                    newpdf.write(f)

                SplitPdf.objects.create(
                    article=Article.objects.get(pk=i.id),
                    start_page=request.POST[f'start_page{i.id}'],
                    finish_page=request.POST[f'end_page{i.id}'],
                    file=f"/split_files/{Article.objects.get(pk=i.id).author.id}_{Article.objects.get(pk=i.id).id}.pdf"
                )
        return redirect('get_journals')
    context = {
        'journal': journal,
        'article_number': journal.article.all()
    }
    return render(request, 'journal/splitpdf.html', context=context)


@login_required(login_url='login')
# @allowed_users(perm='add_magazine')
def create_journal(request):
    if request.method == 'POST':
        form = CreateJournalForm(request.POST, request.FILES)
        articles = Article.objects.filter(article_status_id=2, is_publish_journal=False)
        if form.is_valid():
            journal = form.save(commit=False)
            journal.save()
            for i in articles:
                journal.article.add(Article.objects.get(pk=i.id))
                article = Article.objects.get(pk=i.id)
                article.is_publish_journal = True
                article.save()
            return redirect('split_pdf')
    context = {
        'form': CreateJournalForm(),
        'articles': Article.objects.filter(article_status_id=2, is_publish_journal=False),
        'len_articles': len(Article.objects.filter(article_status_id=2, is_publish_journal=False))
    }
    return render(request, "journal/create_journal.html", context=context)


def journal_detail(request, pk):
    magazine = get_object_or_404(Journal, pk=pk)
    context = {
        'magazine': magazine
    }
    return render(request, "journal/journal_detail.html", context=context)


def journal_article(request, pk_article):
    article = Article.objects.get(pk=pk_article)
    article_journal = SplitPdf.objects.get(article_id=pk_article)
    return render(request, 'journal/journal_article.html',
                  context={'article_journal': article_journal, 'article': article})
    # return HttpResponse(f'{pk_article}, \n {a.file.path}')


@login_required(login_url='login')
def get_journal(request):
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
    return render(request, "journal/journals.html", context=context)


def about_journal(request):
    journal_ab = BlankPage.objects.get(id=1)
    return render(request, "journal/about_journal.html", {
        "ob": journal_ab
    })


def journals_number(request):
    journals = Journal.objects.filter(status=True)
    context = {
        'journals': journals
    }
    return render(request, "journal/journals_number.html", context=context)


@login_required(login_url='login')
def edit_journal(request, pk):
    journal = Journal.objects.get(pk=pk)
    if request.method == "POST":
        form = UpdateJournalForm(request.POST, request.FILES, instance=journal)
        if form.is_valid():
            form.save()
            return redirect('get_journals')
    context = {
        'form': UpdateJournalForm(instance=journal),
        'journal': journal,
    }
    return render(request, "journal/edit_journal.html", context=context)


@login_required(login_url='login')
def delete_journal(request, delete_journal_id):
    journal = Journal.objects.get(id=delete_journal_id)
    for i in journal.article.all():
        article = Article.objects.get(pk=i.id)
        article.is_publish_journal = False
        article.save()
        split_pdfs = SplitPdf.objects.get(article=article)
        split_pdfs.delete()
    journal.delete()
    return HttpResponseRedirect(reverse('get_journals'))


@login_required(login_url='login')
def journal_view(request, journal_view_id):
    journal = Journal.objects.get(id=journal_view_id)
    return render(request, 'journal/journal_view.html', context={'journal': journal})
