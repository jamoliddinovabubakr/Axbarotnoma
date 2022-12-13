from django.db.models import Q
from django.forms import TextInput, NumberInput

from article_app.models import Article, Section
from journal.models import Journal
from django import forms


class CreateJournalForm(forms.ModelForm):
    # choices = [['', '']]
    # a = Article.objects.all()
    # query = Article.objects.filter(article_status_id=2, is_publish_journal=False).values()
    # print(query)
    # if query:
    #     choices = [[x['id'], x['title']] for x in query]
    #
    # article = forms.MultipleChoiceField(choices=choices, required=True, widget=forms.SelectMultiple(attrs={
    #     'class': 'multiple-select2 form-control',
    #     'multiple': 'multiple',
    #     'data - size': "10",
    #     'data-live-search': "true",
    #     'data - style': "btn-white",
    #     'data - parsley - required': "true",
    # }))

    class Meta:
        model = Journal
        fields = '__all__'


class UpdateJournalForm(forms.ModelForm):
    # choices = [['', '']]
    # a = Article.objects.all()
    # query = Article.objects.filter(article_status_id=2, is_publish_journal=True).values()
    # if query:
    #     choices = [[x['id'], x['title']] for x in query]
    #
    # article = forms.MultipleChoiceField(choices=choices, required=True, widget=forms.SelectMultiple(attrs={
    #     'class': 'multiple-select2 form-control',
    #     'multiple': 'multiple',
    #     'data - size': "10",
    #     'data-live-search': "true",
    #     'data - style': "btn-white",
    #     'data - parsley - required': "true",
    # }))

    class Meta:
        model = Journal
        fields = ['file_pdf', 'journal_number', 'journal_year', 'status']

        widgets = {
            'year_magazine': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': "Enter...",
                'data - parsley - required': "true",
            }),
            'number_magazine': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter...",
                'data - parsley - required': "true",
            }),
        }
