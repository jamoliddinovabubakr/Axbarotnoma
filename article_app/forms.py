from django import forms
from django.forms import Select, DateInput, PasswordInput, TextInput, SelectMultiple
from .models import Article, Category


class AddArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'abstract', 'keywords', 'references', 'file', 'author']

        widgets = {
            'category': Select(attrs={
                'class': 'form-control selectpicker',
                'data - size': "10",
                'data-live-search': "true",
                'data - style': "btn-white",
                'data - parsley - group': "step-3",
            }),
            # 'author': SelectMultiple(attrs={
            #     'class': 'form-control',
            #     'data - size': "10",
            #     'data-live-search': "true",
            #     'data - style': "btn-white",
            #     'data - parsley - group': "step-3",
            # }),
            'title': TextInput(attrs={
                'class': 'form-control',
                'data - size': "10",
                'data - parsley - group': "step-3",
            }),
            'abstract': TextInput(attrs={
                'class': 'form-control',
                'data - size': "10",
                'data - parsley - group': "step-3",
            }),
            'keywords': TextInput(attrs={
                 'class': 'form-control',
                'data - size': "10",
                'data - parsley - group': "step-3",
            }),
            'references': TextInput(attrs={
                'class': 'form-control',
                'data - size': "10",
                'data - parsley - group': "step-3",
            }),
        }
