from django import forms
from django.forms import Select, DateInput, PasswordInput, TextInput
from .models import Article, Category, Author


class AddArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'abstract', 'keywords', 'references', 'file']

        widgets = {
            'category': Select(attrs={
                'class': 'form-control selectpicker',
                'data - size': "10",
                'data-live-search': "true",
                'data - style': "btn-white",
                'data - parsley - group': "step-1",
            }),
            # 'role': Select(attrs={
            #     'class': 'form-control',
            # })
        }
