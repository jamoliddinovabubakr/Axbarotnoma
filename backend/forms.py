from django import forms
from django.forms import Select, DateInput, PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'username', 'password1', 'password2']

        # widgets = {
        #     'gender': Select(attrs={
        #         'class': 'form-control',
        #     }),
        #     'region': Select(attrs={
        #         'class': 'form-control',
        #     }),
        #     'district': Select(attrs={
        #         'class': 'form-control',
        #     })
        # }