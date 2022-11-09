from django import forms
from django.forms import TextInput, Textarea, FileInput, NumberInput, SelectMultiple, Select
from article_app.models import *


class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['section', 'title', 'author']

        widgets = {
            'section': Select(attrs={
                'class': 'form-control selectpicker',
                'data - size': "10",
                'data-live-search': "true",
                'data - style': "btn-white",
                'data - parsley - required': "true",
            }),
            'title': Textarea(attrs={
                'class': 'form-control',
                'data - size': "10",
                'data - parsley - required': "true",
            }),
        }


class CreateArticleFileForm(forms.ModelForm):
    class Meta:
        model = ArticleFile
        fields = ['article', 'file']

        widgets = {
            'file': FileInput(attrs={
                'id': 'id_file',
                'type': 'file',
                'class': 'form-control',
                'accept': ".docx, .doc"
            }),
        }


class UpdateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'section', 'abstract', 'keywords', 'references']

        widgets = {
            'section': Select(attrs={
                'class': 'form-control selectpicker',
                'data-live-search': "true",
                'data - style': "btn-white",
                'data - parsley - required': "true",
                'name': 'category',
            }),
            'title': Textarea(attrs={
                'class': 'form-control',
                'data - parsley - required': "true",
                'rows': '3',
                'id': 'title',
            }),
            'abstract': Textarea(attrs={
                'class': 'form-control',
                'data - parsley - required': "true",
                'rows': '5',
                'placeholder': 'Enter...',
                'id': 'abstract',
            }),
            'keywords': Textarea(attrs={
                'class': 'form-control',
                'data - parsley - required': "true",
                'id': 'keywords',
            }),
            'references': Textarea(attrs={
                'class': 'form-control',
                'data - parsley - required': "true",
                'rows': '5',
                'placeholder': 'Enter...',
                'id': 'references',

            }),
        }


# class AddAuthorForm(forms.ModelForm):
#     class Meta:
#         model = Authors
#         fields = ['article', 'first_name', 'last_name', 'middle_name', 'email', 'work_place', 'author_order']
#
#         widgets = {
#             'first_name': TextInput(attrs={
#                 'id': 'author_fname',
#                 'class': 'form-control',
#                 'type': 'text',
#                 'placeholder': "Enter...",
#                 'data - parsley - required': "true",
#             }),
#             'last_name': TextInput(attrs={
#                 'id': 'author_lname',
#                 'class': 'form-control',
#                 'type': 'text',
#                 'placeholder': "Enter...",
#                 'data - parsley - required': "true",
#             }),
#             'middle_name': TextInput(attrs={
#                 'id': 'author_mname',
#                 'class': 'form-control',
#                 'type': 'text',
#                 'placeholder': "Enter...",
#                 'data - parsley - required': "true",
#             }),
#             'email': TextInput(attrs={
#                 'id': 'author_email',
#                 'class': 'form-control',
#                 'type': 'email',
#                 'data-parsley-type': "email",
#                 'placeholder': 'someone@example.com',
#                 'data - parsley - required': "true",
#             }),
#             'work_place': TextInput(attrs={
#                 'id': 'author_work_place',
#                 'class': 'form-control',
#                 'type': 'text',
#                 'placeholder': "Enter...",
#                 'data - parsley - required': "true",
#             }),
#             'author_order': TextInput(attrs={
#                 'id': 'author_author_order',
#                 'class': 'form-control',
#                 'type': 'number',
#                 'placeholder': "Enter...",
#                 'data - parsley - required': "true",
#             }),
#         }


class CreateSectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name']

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': "Enter...",
                'data - parsley - required': "true",
            }),
        }


# class CreateMagazineForm(forms.ModelForm):
#     class Meta:
#         model = Journal
#         fields = ['number_magazine', 'year_magazine']
#
#         widgets = {
#             'year_magazine': TextInput(attrs={
#                 'class': 'form-control',
#                 'type': 'text',
#                 'placeholder': "Enter...",
#                 'data - parsley - required': "true",
#             }),
#             'number_magazine': NumberInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': "Enter...",
#                 'data - parsley - required': "true",
#             }),
#
#         }


# class UpdateMagazineForm(forms.ModelForm):
#     class Meta:
#         model = Journal
#         fields = ['number_magazine', 'year_magazine', 'article', 'status']
#
#         widgets = {
#             'year_magazine': TextInput(attrs={
#                 'class': 'form-control',
#                 'type': 'text',
#                 'placeholder': "Enter...",
#                 'data - parsley - required': "true",
#             }),
#             'number_magazine': NumberInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': "Enter...",
#                 'data - parsley - required': "true",
#             }),
#         }
