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
    # Remove the password field from the form
    password = None
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'profile_picture')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'email': forms.EmailInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'first_name': forms.TextInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'last_name': forms.TextInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'phone_number': forms.TextInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'address': forms.Textarea(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md', 'rows': 3}),
            'profile_picture': forms.FileInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
        } 