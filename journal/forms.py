from django.forms import TextInput, NumberInput, FileInput

from journal.models import Journal
from django import forms


class CreateJournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['name', 'year', 'number', 'file_pdf']

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control name',
                'name': 'name',
                'id': 'id_name'
            }),
            'year': NumberInput(attrs={
                'class': 'form-control year',
                'name': 'year',
                'id': 'id_year'
            }),
            'number': NumberInput(attrs={
                'class': 'form-control number',
                'name': 'number',
                'id': 'id_number'
            }),
            'file_pdf': FileInput(attrs={
                'class': 'form-control file_pdf',
                'name': 'file_pdf',
                'id': 'id_file_pdf',
                'type': 'file',
                'accept': ".pdf, .rtf",
            }),

        }

    class UpdateJournalForm(forms.ModelForm):
        pass
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

        # class Meta:
        #     model = Journal
        #     fields = ['file_pdf', 'journal_number', 'journal_year', 'status']
        #
        #     widgets = {
        #         'year_magazine': TextInput(attrs={
        #             'class': 'form-control',
        #             'type': 'text',
        #             'placeholder': "Enter...",
        #             'data - parsley - required': "true",
        #         }),
        #         'number_magazine': NumberInput(attrs={
        #             'class': 'form-control',
        #             'placeholder': "Enter...",
        #             'data - parsley - required': "true",
        #         }),
        #     }
