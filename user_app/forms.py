from django import forms
from django.forms import Select, DateInput, PasswordInput, TextInput, EmailInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'username', 'password1', 'password2']


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'middle_name', 'birthday', 'gender', 'avatar', 'email',
                  'phone', 'passport', 'work_place', 'position', 'region', 'district']

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
                'data - parsley - group': "step-2",
                'data - parsley - required': "true",
            }),
            'phone': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'id': 'masked-input-phone',
                'placeholder': '(99) 999-99-99',
                'data - parsley - group': "step-2",
            }),
            'passport': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'id': 'masked-input-passport',
                'placeholder': 'AA 9999999',
                'data - parsley - group': "step-2",
            }),
            # 'email': TextInput(attrs={
            #     'class': 'form-control',
            #     'type': 'email',
            #     'data-parsley-type': "email",
            #     'placeholder': 'someone@example.com',
            #     'data - parsley - group': "step-2",
            #     'data - parsley - required': "true",
            # }),
            # 'birthday': DateInput(attrs={
            #     'class': 'form-control',
            #     'type': 'date',
            #     'data - parsley - group': "step-1",
            # }),
            'region': Select(attrs={
                'class': 'form-control selectpicker',
                'data - size': "10",
                'data-live-search': "true",
                'data - style': "btn-white",
                'data - parsley - group': "step-1",
            }),
            'district': Select(attrs={
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
            'work_place': TextInput(attrs={
                'class': 'form-control m-b-10',
                'type': 'text',
                'placeholder': "Enter...",
                'data - parsley - group': "step-2",
            }),
            'position': TextInput(attrs={
                'class': 'form-control m-b-10',
                'type': 'text',
                'placeholder': "Enter...",
                'data - parsley - group': "step-2",
            }),

        }
