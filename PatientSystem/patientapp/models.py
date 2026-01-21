from django.db import models


class PatientRegistration(models.Model):
    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100, blank=True, null=True) #this make the field allow null values
    lastname = models.CharField(max_length=100)
    gender = models.Choices()
    dateofbirth = models.DateField()
    patientno = models.DecimalField(max_digits=10, unique=True)
    registrationdate = models.DateField()

    def __str__(self):
        return f"{self.firstname} {self.middlename or ''} {self.lastname}".strip()
    
class PatientVitals(models.Model):
    patientname = models.ForeignKey(PatientRegistration, on_delete=models.CASCADE)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    bmistatus = models.CharField(max_length=50)
    visitdate = models.DateField()

    def __str__(self):
        return f"Vitals for {self.patientname.firstname} on {self.visitdate}"
    
class OverweightAssment(models.Model):
    patientname = models.ForeignKey(PatientRegistration, on_delete=models.CASCADE)
    visitdate = models.DateField()
    generalhealth = models.Choices()
    question1 = models.Choices()
    comments = models.TextField()

    def __str__(self):
        return f"Overweight Assessment for {self.patientname.firstname} on {self.visitdate}"
    
class GeneralAssment(models.Model):
    patientname = models.ForeignKey(PatientRegistration, on_delete=models.CASCADE)
    visitdate = models.DateField()
    generalhealth = models.Choices()
    question2 = models.Choices()
    comments = models.TextField()

    def __str__(self):
        return f"General Assessment for {self.patientname.firstname} on {self.visitdate}"    

class PatientListing(models.Model):
    patientname = models.ForeignKey(PatientRegistration, on_delete=models.CASCADE)
    age = models.IntegerField()
    bmistatus = models.CharField(max_length=50)
    lastassessmentdate = models.DateField()

    def __str__(self):
        return f"Listing #{self.id} - {self.patientname.firstname} {self.patientname.lastname}"
