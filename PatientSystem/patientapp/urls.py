from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('patient-registration/', views.patient_registration, name='patient_registration'),
    path('patient-vitals/', views.patient_vitals, name='patient_vitals'),
    path('overweight-assessment/', views.overweight_assessment, name='overweight_assessment'),
    path('general-assessment/', views.general_assessment, name='general_assessment'),
    path('patient-listing/', views.patient_listing, name='patient_listing'),
    path('logout/', views.logout_view, name='logout'),

]