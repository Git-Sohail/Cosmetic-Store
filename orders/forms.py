from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'notes']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-input rounded-md shadow-sm mt-1 block w-full'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-input rounded-md shadow-sm mt-1 block w-full'})
        self.fields['email'].widget.attrs.update({'class': 'form-input rounded-md shadow-sm mt-1 block w-full'})
        self.fields['phone'].widget.attrs.update({'class': 'form-input rounded-md shadow-sm mt-1 block w-full'})
        self.fields['address'].widget.attrs.update({'class': 'form-textarea rounded-md shadow-sm mt-1 block w-full'})
        self.fields['notes'].widget.attrs.update({'class': 'form-textarea rounded-md shadow-sm mt-1 block w-full'}) 