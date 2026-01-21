from django.db import models


class PatientRegistration(models.Model):
    class Gender(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'

    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100, blank=True, null=True) #this make the field allow null values
    lastname = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=6,
        choices=Gender.choices
    )
    dateofbirth = models.DateField()
    patientno = models.DecimalField(max_digits=10, decimal_places=0, unique=True)
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

    class Generalquestion(models.TextChoices):
        GOOD = 'Good', 'Good'
        POOR = 'Poor', 'Poor'

    class Otherquestion(models.TextChoices):
        YES = 'Yes', 'Yes'
        NO = 'No', 'No'

    patientname = models.ForeignKey(PatientRegistration, on_delete=models.CASCADE)
    visitdate = models.DateField()
    generalhealth = models.CharField(
         max_length=5,
        choices=Generalquestion.choices
    )
    question1 = models.CharField(
        max_length=5,
        choices=Otherquestion.choices
    )
    comments = models.TextField()

    def __str__(self):
        return f"Overweight Assessment for {self.patientname.firstname} on {self.visitdate}"
    
class GeneralAssment(models.Model):
    class Generalquestion(models.TextChoices):
        GOOD = 'Good', 'Good'
        POOR = 'Poor', 'Poor'

    class Otherquestion(models.TextChoices):
        YES = 'Yes', 'Yes'
        NO = 'No', 'No'

    patientname = models.ForeignKey(PatientRegistration, on_delete=models.CASCADE)
    visitdate = models.DateField()
    generalhealth = models.CharField(
         max_length=5,
        choices=Generalquestion.choices
    )
    question2 = models.CharField(
        max_length=5,
        choices=Otherquestion.choices
    )
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
