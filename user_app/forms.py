from django import forms
from django.forms import Select, TextInput, SelectMultiple
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from user_app.models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'middle_name', 'username', 'email', 'password1', 'password2']


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'middle_name', 'birthday', 'avatar', 'email',
                  'phone', 'pser', 'pnum', 'region', 'gender', 'work']

        widgets = {
            'first_name': TextInput(attrs={
                'class': 'form-control first_name',
                'type': 'text',
                'placeholder': "Surname",
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control last_name',
                'type': 'text',
                'placeholder': "Name",
            }),
            'middle_name': TextInput(attrs={
                'class': 'form-control middle_name',
                'type': 'text',
                'placeholder': "Middle",
            }),
            'username': TextInput(attrs={
                'class': 'form-control username',
                'type': 'text',
                'placeholder': "Username",
                'data - parsley - required': "true",
            }),
            'phone': TextInput(attrs={
                'class': 'form-control phone',
                'type': 'text',
                'id': 'masked-input-phone',
                'placeholder': 'Phone Number',
            }),
            'pser': TextInput(attrs={
                'class': 'form-control pser',
                'type': 'text',
                'id': 'masked-input-pasport',
                'placeholder': 'Passport Seria',
                'data - parsley - group': "step-1",
            }),
            'pnum': TextInput(attrs={
                'class': 'form-control pnum',
                'type': 'text',
                'id': 'masked-input-pasport',
                'placeholder': 'Passport Number',
            }),
            'email': TextInput(attrs={
                'class': 'form-control email',
                'type': 'email',
                'placeholder': 'Email',
            }),

            'region': Select(attrs={
                'class': 'form-control region',
                'data-live-search': "true",
                'data-style': "btn-white",
            }),
            'gender': Select(attrs={
                'class': 'form-control gender',
                'data-live-search': "true",
                'data-style': "btn-white",
            }),
            'work': TextInput(attrs={
                'class': 'form-control work',
                'type': 'text',
                'placeholder': 'Please enter your work',
            }),
        }


class ReviewerFileForm(forms.ModelForm):
    file = forms.FileField(
        label="Files",
        widget=forms.ClearableFileInput(attrs={"multiple": True, "name": "file"})
    )

    class Meta:
        model = ReviewerFile
        fields = ['file']


class AddReviewerForm(forms.ModelForm):
    class Meta:
        model = Reviewer
        fields = ['user', 'section', 'scientific_degree']

        widgets = {
            'section': SelectMultiple(attrs={
                'class': 'multiple-select2 form-control',
                'multiple': 'multiple',
                'placeholder': 'Select',
                'name': 'section',
            }),
            'scientific_degree': Select(attrs={
                'class': 'form-control selectpicker',
                'data-live-search': "true",
                'data-style': "btn-white",
                'name': 'scientific_degree',
            }),
        }
