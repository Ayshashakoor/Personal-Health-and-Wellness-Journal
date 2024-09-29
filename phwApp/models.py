from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Registration(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=20)
    age = models.IntegerField(null=True)
    gender=models.CharField(max_length=20,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Expert(models.Model):
    name=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    add=models.CharField(max_length=100)
    con=models.BigIntegerField()
    lic=models.ImageField()
    psw=models.CharField(max_length=20)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

class Request(models.Model):
    date = models.DateField(auto_now=True,null=True)
    user=models.ForeignKey(Registration,on_delete=models.CASCADE)
    height=models.CharField(max_length=20,null=True)
    weight=models.CharField(max_length=20,null=True)
    healthstat=models.CharField(max_length=200,null=True)
    bmi=models.CharField(max_length=200,null=True)
    bmr=models.CharField(max_length=200,null=True)
    goal=models.CharField(max_length=200,null=True)
    activeStatus=models.CharField(max_length=200,null=True)
    reqCal=models.CharField(max_length=200,null=True)
    status=models.CharField(max_length=500, default='In Progress')

class FoodJournals(models.Model):
    date = models.DateField(auto_now=True,null=True)
    user=models.ForeignKey(Registration,on_delete=models.CASCADE)
    calorieIntake = models.CharField(max_length=20,null=True)
    status = models.CharField(max_length=50,null=True)

class WorkoutJournals(models.Model):
    date = models.DateField(auto_now=True,null=True)
    user=models.ForeignKey(Registration,on_delete=models.CASCADE)
    duration = models.CharField(max_length=20,null=True)
    workouts = models.CharField(max_length=200,null=True)
    status = models.CharField(max_length=50,null=True)

class SleepJournals(models.Model):
    date = models.DateField(auto_now=True,null=True)
    user=models.ForeignKey(Registration,on_delete=models.CASCADE)
    duration = models.CharField(max_length=20,null=True)
    desc = models.CharField(max_length=200,null=True)
    status = models.CharField(max_length=50,null=True)

class MedicalJournals(models.Model):
    date = models.DateField(auto_now=True,null=True)
    user=models.ForeignKey(Registration,on_delete=models.CASCADE)
    desc = models.CharField(max_length=20,null=True)
    report = models.FileField()

class Videos(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True,null=True)
    title=models.CharField(max_length=20)
    file=models.FileField()

class Tips(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True,null=True)
    title=models.CharField(max_length=20)
    desc=models.CharField(max_length=200)
    
class Blogs(models.Model):
    user=models.ForeignKey(Registration,on_delete=models.CASCADE,null=True)
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE,null=True)
    date = models.DateField(auto_now=True,null=True)
    title=models.CharField(max_length=20)
    desc=models.CharField(max_length=200)

class Chat(models.Model):
    user=models.ForeignKey(Registration,on_delete=models.CASCADE)
    expert=models.ForeignKey(Expert, on_delete=models.CASCADE)
    sendby=models.CharField(max_length=40)
    date=models.DateField(auto_now_add=True)
    message=models.CharField(max_length=400)

class Comments(models.Model):
    date = models.DateField(auto_now_add=True)
    comment = models.CharField(max_length=200)
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    user = models.ForeignKey(Registration, on_delete=models.CASCADE,null=True)
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE,null=True)

class Doctor(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    email=models.EmailField()
    qualification=models.FileField(null=True)
    experience=models.CharField(max_length=100)
    specialization=models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Booking(models.Model):
    bookeddate=models.DateField(auto_now_add=True,null=True)
    regid=models.ForeignKey(Registration,on_delete=models.CASCADE)
    docid=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    bookingdate=models.DateField()
    time=models.CharField(null=True, blank=True,max_length=20)
    token=models.IntegerField(null=True, default=0)
    status=models.CharField(max_length=100, default='Booked')

class Payment(models.Model):
    bid=models.ForeignKey(Booking,on_delete=models.CASCADE)
    paydate=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=50)

class Prescription(models.Model):
    date=models.DateField(auto_now_add=True,null=True)
    bid=models.ForeignKey(Booking,on_delete=models.CASCADE)
    diagnosis=models.CharField(max_length=100)    
    prescription=models.CharField(max_length=100)  
    status=models.CharField(max_length=10,null=True,default='Prescribed')