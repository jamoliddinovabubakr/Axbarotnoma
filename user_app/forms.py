from django import forms
from django.forms import Select, DateInput, PasswordInput, TextInput, EmailInput, NumberInput, ModelMultipleChoiceField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from user_app.models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'username', 'email', 'password1', 'password2']


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'middle_name', 'birthday', 'avatar', 'email',
                  'phone', 'pser', 'pnum', 'region', 'gender', 'work']

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
            'pser': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'id': 'masked-input-pasport',
                'placeholder': 'AA',
                'data - parsley - group': "step-1",
            }),
            'pnum': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'id': 'masked-input-pasport',
                'placeholder': '9999999',
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
            'gender': Select(attrs={
                'class': 'form-control selectpicker',
                'data - size': "10",
                'data-live-search': "true",
                'data - style': "btn-white",
                'data - parsley - group': "step-1",
            }),
            'work': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Enter',
                'data - parsley - group': "step-1",
            }),
        }


class AddReviewerForm(forms.ModelForm):
    class Meta:
        model = Reviewer
        fields = ['user', 'mfile', 'section']

        widgets = {
            'section': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'id': 'masked-input-phone',
                'placeholder': '(99) 999-99-99',
                'data - parsley - group': "step-1",
            }),
            'mfile': TextInput(attrs={
                'class': 'form-control',
                'type': 'email',
                'data-parsley-type': "email",
                'placeholder': 'someone@example.com',
                'data - parsley - group': "step-1",
                'data - parsley - required': "true",
            }),
        }

# class CreateMenuForm(forms.ModelForm):
#     class Meta:
#         model = Menu
#         fields = ['name', 'parent_id', 'icon', 'url', 'type_menu', 'menu_tr', 'status', 'allowed_roles']
#
#         widgets = {
#             'name': TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': "Enter...",
#             }),
#             'parent_id': NumberInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': "Enter...",
#             }),
#             'icon': TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': "Enter...",
#             }),
#             'url': TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': "Enter...",
#
#             }),
#             'type_menu': NumberInput(attrs={
#                 'class': 'form-control',
#             }),
#             'menu_tr': NumberInput(attrs={
#                 'class': 'form-control',
#             }),
#         }
#
#
# class CreateRoleForm(forms.ModelForm):
#     class Meta:
#         model = Role
#         fields = ['name', 'status']
#
#         widgets = {
#             'name': TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': "Enter...",
#             }),
#         }
#

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


# class CreateStateForm(forms.ModelForm):
#     class Meta:
#         model = State
#         fields = ['name', 'status']
#
#         widgets = {
#             'name': TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': "Enter...",
#             }),
#         }
#
#
# class CreateRegionForm(forms.ModelForm):
#     class Meta:
#         model = Region
#         fields = ['name', 'key']
#
#         widgets = {
#             'name': TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': "Enter...",
#             }),
#
#             'key': NumberInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': "Enter...",
#             }),
#         }
#
#
# class CreateNotificationForm(forms.ModelForm):
#     class Meta:
#         model = Notification
#         fields = ['article', 'title', 'description', 'status']
#
#         widgets = {
#             'title': TextInput(attrs={
#                 'class': 'form-control',
#                 'type': 'text',
#                 'placeholder': "Enter...",
#                 'data - parsley - required': "true",
#             }),
#             'description': TextInput(attrs={
#                 'class': 'form-control',
#                 'type': 'text',
#                 'placeholder': "Enter...",
#                 'data - parsley - required': "true",
#             }),
#             'article': Select(attrs={
#                 'class': 'form-control selectpicker',
#                 'data - size': "10",
#                 'data-live-search': "true",
#                 'data - style': "btn-white",
#                 'data - parsley - required': "true",
#             }),
#             'status': Select(attrs={
#                 'class': 'form-control selectpicker',
#                 'data - size': "10",
#                 'data-live-search': "true",
#                 'data - style': "btn-white",
#             }),
#         }