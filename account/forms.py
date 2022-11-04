from django import forms
from django.forms import TextInput
from .models import Account

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs={'PlaceHolder': 'Password'}), max_length=16)
	class Meta:
		model 	= Account
		fields 	= ('name', 'phone_number', 'email', 'username', 'password',)
		widgets = {
            'name': TextInput(attrs={'PlaceHolder': 'Enter Fullname'}),
            'phone_number': TextInput(attrs={'PlaceHolder': '0814 614 9773'}),
            'email': TextInput(attrs={'PlaceHolder': 'Email Address'}),
            'username': TextInput(attrs={'PlaceHolder': 'Username'}),
        }

class LoginForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs={'PlaceHolder': 'Password'}), max_length=16)
	class Meta:
		model 	= Account
		fields 	= ('username', 'password',)
		widgets = {
            'username': TextInput(attrs={'PlaceHolder': 'Username'}),
        }