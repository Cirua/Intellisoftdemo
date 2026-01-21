from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import PatientRegistration, PatientVitals, OverweightAssment, GeneralAssment, PatientListing
from .form import SignUpForm, PatientRegistrationForm, PatientVitalsForm, OverweightAssmentForm, GeneralAssmentForm
from django.contrib import messages



def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'patientapp/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'patientapp/login.html', {'error': 'Invalid credentials'})
    return render(request, 'patientapp/login.html')

@login_required
def patient_registration(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient registered successfully!")
            return redirect('patient_registration')
    else:
        form = PatientRegistrationForm()
    patients = PatientRegistration.objects.all().order_by('firstname')
    return render(request, 'Patient registration.html', {'form': form, 'patients': patients})

@login_required
def patient_vitals(request):
    if request.method == 'POST':
        form = PatientVitalsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vitals recorded successfully!")
            return redirect('patient_vitals')
    else:
        form = PatientVitalsForm()
    vitals = PatientVitals.objects.all().order_by('-visitdate')
    return render(request, 'Vitals.html', {'form': form, 'vitals': vitals})

@login_required
def overweight_assessment(request):
    if request.method == 'POST':
        form = OverweightAssmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Overweight assessment saved!")
            return redirect('overweight_assessment')
    else:
        form = OverweightAssmentForm()
    assessments = OverweightAssment.objects.all().order_by('-visitdate')
    return render(request, 'Overweight form.html', {'form': form, 'assessments': assessments})

def general_assessment(request):
    if request.method == 'POST':
        form = GeneralAssmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "General assessment saved!")
            return redirect('general_assessment')
    else:
        form = GeneralAssmentForm()
    assessments = GeneralAssment.objects.all().order_by('-visitdate')
    return render(request, 'General form.html', {'form': form, 'assessments': assessments})

@login_required
def patient_listing(request):
    listings = PatientListing.objects.all().order_by('-lastassessmentdate')
    return render(request, 'Patient listing.html', {'listings': listings})

def logout_view(request):
    logout(request)
    return redirect('login')