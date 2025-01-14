from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import User, Profile

# Get the custom user model
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text=(
            "Your password must be at least 8 characters long, "
            "not entirely numeric, and not too similar to your personal information."
        ),
        error_messages={
            'password_too_similar': "The password is too similar to your personal information.",
            'password_too_short': "The password must contain at least 8 characters.",
            'password_common': "The password is too common.",
            'password_entirely_numeric': "The password cannot be entirely numeric.",
        },
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        help_texts = {
            'username': 'Enter a unique username.',
        }


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    profile_picture = forms.ImageField(required=False)
    address_line1 = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Address Line 1'}))
    city = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'City'}))
    state = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'State'}))
    pincode = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'placeholder': 'Pincode'}))
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'user_type', 'profile_picture', 'address_line1', 'city', 'state', 'pincode']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            raise ValidationError("Password and Confirm Password do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()

        # Save additional fields in the Profile model
        Profile.objects.create(
            user=user,
            profile_picture=self.cleaned_data.get('profile_picture'),
            address_line1=self.cleaned_data['address_line1'],
            city=self.cleaned_data['city'],
            state=self.cleaned_data['state'],
            pincode=self.cleaned_data['pincode']
        )
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
