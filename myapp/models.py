from django.db import models
from django.contrib.auth.models import User



#create new model Hospital
class Hospital(models.Model):
    h_name = models.CharField(max_length=50)
    h_address = models.CharField(max_length=80)
    h_rating = models.IntegerField(default=0)
    h_rcount = models.IntegerField(default=0)

    def __str__(self):
        return self.h_name

class Review(models.Model):
    class Rating(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
    stars = models.IntegerField(choices=Rating.choices)
    review = models.TextField(max_length=200)
    r_creator = models.ForeignKey(User, on_delete=models.CASCADE,related_name="review_creator",default=None)
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE,related_name='review')

class Doctor(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    doctor_name = models.CharField(max_length=30)
    doctor_speciality = models.CharField(max_length=30)
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE,related_name="doctor")
    
    def __str__(self):
        return self.doctor_name

class Patient(models.Model):
    name = models.CharField(max_length=30)
    alive = models.BooleanField(default=True)
    address = models.CharField(max_length=50)
    Birthdate = models.DateField()
    doctor = models.ForeignKey(Doctor,on_delete=models.SET_NULL,null=True,related_name='patient')
    # hospital = models.OneToOneField(Hospital,on_delete=models.CASCADE,related_name='patients')
    # country = models.TextChoices(Choice = countries)
    def __str__(self):
        return self.name
    countries = [
        ('INDIA', 'India'),
        ('RUSSIA', 'Russia'),
        ('ISRAIL', 'Israil'),
        ('ICELAND', 'Iceland'),
        ('AUSTRALIA', 'Australia'),
        ('JAPAN', 'Japan'),
    ] 
    country = models.CharField(
        max_length=10,
        choices=countries,
        default='INDIA',
    )
