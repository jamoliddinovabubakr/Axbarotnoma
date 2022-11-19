from django import forms
from django.forms import TextInput, Textarea, FileInput, NumberInput, SelectMultiple, Select
from article_app.models import *


class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['section', 'title']

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
        fields = ['file', 'article']
        labels = {
            'file': 'Writer',
        }
        help_texts = {
            'file': 'Word yuklang!',
        }
        error_messages = {
            'file': {
                'max_length': "This writer's name is too long.",
            },
        }

        widgets = {
            'file': FileInput(attrs={
                'class': 'form-control',
                'type': 'file',
                'name': 'file',
                'id': 'id_file',
                'accept': ".docx, .doc",
                'data - parsley - required': "true",
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
                'name': 'section',
                'id': 'id_section',
            }),
            'title': Textarea(attrs={
                'class': 'form-control',
                'data - parsley - required': "true",
                'rows': '3',
                'name': 'title',
                'id': 'id_title',
            }),
            'abstract': Textarea(attrs={
                'class': 'form-control',
                'data - parsley - required': "true",
                'rows': '5',
                'placeholder': 'Enter...',
                'name': 'abstract',
                'id': 'id_abstract',
            }),
            'keywords': Textarea(attrs={
                'class': 'form-control',
                'data - parsley - required': "true",
                'name': 'keywords',
                'id': 'id_keywords',
            }),
            'references': Textarea(attrs={
                'class': 'form-control',
                'data - parsley - required': "true",
                'rows': '5',
                'placeholder': 'Enter...',
                'name': 'references',
                'id': 'id_references',

            }),
        }


class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = ExtraAuthor
        fields = ['article', 'fname', 'lname', 'mname', 'email', 'work']

        widgets = {
            'fname': TextInput(attrs={
                'id': 'author_fname',
                'class': 'form-control',
                'type': 'text',
                'placeholder': "Enter...",
                'data - parsley - required': "true",
            }),
            'lname': TextInput(attrs={
                'id': 'author_lname',
                'class': 'form-control',
                'type': 'text',
                'placeholder': "Enter...",
                'data - parsley - required': "true",
            }),
            'mname': TextInput(attrs={
                'id': 'author_mname',
                'class': 'form-control',
                'type': 'text',
                'placeholder': "Enter...",
                'data - parsley - required': "true",
            }),
            'email': TextInput(attrs={
                'id': 'author_email',
                'class': 'form-control',
                'type': 'email',
                'data-parsley-type': "email",
                'placeholder': 'someone@example.com',
                'data - parsley - required': "true",
            }),
            'work': TextInput(attrs={
                'id': 'author_work',
                'class': 'form-control',
                'type': 'text',
                'placeholder': "Enter...",
                'data - parsley - required': "true",
            }),

        }


class SendMessageForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['article', 'from_user', 'to_user', 'message']

        widgets = {
            'message': Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Write a message...",
                'data - parsley - required': "true",
                'name': 'message',
            }),
        }


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
