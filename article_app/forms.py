from django import forms
from django.forms import Select, DateInput, PasswordInput, TextInput, Textarea
from .models import Article, Category


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
                'rows':'5',
                'placeholder': 'Enter...'
            }),
        }
