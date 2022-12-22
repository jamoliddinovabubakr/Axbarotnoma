from django.forms import TextInput, NumberInput, FileInput, CheckboxInput

from journal.models import Journal, JournalArticle
from django import forms


class CreateJournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['name', 'year', 'number', 'file_pdf', 'image']

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
            'image': FileInput(attrs={
                'class': 'form-control image',
                'name': 'image',
                'id': 'id_image',
                'type': 'file',
                'accept': ".jpg, .jpeg, .png",
            }),
        }


class UpdateJournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['name', 'year', 'number', 'file_pdf', 'is_publish', 'status', 'image']

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'data - parsley - required': "true",
            }),
            'year': NumberInput(attrs={
                'class': 'form-control',
                'data - parsley - required': "true",
            }),
            'number': NumberInput(attrs={
                'class': 'form-control',
                'data - parsley - required': "true",
            }),
            'file_pdf': FileInput(attrs={
                'class': 'form-control file_pdf',
                'name': 'file_pdf',
                'id': 'id_file_pdf',
                'type': 'file',
                'accept': ".pdf, .rtf",
            }),
            'image': FileInput(attrs={
                'class': 'form-control image',
                'name': 'image',
                'id': 'id_image',
                'type': 'file',
                'accept': ".jpg, .jpeg, .png",
            }),
            'is_publish': CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'status': CheckboxInput(attrs={
                'class': 'form-control',
            }),
        }
