from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input rounded-md shadow-sm mt-1 block w-full'})
        self.fields['email'].widget.attrs.update({'class': 'form-input rounded-md shadow-sm mt-1 block w-full'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-input rounded-md shadow-sm mt-1 block w-full'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-input rounded-md shadow-sm mt-1 block w-full'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-input rounded-md shadow-sm mt-1 block w-full'})
        self.fields['address'].widget.attrs.update({'class': 'form-textarea rounded-md shadow-sm mt-1 block w-full'})
        self.fields['password1'].widget.attrs.update({'class': 'form-input rounded-md shadow-sm mt-1 block w-full'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input rounded-md shadow-sm mt-1 block w-full'})

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input rounded-md shadow-sm mt-1 block w-full'})
        self.fields['email'].widget.attrs.update({'class': 'form-input rounded-md shadow-sm mt-1 block w-full'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-input rounded-md shadow-sm mt-1 block w-full'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-input rounded-md shadow-sm mt-1 block w-full'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-input rounded-md shadow-sm mt-1 block w-full'})
        self.fields['address'].widget.attrs.update({'class': 'form-textarea rounded-md shadow-sm mt-1 block w-full'}) 