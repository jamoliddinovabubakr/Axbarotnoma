from django import forms
from django.forms import TextInput, Textarea, FileInput, Select
from article_app.models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['section', 'title', 'article_type', 'article_lang', 'country']

        widgets = {
            'country': Select(attrs={
                'class': 'form-control selectpicker',
                'data-size': "10",
                'data-live-search': "true",
                'data-style': "btn-white",
                'data-placeholder': "Tanlang",
                'data-parsley-required': "true",
            }),
            'article_type': Select(attrs={
                'class': 'form-control selectpicker',
                'data - size': "10",
                'data-live-search': "true",
                'data-style': "btn-white",
                'data - parsley - required': "true",
            }),
            'article_lang': Select(attrs={
                'class': 'form-control selectpicker',
                'data - size': "10",
                'data-live-search': "true",
                'data-style': "btn-white",
                'data - parsley - required': "true",
            }),
            'section': Select(attrs={
                'class': 'form-control selectpicker',
                'data - size': "10",
                'data-live-search': "true",
                'data-style': "btn-white",
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
    abstract = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = ['title', 'title_en', 'section', 'abstract', 'keywords', 'abstract_en', 'keywords_en', 'references',
                  'article_type', 'article_lang', 'country']

        widgets = {
            'section': Select(attrs={
                'class': 'form-control selectpicker',
                'data-live-search': "true",
                'data-style': "btn-white",
                'name': 'section',
                'id': 'id_section',
            }),
            'title': Textarea(attrs={
                'class': 'form-control title',
                'rows': '1',
                'name': 'title',
                'id': 'id_title',
            }),
            'title_en': Textarea(attrs={
                'class': 'form-control title_en',
                'rows': '1',
                'name': 'title-en',
                'id': 'id_title_en',
            }),
            # 'abstract': Textarea(attrs={
            #     'class': 'form-control',
            #     'rows': '3',
            #     'placeholder': 'Enter...',
            #     'name': 'abstract',
            #     'id': 'id_abstract',
            # }),
            # 'abstract_en': Textarea(attrs={
            #     'class': 'form-control',
            #     'rows': '3',
            #     'name': 'abstract_en',
            #     'id': 'id_abstract_en',
            # }),
            'keywords': Textarea(attrs={
                'class': 'form-control',
                'name': 'keywords',
                'id': 'id_keywords',
                'rows': '3',
            }),
            'keywords_en': Textarea(attrs={
                'class': 'form-control',
                'name': 'keywords_en',
                'id': 'id_keywords_en',
                'rows': '3',
            }),
            'references': Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Enter...',
                'name': 'references',
                'id': 'id_references',

            }),
            'country': Select(attrs={
                'class': 'form-control selectpicker',
                'data-size': "10",
                'data-live-search': "true",
                'data-style': "btn-white",
                'data-placeholder': "Tanlang",
                'data-parsley-required': "true",
            }),
            'article_type': Select(attrs={
                'class': 'form-control selectpicker',
                'data - size': "10",
                'data-live-search': "true",
                'data-style': "btn-white",
            }),
            'article_lang': Select(attrs={
                'class': 'form-control selectpicker',
                'data - size': "10",
                'data-live-search': "true",
                'data-style': "btn-white",
            }),
        }


class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = ExtraAuthor
        fields = ['article', 'fname', 'lname', 'mname', 'email', 'work', 'scientific_degree']

        widgets = {
            'fname': TextInput(attrs={
                'id': 'author_fname',
                'class': 'form-control',
                'type': 'text',
                'placeholder': "Enter...",
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
            'scientific_degree': Select(attrs={
                'class': 'form-control',
                'data-live-search': "true",
                'data-style': "btn-white",
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
