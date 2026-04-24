from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-2 rounded-lg border-2 border-pink-300 focus:border-pink-500 focus:outline-none',
        'placeholder': 'Enter your email'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 rounded-lg border-2 border-pink-300 focus:border-pink-500 focus:outline-none',
        'placeholder': 'Choose a username'
    }))
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 rounded-lg border-2 border-pink-300 focus:border-pink-500 focus:outline-none',
            'placeholder': 'Enter password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 rounded-lg border-2 border-pink-300 focus:border-pink-500 focus:outline-none',
            'placeholder': 'Confirm password'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered!')
        return email

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 rounded-lg border-2 border-pink-300 focus:border-pink-500 focus:outline-none',
        'placeholder': 'Enter username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 rounded-lg border-2 border-pink-300 focus:border-pink-500 focus:outline-none',
        'placeholder': 'Enter password'
    }))

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 rounded-lg border-2 border-pink-300 focus:border-pink-500 focus:outline-none',
        'placeholder': 'First name'
    }))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 rounded-lg border-2 border-pink-300 focus:border-pink-500 focus:outline-none',
        'placeholder': 'Last name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-2 rounded-lg border-2 border-pink-300 focus:border-pink-500 focus:outline-none',
        'placeholder': 'Email'
    }))

    class Meta:
        model = UserProfile
        fields = ('bio', 'avatar')
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border-2 border-pink-300 focus:border-pink-500 focus:outline-none',
                'placeholder': 'Tell us about yourself',
                'rows': 4
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border-2 border-pink-300',
                'accept': 'image/*'
            })
        }