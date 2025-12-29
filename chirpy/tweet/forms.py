from django import forms
from .models import Tweet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light border-secondary rounded-4 fs-5',
                'rows': 5,
                'placeholder': "What's happening?",
                'style': 'resize:none;'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control bg-dark text-light'
            }),
        }
        
class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-light border-secondary rounded-3',
        'placeholder': 'Username'
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control bg-dark text-light border-secondary rounded-3',
        'placeholder': 'Email'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control bg-dark text-light border-secondary rounded-3',
        'placeholder': 'Password'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control bg-dark text-light border-secondary rounded-3',
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
