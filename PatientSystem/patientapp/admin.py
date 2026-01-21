from django.contrib import admin
from .models import PatientListing


@admin.register(PatientListing)
class PatientListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'patientname', 'age', 'bmistatus', 'lastassessmentdate')