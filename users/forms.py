from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User

class CustomLoginForm(AuthenticationForm):
    """Custom login form with enhanced styling and validation."""
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add common classes to all fields
        common_classes = 'appearance-none block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 transition duration-150 ease-in-out sm:text-sm'
        
        self.fields['username'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Enter your username'
        })
        self.fields['password'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Enter your password'
        })

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    address = forms.CharField(required=True, widget=forms.TextInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add common classes to all fields
        common_classes = 'appearance-none block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 transition duration-150 ease-in-out sm:text-sm'
        
        self.fields['username'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Enter your username'
        })
        self.fields['email'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Enter your email'
        })
        self.fields['first_name'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'First name'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Last name'
        })
        self.fields['phone_number'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Enter your phone number'
        })
        self.fields['address'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Enter your address'
        })
        self.fields['password1'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Confirm your password'
        })

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