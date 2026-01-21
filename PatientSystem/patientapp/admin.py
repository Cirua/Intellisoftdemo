from django.contrib import admin
from .models import PatientListing


@admin.register(PatientListing)
class PatientAdmin():
    list_display = ('patientname', 'age', 'bmistatus', 'lastassessmentdate')
    list_filter = ('lastassessmentdate',)