# Dans KidalApp/forms.py

from django import forms

class MessageForm(forms.Form):
    message = forms.CharField(label='Votre message', widget=forms.Textarea(attrs={'rows': 4}))
from django import forms
from .models import CustomUser

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'adresse']

