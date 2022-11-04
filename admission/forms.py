from logging import PlaceHolder
from pyexpat import model
from django import forms
from django.forms import TextInput, Textarea, DateInput
from .models import *

class CustomDateInput(DateInput):
    input_type = 'date'

class ApplicantForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=CustomDateInput)

    class Meta:
        model = Applicant
        exclude = ('age', 'sessions',)
        widgets = {
            'first_name': TextInput(attrs={'PlaceHolder': 'First Name'}),
            'second_name': TextInput(attrs={'PlaceHolder': 'Second Name'}),
            'last_name': TextInput(attrs={'PlaceHolder': 'Last Name'}),
            'phone_number': TextInput(attrs={'PlaceHolder': '0814 614 9773'}),
            'email_address': TextInput(attrs={'PlaceHolder': 'Email Address'}),
            'per_address': Textarea(attrs={'placeholder': 'Present Address', 'rows': 4,}),
            'class_room': TextInput(attrs={'PlaceHolder': 'Requested Class'}),
        }

class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        exclude = ('applicant',)
        widgets = {
            'name': TextInput(attrs={'PlaceHolder': 'Sponsor/Guardian Fullname'}),
            'phone_number': TextInput(attrs={'PlaceHolder': '0814 614 9773'}),
            'email_address': TextInput(attrs={'PlaceHolder': 'Email Address'}),
            'per_address': Textarea(attrs={'placeholder': 'Permanent Address', 'rows': 4,}),
        }

class NextOfKinForm(forms.ModelForm):
    class Meta:
        model = NextOfKin
        exclude = ('applicant',)
        widgets = {
            'name': TextInput(attrs={'PlaceHolder': 'Next of Kin Fullname'}),
            'phone_number': TextInput(attrs={'PlaceHolder': '0814 614 9773'}),
            'email_address': TextInput(attrs={'PlaceHolder': 'Email Address'}),
            'per_address': Textarea(attrs={'placeholder': 'Permanent Address', 'rows': 4,}),
        }

class ClassSectionForm(forms.ModelForm):
    class Meta:
        model = classSection
        fields = '__all__'
        widgets = {
            'classes': TextInput(attrs={'placeholder': 'Enter Classes separated by comma (,)'})
        }

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('session',)
        widgets = {
            'session': TextInput(attrs={'Placeholder': '2022/2023'})
        }