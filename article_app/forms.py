from django import forms
from django.forms import TextInput, Textarea, FileInput, NumberInput, SelectMultiple
from .models import Article, Category, Authors, Journal, MyResendArticle


class CreateArticleForm(forms.Form):
    choices = [['', '']]
    query = Category.objects.all().values().order_by('name')
    if query:
        choices = [[x['id'], x['name']] for x in query]

    category = forms.MultipleChoiceField(choices=choices, required=True, widget=forms.SelectMultiple(attrs={
        'class': 'multiple-select2 form-control',
        'multiple': 'multiple',
        'data - size': "10",
        'data-live-search': "true",
        'data - style': "btn-white",
        'data - parsley - required': "true",
    }))
    title = forms.CharField(max_length=255, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'data - size': "10",
        'data - parsley - required': "true",
    }))


class CreateMyResendArticleForm(forms.ModelForm):
    class Meta:
        model = MyResendArticle
        fields = ['author', 'article', 'file_word']


class UpdateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'abstract', 'keywords', 'references', 'file', 'author']

        widgets = {
            'category': SelectMultiple(attrs={
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
            'file': FileInput(attrs={
                'id': 'id_file',
                'type': 'file',
                'class': 'form-control',
                'accept': ".docx, .doc"
            }),
        }


class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Authors
        fields = ['article', 'first_name', 'last_name', 'middle_name', 'email', 'work_place', 'author_order']

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


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'status']

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': "Enter...",
                'data - parsley - required': "true",
            }),
        }


class CreateMagazineForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['number_magazine', 'year_magazine']

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


class UpdateMagazineForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['number_magazine', 'year_magazine', 'article', 'status']

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
