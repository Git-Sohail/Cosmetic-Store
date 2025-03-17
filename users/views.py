from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Create your views here.

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please login with your credentials.', extra_tags='success')
        return response

@login_required
def profile(request):
    if request.method == 'POST':
        # Check if the user wants to remove their profile picture
        if 'remove_profile_picture' in request.POST:
            if request.user.profile_picture:
                # Delete the profile picture
                request.user.profile_picture.delete(save=True)
                messages.success(request, 'Profile picture removed successfully!', extra_tags='success')
            return redirect('users:profile')
            
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!', extra_tags='success')
            return redirect('users:profile')
        else:
            # Add debug messages for form errors
            messages.error(request, 'Error updating profile. Please check the form.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username:
            messages.error(request, 'Please enter your username.')
            return render(request, 'users/login.html')
        if not password:
            messages.error(request, 'Please enter your password.')
            return render(request, 'users/login.html')
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('products:product_list')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return render(request, 'users/login.html')
    
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('users:login')
