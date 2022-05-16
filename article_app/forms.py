from django import forms
from django.forms import Select, DateInput, PasswordInput, TextInput, Textarea, FileInput
from .models import Article, Category, Authors


class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['author', 'title', 'category', 'keywords']

        widgets = {
            'category': Select(attrs={
                'class': 'form-control selectpicker',
                'data - size': "10",
                'data-live-search': "true",
                'data - style': "btn-white",
                'data - parsley - required': "true",
            }),
            'title': TextInput(attrs={
                'class': 'form-control',
                'data - size': "10",
                'data - parsley - required': "true",
            }),
            'keywords': TextInput(attrs={
                'class': 'form-control',
                'data - size': "10",
                'data - parsley - required': "true",
            }),
        }


class UpdateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'abstract', 'keywords', 'references', 'file', 'author']

        widgets = {
            'category': Select(attrs={
                'class': 'form-control selectpicker',
                'data-live-search': "true",
                'data - style': "btn-white",
                'data - parsley - required': "true",
            }),
            'title': TextInput(attrs={
                'class': 'form-control',
                'data - parsley - required': "true",
            }),
            'abstract': Textarea(attrs={
                'class': 'form-control',
                'data - parsley - required': "true",
                'rows': '5',
                'placeholder': 'Enter...'
            }),
            'keywords': TextInput(attrs={
                'class': 'form-control',
                'data - parsley - required': "true",
            }),
            'references': Textarea(attrs={
                'class': 'form-control',
                'data - parsley - required': "true",
                'rows': '5',
                'placeholder': 'Enter...'
            }),
            'file': FileInput(attrs={
                'type': 'file',
                'class': 'form-control',
                'data - parsley - required': "true",
                'accept': ".docx, .doc, .pdf"
            }),
        }


class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Authors
        fields = ['first_name', 'last_name', 'middle_name', 'email', 'article', 'work_place', 'author_order']

        widgets = {
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': "Enter...",
                'data - parsley - required': "true",
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': "Enter...",
                'data - parsley - required': "true",
            }),
            'middle_name': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': "Enter...",
                'data - parsley - required': "true",
            }),
            'email': TextInput(attrs={
                'class': 'form-control',
                'type': 'email',
                'data-parsley-type': "email",
                'placeholder': 'someone@example.com',
                'data - parsley - required': "true",
            }),
            'work_place': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': "Enter...",
                'data - parsley - required': "true",
            }),
            'author_order': TextInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'placeholder': "Enter...",
                'data - parsley - required': "true",
            }),
        }
