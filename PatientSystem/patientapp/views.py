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
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('/login/')
        elif 'password1' in form.errors or 'password2' in form.errors:
            # If password2 error contains 'The two password fields didn’t match.' show match error, else show requirements error
            password2_errors = form.errors.get('password2', [])
            if any('match' in str(e).lower() for e in password2_errors):
                messages.error(request, "Passwords do not match.")
            else:
                messages.error(request, "Password does not meet requirements.")
    else:
        form = SignUpForm()
    return render(request, 'patientapp/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Debug print (remove in production)
        print(f"Login attempt: username={username}")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('/patient-registration/')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    
    # GET request or failed login
    return render(request, 'patientapp/login.html')

#@login_required
def patient_registration(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            # Check for duplicate patient (by patientno or unique name/dob combo)
            patientno = form.cleaned_data['patientno']
            if PatientRegistration.objects.filter(patientno=patientno).exists():
                messages.error(request, "A patient with this Patient Number already exists!")
            else:
                # Optionally, check for duplicate by name and DOB
                firstname = form.cleaned_data['firstname']
                lastname = form.cleaned_data['lastname']
                dateofbirth = form.cleaned_data['dateofbirth']
                if PatientRegistration.objects.filter(firstname=firstname, lastname=lastname, dateofbirth=dateofbirth).exists():
                    messages.error(request, "A patient with this name and date of birth already exists!")
                else:
                    patient = form.save()
                    messages.success(request, "Patient registered successfully!")
                    # Redirect to vitals page, optionally pre-selecting the patient
                    return redirect('patient_vitals')
    else:
        form = PatientRegistrationForm()
    patients = PatientRegistration.objects.all().order_by('firstname')
    return render(request, 'Patient registration.html', {'form': form, 'patients': patients})

#@login_required
def patient_vitals(request):
    if request.method == 'POST':
        form = PatientVitalsForm(request.POST)
        if form.is_valid():
            patient = form.cleaned_data['patientname']
            visitdate = form.cleaned_data['visitdate']
            # Only allow one vitals record per patient per date
            if PatientVitals.objects.filter(patientname=patient, visitdate=visitdate).exists():
                messages.error(request, "Vitals for this patient on this date already exist.")
            else:
                # Save with auto-calculated BMI and status
                vitals = form.save(commit=False)
                height = float(form.cleaned_data['height'])
                weight = float(form.cleaned_data['weight'])
                height_m = height / 100 if height > 10 else height
                bmi = float(weight) / (height_m ** 2)
                vitals.bmistatus = round(bmi, 2)
                # Set BMI status
                if bmi < 18.5:
                    vitals.bmistatus = f"{vitals.bmistatus} (Underweight)"
                elif 18.5 <= bmi < 25:
                    vitals.bmistatus = f"{vitals.bmistatus} (Normal)"
                else:
                    vitals.bmistatus = f"{vitals.bmistatus} (Overweight)"
                vitals.save()
                messages.success(request, "Vitals recorded successfully!")
                # Redirect based on BMI
                if bmi <= 25:
                    return redirect('general_assessment')
                else:
                    return redirect('overweight_assessment')
    else:
        form = PatientVitalsForm()
    vitals = PatientVitals.objects.all().order_by('-visitdate')
    return render(request, 'Vitals.html', {'form': form, 'vitals': vitals})

#@login_required
def overweight_assessment(request):
    # Only allow access if a valid BMI > 25 is present in the latest vitals for a patient (session or query param)
    latest_vitals = None
    if request.method == 'GET':
        patient_id = request.GET.get('patient')
        if patient_id:
            from .models import PatientVitals
            latest_vitals = PatientVitals.objects.filter(patientname_id=patient_id).order_by('-visitdate').first()
            if not latest_vitals or latest_vitals.bmistatus <= 25:
                messages.error(request, "Overweight Assessment is only available for patients with BMI > 25.")
                return redirect('patient_vitals')
    if request.method == 'POST':
        form = OverweightAssmentForm(request.POST)
        # Make all fields required
        for field in form.fields.values():
            field.required = True
        if form.is_valid():
            patient = form.cleaned_data['patientname']
            visitdate = form.cleaned_data['visitdate']
            # Only allow one assessment per patient per date
            if OverweightAssment.objects.filter(patientname=patient, visitdate=visitdate).exists():
                messages.error(request, "Overweight assessment for this patient on this date already exists.")
            else:
                form.save()
                messages.success(request, "Overweight assessment saved!")
                return redirect('patient_listing')
    else:
        form = OverweightAssmentForm()
    assessments = OverweightAssment.objects.all().order_by('-visitdate')
    return render(request, 'Overweight form.html', {'form': form, 'assessments': assessments})

def general_assessment(request):
    # Only allow access if a valid BMI <= 25 is present in the latest vitals for a patient (session or query param)
    latest_vitals = None
    if request.method == 'GET':
        patient_id = request.GET.get('patient')
        if patient_id:
            from .models import PatientVitals
            latest_vitals = PatientVitals.objects.filter(patientname_id=patient_id).order_by('-visitdate').first()
            if not latest_vitals or latest_vitals.bmistatus > 25:
                messages.error(request, "General Assessment is only available for patients with BMI ≤ 25.")
                return redirect('patient_vitals')
    if request.method == 'POST':
        form = GeneralAssmentForm(request.POST)
        # Make all fields required
        for field in form.fields.values():
            field.required = True
        if form.is_valid():
            patient = form.cleaned_data['patientname']
            visitdate = form.cleaned_data['visitdate']
            # Only allow one assessment per patient per date
            if GeneralAssment.objects.filter(patientname=patient, visitdate=visitdate).exists():
                messages.error(request, "General assessment for this patient on this date already exists.")
            else:
                form.save()
                messages.success(request, "General assessment saved!")
                return redirect('patient_listing')
    else:
        form = GeneralAssmentForm()
    assessments = GeneralAssment.objects.all().order_by('-visitdate')
    return render(request, 'General form.html', {'form': form, 'assessments': assessments})

#@login_required
def patient_listing(request):
    visitdate = request.GET.get('visitdate')
    listings = PatientListing.objects.all().order_by('-lastassessmentdate')
    if visitdate:
        listings = listings.filter(lastassessmentdate=visitdate)
    return render(request, 'Patient listing.html', {'listings': listings, 'visitdate': visitdate})

def logout_view(request):
    logout(request)
    return redirect('login')