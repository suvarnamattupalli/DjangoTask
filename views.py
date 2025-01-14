from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm, LoginForm
from django.contrib.auth.models import User
from .models import Profile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            # Create the user
            user = form.save()

            # Check if the user already has a profile
            if Profile.objects.filter(user=user).exists():
                # If the profile exists, show a message and redirect to the login page
                messages.error(request, 'Profile already exists. Please log in.')
                return redirect('login')  # Redirect to the login page or wherever needed
            else:
                # If no profile exists, create a new profile
                profile = Profile.objects.create(
                    user=user,
                    profile_picture=form.cleaned_data.get('profile_picture'),
                    address_line1=form.cleaned_data.get('address_line1'),
                    city=form.cleaned_data.get('city'),
                    state=form.cleaned_data.get('state'),
                    pincode=form.cleaned_data.get('pincode')
                )

                # Optionally, you can show a success message here
                messages.success(request, 'Account created successfully. Please log in.')

                return redirect('login')  # Redirect to the login page after successful signup
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                # Redirect to respective dashboard based on user type
                if user.user_type == 'patient':
                    return redirect('patient_dashboard')  # Redirect to patient dashboard
                elif user.user_type == 'doctor':
                    return redirect('doctor_dashboard')  # Redirect to doctor dashboard
                else:
                    return redirect('default_dashboard')  # Default dashboard for other users
            else:
                form.add_error(None, 'Invalid username or password')  # Add error if authentication fails
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def patient_dashboard(request):
    return render(request, 'patient_dashboard.html')

def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')

def default_dashboard(request):
    return render(request, 'default_dashboard.html')
