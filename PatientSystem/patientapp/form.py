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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patientname'].queryset = PatientRegistration.objects.all().order_by('firstname')
        self.fields['patientname'].label_from_instance = lambda obj: f"{obj.firstname} {obj.middlename or ''} {obj.lastname}".strip()
        # Make all fields required
        for field in self.fields.values():
            field.required = True
    def clean(self):
        cleaned_data = super().clean()
        height = cleaned_data.get('height')
        weight = cleaned_data.get('weight')
        if height and weight:
            try:
                height_m = float(height) / 100 if float(height) > 10 else float(height)  # Accept cm or m
                bmi = float(weight) / (height_m ** 2)
                cleaned_data['bmistatus'] = round(bmi, 2)
            except Exception:
                self.add_error('height', 'Invalid height or weight for BMI calculation.')
        return cleaned_data
    class Meta:
        model = PatientVitals
        fields = ['patientname', 'height', 'weight', 'bmistatus', 'visitdate']
        widgets = {
            'visitdate': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            })
        }
        labels = {
            'bmistatus': 'BMI (auto-calculated)',
        }
        help_texts = {
            'bmistatus': 'BMI = Weight(kg) / Height(m)^2',
        }

class OverweightAssmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patientname'].queryset = PatientRegistration.objects.all().order_by('firstname')
        self.fields['patientname'].label_from_instance = lambda obj: f"{obj.firstname} {obj.middlename or ''} {obj.lastname}".strip()
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patientname'].queryset = PatientRegistration.objects.all().order_by('firstname')
        self.fields['patientname'].label_from_instance = lambda obj: f"{obj.firstname} {obj.middlename or ''} {obj.lastname}".strip()
    class Meta:
        model = GeneralAssment
        fields = ['patientname', 'visitdate', 'generalhealth', 'question2', 'comments']
        widgets = {
            'visitdate': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            })
        }