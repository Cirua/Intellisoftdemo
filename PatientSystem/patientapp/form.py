from django import forms
from .models import PatientRegistration, PatientVitals, OverweightAssment, GeneralAssment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = PatientRegistration
        fields = ['firstname', 'middlename', 'lastname', 'gender', 'dateofbirth', 'patientno', 'registrationdate']
        widgets = {
            'registrationdate': forms.DateInput(attrs={
                'type': 'date',  # HTML5 date picker
                'class': 'form-control'
            })
        }

class PatientVitalsForm(forms.ModelForm):
    class Meta:
        model = PatientVitals
        fields = ['patientname', 'height', 'weight', 'bmistatus', 'visitdate']
        widgets = {
            'visitdate': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            })
        }

class OverweightAssmentForm(forms.ModelForm):
    class Meta:
        model = OverweightAssment
        fields = ['patientname', 'visitdate', 'generalhealth', 'question1', 'comments']
        widgets = {
            'visitdate': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            })
        }

class GeneralAssmentForm(forms.ModelForm):
    class Meta:
        model = GeneralAssment
        fields = ['patientname', 'visitdate', 'generalhealth', 'question2', 'comments']
        widgets = {
            'visitdate': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            })
        }