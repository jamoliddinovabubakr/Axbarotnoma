from django import forms
from django.forms import Select, DateInput, PasswordInput, TextInput, EmailInput, NumberInput, ModelMultipleChoiceField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from article_app.models import Category
from .models import User, Menu, Role, State, Region, Notification


class CreateUserForm(UserCreationForm):
    choices = [['', '']]
    query = Category.objects.all().values().order_by('name')
    if query:
        choices = [[x['id'], x['name']] for x in query]

    speciality = forms.MultipleChoiceField(choices=choices, required=True, widget=forms.SelectMultiple(attrs={
        'class': 'multiple-select2 form-control',
        'multiple': 'multiple',
        'data - size': "10",
        'data-live-search': "true",
        'data - style': "btn-white",
        'data - parsley - required': "true",
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'speciality', 'password1', 'password2']


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'middle_name', 'birthday', 'avatar', 'email',
                  'phone', 'passport', 'region', 'role']

        widgets = {
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': "Enter...",
                'data - parsley - group': "step-1",
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': "Enter...",
                'data - parsley - group': "step-1",
            }),
            'middle_name': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': "Enter...",
                'data - parsley - group': "step-1",
            }),
            'username': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': "Enter...",
                'data - parsley - group': "step-1",
                'data - parsley - required': "true",
            }),
            'phone': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'id': 'masked-input-phone',
                'placeholder': '(99) 999-99-99',
                'data - parsley - group': "step-1",
            }),
            'passport': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'id': 'masked-input-pasport',
                'placeholder': 'AA 9999999',
                'data - parsley - group': "step-1",
            }),
            'role': Select(attrs={
                'class': 'form-control selectpicker',
                'data - size': "10",
                'data-live-search': "true",
                'data - style': "btn-white",
                'data - parsley - group': "step-1",
            }),
            'email': TextInput(attrs={
                'class': 'form-control',
                'type': 'email',
                'data-parsley-type': "email",
                'placeholder': 'someone@example.com',
                'data - parsley - group': "step-1",
                'data - parsley - required': "true",
            }),

            'region': Select(attrs={
                'class': 'form-control selectpicker',
                'data - size': "10",
                'data-live-search': "true",
                'data - style': "btn-white",
                'data - parsley - group': "step-1",
            }),
        }


class CreateMenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'parent_id', 'icon', 'url', 'type_menu', 'menu_tr', 'status', 'allowed_roles']

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter...",
            }),
            'parent_id': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter...",
            }),
            'icon': TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter...",
            }),
            'url': TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter...",
        
            }),
            'type_menu': NumberInput(attrs={
                'class': 'form-control',
            }),
            'menu_tr': NumberInput(attrs={
                'class': 'form-control',
            }),
        }


class CreateRoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'status']

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter...",
            }),
        }


# class CreateGenderForm(forms.ModelForm):
#     class Meta:
#         model = Gender
#         fields = ['name', 'status']
#
#         widgets = {
#             'name': TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': "Enter...",
#             }),
#         }


class CreateStateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ['name', 'status']

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter...",
            }),
        }


class CreateRegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name', 'key']

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter...",
            }),

            'key': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter...",
            }),
        }


class CreateNotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['article', 'title', 'description', 'status']

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': "Enter...",
                'data - parsley - required': "true",
            }),
            'description': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': "Enter...",
                'data - parsley - required': "true",
            }),
            'article': Select(attrs={
                'class': 'form-control selectpicker',
                'data - size': "10",
                'data-live-search': "true",
                'data - style': "btn-white",
                'data - parsley - required': "true",
            }),
            'status': Select(attrs={
                'class': 'form-control selectpicker',
                'data - size': "10",
                'data-live-search': "true",
                'data - style': "btn-white",
            }),
        }